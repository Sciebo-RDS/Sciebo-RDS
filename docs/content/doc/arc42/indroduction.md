---
title: Introduction
subtitle: Architecture documentation with Arc42

menu:
  doc:
    parent: architecture
weight: 401
---

## Introduction and goals

The following documentation of the architecture for the *sciebo Research Data Services* is created and maintained by Peter Heiss (peter.heiss@uni-muenster.de). First of all, the core task of the system should be mentioned and then a detailed task description should be explained.

### Core task

The system offers bridging functionalities to already existing research data services and supports the researcher working in Sciebo in his research data management from project development to publication and archiving. The most important aspects are the low-threshold services, reuse of existing services, integration of the system in Sciebo and user experience.

### Task definition

The application documents for this project for the DFG describe many of the tasks in great detail. They can be found in the **sciebo RDS**-specific folder in Sciebo under 'sciebo RDS/Documents-DFG/DFG-Antrag_sciebo_RDS_final.pdf'. These are summarized in the following.

| ID  | Request                          | Explanation                                                                                                         |
| --- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| M-1 | Integration in Sciebo            | Researchers are already familiar with Sciebo.                                                                       |
| M-2 | Low-threshold services           | Easy handling guarantees long-term use.                                                                             |
| M-3 | offers bridge functionalities    | Already existing services are connected by bridge functionalities                                                   |
| M-4 | Integration of external services | It is avoided to initiate new developments by reusing already existing services and infrastructures.                |
| M-5 | adapts external expert tools     | The researchers' tools are to be integrated into the bridge functionalities.                                        |
| M-6 | offers basic FDM                 | For this purpose, functionalities for the indexing of research data are developed.                                  |
| M-7 | continuous working methods       | The FDM receives continuous support from project development through operational work to publication and archiving. |

Legend: M = Must, O = Optional

The following figure is a symbolic classification of the software architecture to be generated into the existing internal and external services.

![requirement cluster](/images/request cluster.svg)

A detailed list of all services and repositories to be connected can be found in the application on p. 15.

### Quality objectives

The following table lists goals and requirements that are intended to help stakeholders in the operation and user experience of the services.

| ID  | Prio  | Quality Target | Explanation                                                                                                                             |
| --- | :---: | -------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Q-1 |   2   | Performance    | The system processes user requests as instantaneously or asynchronously as possible, so that the users have no delay in their workflow. |
| Q-2 |   1   | Flexibility    | New functions can be added without much effort. New services can be integrated.                                                         |
| Q-3 |   1   | Security       | User data is not changed during processing, data protection is taken into account. User data remain the property of the user.           |
| Q-4 |   2   | Correctness    | The user guidance and understanding of the functionalities is comprehensible for non-technical departments and meets the expectations.  |
| Q-5 |   3   | Continuous     | The user guidance has a continuous sensible workflow or the users can use their own workflow.                                           |
| Q-6 |   3   | Transparency   | The processing of data is designed transparently and the software is provided as open source.                                           |
| Q-7 |   1   | Monitoring     | All services and orders and their status can be viewed at any time.                                                                     |

Legend: Priority scale 1 (particularly valuable) to 4 (to be aimed at)

(TODO) add scenarios (see 