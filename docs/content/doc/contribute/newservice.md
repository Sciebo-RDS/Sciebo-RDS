---
title: New Service
subtitle: How to register a new service

menu:
  doc:
    parent: contrib

mermaid: true
weight: 10010
---
The following describes how the microservices work together and how a new one is created and integrated into the system. The architecture is explained once again, and some terms are clarified in order to then go into the process and implementation of a service. It also describes how to use the Gitlab CI Pipeline and configure it for the new service.

# Architecture

The advantage of the microservice architecture is that each service can be written in a different language to best solve the problem that needs to be solved. Currently, most microservices are written in Python3, so all available libraries and facilities are written in this language.

If you have not yet internalized the [architecture and its concepts](/doc/arc42/indroduction/), you should pause here and read the [related documentation](/doc/arc42/ecosystem/) before continuing.

Remember that the third and deepest layer is where the most important components of the system run. This includes the [Token Storage](/doc/impl/central/token-storage/) and the [Research Manager](/doc/impl/central/research-manager/). These are particularly important for the further process, as they define which services the user can access.

## Project term in RDS context

Since RDS is a metasystem which connects other systems and services, it is necessary to create a project within RDS which the user can configure on his own. However, many systems use the term project, so that confusion can arise during meetings when RDS is to be used as a system to connect the projects of the different services via RDS (which in turn organizes the connections as a project).

For this reason, we have decided to use the term *research context*, which should be used synonymously with (research) project, so that this confusion is reduced.

## Choosing the layer

Before we start, you should make it clear in which layer your micro service is to be classified.

* **Layer 1**: your microservice integrates a service into the RDS ecosystem. Your service is called *port service*.
* **Layer 2**: your microservice uses a microservice from layer 1 and/or layer 3 and processes information, but does not store any information, so it is stateless. Your service is called *UseCase Service*.
* **Layer 3**: your microservice is essential for the entire ecosystem and / or stores information. Your service is called *Central Service*.

If your service does not fit into any of the layers, you should consider splitting your service into several microservices so that the functions you implement can be used by as many other services as possible.

