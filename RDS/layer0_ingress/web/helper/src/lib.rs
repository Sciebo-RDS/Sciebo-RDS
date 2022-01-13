extern crate redis;
extern crate serde;

use redis::{Client, Commands};
use serde::{Deserialize, Serialize};
use std::sync::mpsc;
use std::thread::{self, JoinHandle};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    username: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct JSONUser {
    r#type: String,
    data: User,
}

#[derive(Serialize, Deserialize, Debug)]
struct Service {
    servicename: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct JSONService {
    r#type: String,
    data: Service,
}

#[derive(Serialize, Deserialize, Debug)]
struct Token {
    service: JSONService,
    access_token: String,
    user: JSONUser,
}

#[derive(Serialize, Deserialize, Debug)]
struct JSONToken {
    r#type: String,
    data: Token,
}

pub struct Describo {
    describo_data: String,
    token: String,
}

#[derive(Clone)]
pub struct Config {
    pub client: Client,
    pub redis_channel: String,
    pub describo_url: String,
    pub describo_secret: String,
}

pub fn start_redis_listener(config: Config) -> (mpsc::Receiver<String>, JoinHandle<()>) {
    let (sender, receiver) = mpsc::sync_channel(1000);

    let handle = thread::spawn(move || {
        let mut con = config.client.get_connection().expect("Redis not available");

        // subscribe redis key "TokenStorage_Refresh_Token", wait for data
        let mut pubsub = con.as_pubsub();
        pubsub.subscribe(config.redis_channel).unwrap();

        println!("Start redis listener");

        loop {
            println!("Wait for message.");
            let msg = match pubsub.get_message() {
                Ok(v) => v,
                Err(_) => {
                    print!("Lost connection to redis.");
                    break;
                }
            };

            let payload: String = match msg.get_payload() {
                Ok(v) => {
                    println!("got message, channel '{}': {}", msg.get_channel_name(), v);
                    v
                }
                Err(_) => {
                    println!("Got no valid message from pubsub redis.");
                    continue;
                }
            };

            if sender.send(payload).is_err() {
                print!("There was an critical error while sending payload.");
                break;
            }
        }
        println!(" Quit redis pubsub thread.")
    });
    (receiver, handle)
}

pub fn start_lookup_userid_in_redis(
    config: Config,
    payloads_rcv: mpsc::Receiver<String>,
) -> (mpsc::Receiver<Describo>, JoinHandle<()>) {
    let (sender, receiver) = mpsc::sync_channel(1000);

    println!("Start sessionid lookup");

    let handle = thread::spawn(move || {
        let mut con = config.client.get_connection().expect("Redis not available");

        for payload in payloads_rcv {
            println!("got payload: {:?}", payload);

            let t: JSONToken = match serde_json::from_str(&payload) {
                Ok(v) => v,
                Err(e1) => {
                    eprintln!("Payload error: \n{}", e1);
                    continue;
                }
            };

            if t.data.service.data.servicename != "port-owncloud" {
                println!("skip: It is not for owncloud");
                continue;
            }

            // lookup in redis for user_id to get sessionId
            let describo_data: String = match con.get(&(t.data.user.data.username)) {
                Ok(v) => v,
                Err(err) => {
                    if err.is_connection_dropped() {
                        println!("Redis not available");
                        break;
                    }
                    println!("key '{}' not found in redis.", t.data.user.data.username);
                    continue;
                }
            };

            println!("found describo: {}", describo_data);
            if sender
                .send(Describo {
                    describo_data,
                    token: t.data.access_token,
                })
                .is_err()
            {
                println!("There was an critical error while sending sessionId.");
                break;
            }
        }

        println!("Redis pubsub channel not sending anymore. Quit lookup userid in redis thread.");
    });

    (receiver, handle)
}

use serde_json::Value;

pub fn start_update_describo(
    config: Config,
    describo_rcv: mpsc::Receiver<Describo>,
) -> JoinHandle<()> {
    println!("Start describo session updater");

    let handle = thread::spawn(move || {
        for d in describo_rcv {
            let mut describo_data: Value = match serde_json::from_str(&d.describo_data) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("invalid parsing: {}", e);
                    continue;
                }
            };

            println!("Got token: {}\n describo_data: {}", d.token, describo_data);

            describo_data["payload"]["session"]["owncloud"]["access_token"] =
                serde_json::Value::String(d.token);

            let session_id = describo_data["sessionId"].as_str().unwrap().to_string();
            let request_body = &describo_data["payload"];
            let describo_url = format!("{}/{}", config.describo_url, session_id);

            println!(
                "Sent: url: {}, sessionId: {}, secret: {}\npayload: {}",
                describo_url, session_id, config.describo_secret, request_body
            );

            let res = reqwest::blocking::Client::new()
                .put(describo_url)
                .bearer_auth(&config.describo_secret)
                .header("Content-Type", "application/json")
                .json(request_body)
                .send();

            match res {
                Ok(v) => {
                    println!("response from describo: {:?}", v);
                }
                Err(err) => {
                    println!(
                        "Invalid request to describo, status_code: {}",
                        err.status().unwrap()
                    );
                }
            }
        }

        println!("Redis lookup channel not sending anymore. Quit describo updater thread.");
    });

    handle
}
