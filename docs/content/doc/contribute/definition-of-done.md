---
title: Definition of done
subtitle: What you have to provide for your microservices.

menu:
  doc:
    parent: contrib

mermaid: true
weight: 10007
---

## Definition of Done

Here all properties are listed, which a microservice and its associated files have to fulfill in order to be accepted and included in the RDS ecosystem.

### For a microservice exists

- a separate folder in the (mono) repo
- a gitlab-ci file, which is a
    - Testing of the following requirements,
    - successful compilation and
    - Building a docker image is possible.
        - The docker image is stored in the Gitlab registry
        - The Docker image is marked by a tag based on the respective JobID
        - The Docker image is additionally marked as the latest in the master during a merge using a tag
- a working Kubernetes configuration in the form of Helm charts for deploying the microservice in the same
    - with an Ingress-,
    - a deployment (with a liveness and/or readiness sample) and
    - a service configuration

### For testing exists

- for each more complex function at least one unit test with a language-specific test framework (PHPUnit, JUnit, PyTest, Jest, etc), which includes the following cases
    - a standard input with expected parameters
    - a zero entry for one parameter or zero entries for all parameters
    - for all marginal cases, which are identified during Sprint Planning and checked during implementation
- For each function to be externally connected (usually external API endpoints) a contract unit test using Pact
    - the resulting pact file is automatically stored in the corresponding Gitlab project

### The following aspects are taken into account for operation:

- The microservice provides Prometheus-specific metrics via an API endpoint
    - Additional metrics were decided during the Sprint Planning and recorded in a Sprint Backlog
- The documentation of the software is available at least for externally available functions (are declared as public or API endpoints) and includes
    - the API endpoints are documented by OpenAPI v3
    - Functions are documented with DocString comments
        - a website documentation according to established standards is generated and stored according to the project standards
- The Microservice uses the opentracing technology and picks up corresponding IDs and creates its own chips and returns them to Jaeger so that it can receive and process them.
