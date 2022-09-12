---
displayed_sidebar: referenceSidebar
---

# Context delimitation

## Domain knowledge

The following figure is a delimitation of the Sciebo RDS system to be created for all services used. At the same time a first indication of the communication data is given. This is followed by a table for a better explanation of terms used within the figure. This is explicitly not an explanation of the system to be created, but its embedding in existing services.

The representation is a UML diagram. However, for the technical delimitation, data streams and flows should be shown so that the arrows represent the "flow direction" of the data for simplification. The declaration of the arrows with `flow' has been omitted for better readability.

| element         | meaning                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- |
| User            | Groups together all types of users, including students, researchers and administrators                                     |
| DMP             | short form for data management plans, documents the handling of research data by users.                                    |
| Publication     | Groups together all types of publication and archiving of research data.                                                   |
| Arrow direction | Documents the data flow                                                                                                    |
| ?               | Still to be documented (TODO)                                                                                              |
| Authenticator   | Authenticates the user to a system, in this case Sciebo.                                                                   |
| uni-internal    | These are web services which are operated within the EMU.                                                                  |
| uni-external    | These are web services which are operated outside the EMU (and therefore outside the jurisdiction). *data protection risk* |



### Description of the external interfaces

| Service       | Description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| CLARIN        | European Research Infrastructure for Language Resources and Technology |
| ePIC          | Consortium for Persistent Identifiers in the context of eScience       |
| Zenodo        | Open Science Repository developed by CERN                              |
| Rosetta       | Archiving Software and Service of the State of NRW                     |
| RD Repository | Research Data Repository                                               |
| arXiv.org     | A public document server of the natural sciences                       |

### Technical context

The following figure shows the context delimitation with the respective protocols used. The exclusive use of HTTPS and REST is striking. This is because this has already been defined in the order document.

![extensive technical context delimitation](../../../../static/img/kontextabgrenzung_umfeld_technisch.svg)


# Solution strategy {#section-solution-strategy}

| ID   | Task                                        | Solution                                                                                                                             |
| ---- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| L-1  | Sustainable Architecture                    | A microservice approach will combine existing and new services.                                                                      |
| L-2  | asynchronous communication between services | A messaging system can take over the guarantee of message dispatch for tasks.                                                        |
| L-3  | little effort for new features              | [Clean Architecture](/de/doc/arc42/contextboundary/#section-solid-arch) is implemented with microservices.                           |
| L-4  | Data collection by plugins                  | The integration of RDS in different platforms is realized with the existing plugin system.                                           |
| L-5  | Software flexibility                        | Clean Architecture allows a problem to be solved independently of other stacks using the best technology stack for the task at hand. |
| L-6  | Maintainability, Scalability                | Deployment relies on Docker and Kubernetes and Gitlab as integration, test and deployment pipeline.                                  |
| L-7  | Authentication and Authorization            | The architecture uses OAuth2 as the mechanism to perform tasks legitimately to Sciebo or other services.                             |
| L-8  | encrypted communication                     | External communication (e.g. to REST-API) is always via HTTPS / SSL.                                                                 |
| L-9  | RB-9                                        | Reverse Proxy and Caching Server as front-end server for delivering HTML, CSS and JavaScript and accepting API requests.             |
| L-10 | Data storage                                | Basically, microservices are stateless. If necessary, data is stored in cloud storage in layer 3 of the Clean Architecture.          |

# Scenarios

| quality feature                          | scenario                    | measures                                                                                                  |
| ---------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------- |
| L-3                                      | implement new feature.      | Clean Architecture enables linking of services and fast implementation of new features.                   |
| Integration of RDS into existing systems | Integrate RDS into service. | API endpoints and a security system are offered. Integration with platform-specific features is possible. |

## Clean Architecture {#section-solid-arch}

The [SOLID principles](https://de.wikipedia.org/wiki/Prinzipien_objektorientierten_Designs#SOLID-Prinzipien) have already been successfully applied in (enterprise) software development and are known in practice for [its high maintainability and agility](https://www.informatik-aktuell.de/entwicklung/methoden/solid-die-5-prinzipien-fuer-objektorientiertes-softwaredesign.html).

The author [Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) has already thought about an architecture in 2012, but calls it *Clean Architecture* and describes it in detail in his book of the same name. Since the architecture only describes a concept of how a system can be built and the concept of microservices is seen as a deployment concept, these two concepts can be combined. [Martin also wrote about it](https://blog.cleancoder.com/uncle-bob/2014/10/01/CleanMicroserviceArchitecture.html), but in his opinion one should investigate which advantages and disadvantages one gets and the architecture should and must be able to work without microservices.

{{<callout info>}}
In order not to extend this documentation any further, we explicitly refer to the links in the previous section. Otherwise, it is assumed from here on that the concept of Clean Architecture has been understood by the reader.
{{</callout>}}

Above all, the concept of layers and dependencies should be mentioned here.


![Clean Architecture](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg)
Quelle: https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg

The service system in RDS has been built on the basis of these concepts and is shown as a diagram in the [Service Ecosystem](/en/doc/impl/infrastructure/ecosystem/) in this documentation.

Thereby...
- in the outermost layer the services are counted, which connects external and internal services to RDS. For this reason, the containers in this layer are called *ports*.
- in the middle layer contains the services that implement features. For this reason, the containers are called *Use Cases* here.
- the innermost layer contains services that store information or are so essential for the entire system that they cannot be omitted. Here the containers are named *Central*.

This division of microservices can be found in the link overview in this documentation.

## Concept of Integration

Basically the integration of the RDS application is done by the platform specific plugin system.

Due to the diverse landscape of the software, RDS has to provide the highest possible integration diversity. For this reason the decision was made to hand over this responsibility to the target platform: There must be a plugin system that allows the integration of third-party applications. For this reason, RDS only implements API endpoints and makes them available for further use. Owncloud was chosen as the first target platform. Further integrations are possible, but must adhere to the Oauth2 concept.

RDS uses the first token it receives for a user of an integration platform as the main token, so that all subsequently added tokens assigned to the same user and integration platform are interpreted as connected services and offered to the user for selection. This also results in the use of unique user names or IDs for each integration platform. Although the same user name or ID may occur several times in RDS, it must be possible to assign it uniquely with the integration platform as information. 

For this reason, it is also easy to implement new integrations by other platforms, as the new service must offer Oauth2 and the user must be able to authorise himself to RDS with this service. All services connected through RDS can then be given to the user to choose from and authorise, so that RDS can authorise itself to them on behalf of the user. For this purpose RDS offers many different API endpoints, so that the integration can only focus on displaying and sending requests and not on implementing complex algorithms.

## Security concept

The security concept is currently being revised ([See Issue 12](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/12)). Therefore, this section will be revised again.