As a rule of thumb you should consider the following:
{{<callout info>}}
A micro service basically pursues only one goal and its task can be described in one sentence. This guarantees reusability and reduces the complexity of your service. It also reduces the dependency of the whole system to a few services (see [Clean Architecture](/doc/arc42/contextboundary/#section-solid-arch)).
{{</callout>}}


# Procedure and implementation

The following describes the general procedure as well as the implementation and integration of the service into the RDS system. The previous section described how you can see in which layer your service can be, so now you can look up in the corresponding section how to integrate your service into the RDS system.

## Layer 1

Since your microservice integrates a service into the RDS system, it must register in the Token Storage so that it can offer your microservice in the plugins in the registration process. The Token Storage requires all Oauth2 workflow information (Client ID, Client Secret, authorize url, etc.). For this you use the */service* endpoint of the [Token Storage](/doc/impl/central/token-storage).

``` mermaid
sequenceDiagram
  participant PS as Port Service
  participant TS as Token Storage

  PS->>TS: Registration
```

Your port service should do the login as one of the first steps before starting the API service. When logging on, you must specify which interface (more on this in a moment) has been implemented. This interface is important because your service will be used later by other microservices. RDS uses several OpenAPIv3 specifications to ensure communication between the microservices.

Since your service is in layer 1, it can be used by other microservices than [files](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/layer2_use_cases/interface_port_file_storage.yml)- ([example: Owncloud](/doc/impl/ports/port-owncloud/)) and / or [metadata store](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/layer2_use_cases/interface_port_metadata.yml) ([example: Zenodo](/doc/impl/ports/port-invenio/)).

With the following Python function you can register your service with *Token Storage*.

``` python
def register_service(servicename: str, authorize_url: str, refresh_url: str, client_id: str, client_secret: str):
    tokenStorage = os.getenv("CENTRAL_SERVICE_TOKEN_STORAGE")
    if tokenStorage is None:
        return False

    data = {
        "servicename": servicename,
        "authorize_url": authorize_url,
        "refresh_url": refresh_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "implements": ["fileStorage", "metadata"]
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"{tokenStorage}/service", json=data, headers=headers)

    if response.status_code is not 200:
        raise Exception(
            "Cannot find and register Token Storage, msg:\n{}".format(response.text)

    response = response.json()
    if response["success"]:
        logger.info(
            f "Registering {servicename} in token storage was successful.")
        return True

    logger.error(
        f "There was an error while registering {servicename} to token storage.\nJSON: {response}")

    return False
```

 Note that there is a list in the data-dict in the "implements"-key, which has to be adapted by you, depending on the interface you are implementing.

| Interface        | Implements  |
| ---------------- | ----------- |
| fileStorage      | fileStorage |
| metadata storage | metadata    |


## Layer 2 and 3

Your service does not require registration, because it is called directly via GUI or calls other services independently.

## Connexion-Plus

In order to make working with Python in conjunction with Flask much easier, we started with Connexion, as it directly builds an API server from an OpenAPIv3 specification using Flask. By adding functionality and extending some more libraries [Connexion-Plus](https://pypi.org/project/connexion-plus/) was created. It is strongly recommended to use this library, because many functions like opentracing and Prometheus metrics are added automatically, which are needed for a successful integration (see [Contribute](/doc/contribute/)).

## Logging with Opentracing

In the microservice universe, jaeger on top of opentracing is a very popular choice for distributed logging. It is very benefecial and user-friendly to implemend this in your service. Please take a look to the [manual for jaeger](https://www.jaegertracing.io/docs/1.21/client-libraries/#supported-libraries) for more.

## Prometheus

Please provide some internal numbers from your service via prometheus metrics via */metrics* endpoint. This helps to find problems within the RDS system and your service.

## Gitlab CI

RDS uses Gitlab and its CI System to test the source code and call other functions, including creating and publishing containers.

To use the Gitlab CI, a *.gitlab-ci.yaml* is required in the project folder. As an example, you should look into one that already exists ([Example: Owncloud](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/layer1_adapters_and_ports/port_owncloud/.gitlab-ci.yml)).

In this file you can describe how your service is tested, built and stored. To do this, use existing jobs from the central [*.gitlab-ci.yaml* file](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/.gitlab-ci.yml#L68) in the root directory of the git repository. You also place your newly created file in the *includes* in this central file, so that it will be executed by the pipeline on a *pull request*.

If you don't want to use the predefined procedures, you must overwrite them by specifying your own *script* sections. Otherwise, you will need a *Makefile* ([Example: Owncloud](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/layer1_adapters_and_ports/port_owncloud/Makefile)), which will be executed to test and build your service and then offer it in the gitlab's package directory.

{{<callout warning>}}
It is strongly recommended to use Makefiles to implement the required processes and not to overwrite the scripts in the .gitlab-ci.yaml file, as this can lead to problems in the pipeline. In Makefiles these errors are avoidable. Note: The pipeline uses Ubuntu as a basis.
{{</callout>}}

### Documentation

Your service should automatically keep its own documentation up to date, so that other users can continue to use the documentation. For this you should take a look at an already existing service ([Example: Owncloud](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/layer1_adapters_and_ports/port_owncloud/Makefile#L26)). There you can see how [pydoc-markdown](https://pypi.org/project/pydoc-markdown/) ([Note: Issue 43](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/43)) and Python's DocString can be used to create a markdown file and move it to the correct documentation folder (Note: [pydocmd.yml](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/layer1_adapters_and_ports/port_owncloud/pydocmd.yml) in the same folder). There you will find another markdown file, which integrates this new markdown file using the code short code ([Example: Owncloud](https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/docs/content/doc/impl/ports/port-owncloud.de.md)). You should also implement the same functionality so that when you merge your pull request, the [Website](https://www.research-data-services.org/doc/impl/ports/port-owncloud/) will be updated by the Gitlab CI pipeline. By the way, this applies whenever a change to your code is detected, so not just a merge will trigger this automation.


### Docker file

To build a container, your service needs a *dockerfile* ([Example: Owncloud](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/RDS/layer1_adapters_and_ports/port_owncloud/dockerfile)) in the project folder (the same one where the *.gitlab-ci.yaml* is located, also note that it is case sensitive).

This is where you can define the build process, which packages and programs will be installed and your software will run.

### Kubernetes and Helm Chart

In RDS we use Helm Charts to generate the configuration files for Kubernetes. Therefore your service needs a corresponding [Helm Chart](https://helm.sh/). In the [deploy](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy) folder of the Git repository you will find all available charts and a [Makefile](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy/Makefile) which allows you to apply the available charts to an existing Kubernetes cluster.

First, create a folder with a conventionally named folder: *circle[1,2,3]_servicename*. Then follow the [Helm Developers Guide](https://helm.sh/docs/chart_template_guide/) to create and configure your own chart in the new folder.

Then add the Makefile in the *deploy* folder to set up your service in Kubernetes. For this you create two own procedures:
- the first one installs or renews your service and
- the second one uninstalls your service

It is best if your second procedure has the same name as the first, but with the addition *remove\_* in front of it (example: [port_owncloud](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy/Makefile#L44) and [remove_port_owncloud](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy/Makefile#L77)) Then you add your first procedure to the corresponding procedure *layer1*, *layer2* or *layer3* ([see Makefile](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy/Makefile#L62)). The same applies to your *remove\_* procedure, which will be added to one of the following procedures: *uninstall_layer1*, *uninstall_layer2* or *uninstall_layer3* ([see Makefile](https://github.com/Sciebo-RDS/getting-started/tree/master/deploy/Makefile#L95))

# Integration with GUI plugins

Currently, if you are implementing a new service in layer 2 or 3, it is necessary to create your own plugins, as they currently have no automation to integrate the new endpoints. All available plugins can be found in the root folder of the Git repository. The services in layer 1, called the Port Service, are automatically provided by the Token Storage, connected to the Research Manager, and used by the Metadata and Exporter Service.

Select a plugin ([Example: Owncloud](https://github.com/Sciebo-RDS/plugin-ownCloud)) and see the integration. (Owncloud itself offers a [Developer Manual](https://doc.owncloud.com/server/developer_manual/).)

# Example service

Unfortunately, no sample service exists at present. ([See Issue 42](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/42))
