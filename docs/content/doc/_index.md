---
title: Documentation
subtitle: All what you have to **know** about the <i>doc</i>
weight: -999
---

## Workflow

We use Github as a repository for the source code. As CI/CD platform we use Gitlab and its own runners, which are also available to external people through a connection to the Github repository.
These are used automatically and its defined tasks are triggered as soon as a relevant line of code is changed. As a result of successful test cases, a container (currently we use Docker) is created, which is stored in Gitlab's internal package folder, so that Kubernetes can download and use the created containers from there. These packages are publicly available.

In this documentation, the functionality and concepts are clearly described using Arc42 documentation, as well as the interfaces implemented by RDS using OpenAPIv3 and defined libraries using function declarations and DocString.
