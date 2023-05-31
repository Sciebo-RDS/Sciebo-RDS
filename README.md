
# Sciebo RDS
[![pipeline status](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/badges/develop/pipeline.svg)](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/pipelines)
![MIT License](https://img.shields.io/github/license/Sciebo-RDS/Sciebo-RDS)
[![Version](https://img.shields.io/github/v/release/Sciebo-RDS/Sciebo-RDS)](https://github.com/Sciebo-RDS/Sciebo-RDS/releases/latest)
![Release](https://img.shields.io/github/release-date/Sciebo-RDS/Sciebo-RDS)
[![gitter](https://img.shields.io/gitter/room/Sciebo-RDS/community?color=orange)](https://gitter.im/Sciebo-RDS/community)

Sciebo RDS (**Sciebo** **R**esearch **D**ata **S**ervices) allows researchers to enrich their research data with metadata and to export it directly from Enterprise Sync and Share (EFSS) Systems like Owncloud to Data Repositories like Zenodo and OSF.
It acts as a interoperability layer, allowing them to assign a directory on a Sync and Share System to a research project, annotating the contained data to match the format required by the desired Data Repository and publishing the Research Data directly from the Cloud.

No need to download all the data to a desktop computer to cumbersomely upload it to the repository interface again.


Find more information on the official website at [www.research-data-services.org](https://www.research-data-services.org/).

## Screenshots
|||
|-|-|
|<img  width="475" alt="An_RDS1" src="https://user-images.githubusercontent.com/31971585/196733077-d008bbc9-9c2a-4e59-81fc-718c46af481e.png"> Configuring a project|<img  width="475" alt="An_RDS2" src="https://user-images.githubusercontent.com/31971585/196733085-c5ab157e-27b1-42ea-87f2-512b4db29fcf.png"> Adding metadata|
|<img width="475" alt="An_RDS2" src="https://user-images.githubusercontent.com/31971585/196733090-4eba7303-37f8-48e7-8d11-cbb1a8ff4cfb.png"> Adding metadata|<img width="475" alt="An_RDS4" src="https://user-images.githubusercontent.com/31971585/196733098-df0696bf-4fbc-4a12-b133-23769103cbe5.png"> Adding metadata|
|<img width="475" alt="An_RDS5" src="https://user-images.githubusercontent.com/31971585/196733100-f26e9b9b-ee5c-4c23-9716-22f7bc2574a4.png"> Publishing|<img width="475" alt="An_RDS6" src="https://user-images.githubusercontent.com/31971585/196733102-7b95063f-0a56-427f-bce8-993ac1fbae82.png"> <center>Connecting repositories</center>|


## Deployment

#### Requirements

To deploy Sciebo RDS you will need:

1. A Kubernetes cluster
2. An OwnCloud instance
3. Two different domains

#### Getting Started

Please refer to our [Getting Started](https://www.research-data-services.org/gettingstarted/) Guide to learn how to deploy Sciebo RDS.

#### Development environment

To deploy a local environment on top of [Minikube](https://minikube.sigs.k8s.io/docs/), including RDS and NextCloud and / or OwnCloud,
please refer to [this guide](/getting-started/minikube-embedded/README.md).

## Monorepo Structure

We use a monorepo to make it easier to track related changes. This means that you will find all relevant files in this Github repository.

The following table will give an impression of the individual parts.  

| Folder                                                       | Description                                     |
| ------------------------------------------------ | ----------------------------------------------- |
| /charts                                          | Helm charts                                     |
| /docs                                            | Website with documentation                      |
| /getting-started                                 | Files for easy deployment                       |
| /RDS                                             | The RDS code                                    |
| /RDS/layer0_ingress/web/server                   | The Python Backend                              |
| /RDS/layer0_ingress/web/client/packages/codebase | The Vue.js Frontend                             |
| /RDS/layer3_central_services                     | Microservices `ResearchManager`, `TokenStorage` |
| /                                                | Metafiles and configuration                     |

The monorepo only includes those parts of Sciebo RDS that are officially maintained by the University of Münster.

### Additional Repositories
There is also an [additional repository](https://github.com/Sciebo-RDS/RDS-Connectors) that functions as a community hub for development of 3rd party connectors, such as Dataverse. These connectors are community managed – if you are planning on developing a connector and sharing it as Open Source, feel free to use this repository.    
A third repository is used for the ongoing development of the [Nextcloud Plugin](https://github.com/Sciebo-RDS/plugin-nextcloud).

## Contributing and Documentation

Contributions are always welcome! You can find technical documentation and guides on how to extend Sciebo RDS to your needs and connect additional repositories on our [website](https://www.research-data-services.org/documentation/development/).

We follow the [Gitlab-flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html). Our default branch is called `develop` and can be changed exclusively through pull requests via Github.    
When a certain amount of features are done, they are merged into `release`. From there we will set a tag and publish the changes in helm and docker repositories.

Please adhere to our `code of conduct`.

## Feedback and Support

Please use the Github Issues and Github Discussions for feedback and technical questions. We also have a [Gitter chat](https://gitter.im/Sciebo-RDS/community). :)

If you are using Sciebo RDS as a researcher and need user level support, please refer to the administrators of your Sciebo RDS instance. You can find their email adresse in the `Help` tab of your Sciebo RDS instance.
## Acknowledgements

Sciebo RDS relies on [describo-online](https://github.com/Arkisto-Platform/describo-online) for metadata management.
## Authors

Sciebo RDS is a project developed by the [University of Münster](https://uni-muenster.de/) and funded by the [DFG](https://www.dfg.de/en/index.jsp).

You can reach the development team at `sciebo.rds <at> uni-muenster.de` or on [Gitter](https://gitter.im/Sciebo-RDS/community).
