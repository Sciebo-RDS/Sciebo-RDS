---
title: Pipeline
subtitle: How the gitlab pipeline works.
weight: 10003

menu:
  doc:
    parent: contrib
---

For all activities, a pull request is then triggered via github. The changes are then tested via our Gitlab and accepted by one of the main developers. The changes are then incorporated into the microservices and documentation. The following picture describes the pipeline process in Gitlab.

![Gitlab Pipeline](/images/rds-pipeline.jpg)

## Branching

We follow the gitlab-flow, so you have to develop all your stuff inside of a separate branch rooted from `develop`, make a pull request into `develop` and after some features are completed, we merge it into `release` and tag it with git `major.minor.subminor`. For `develop` branch, we deploy it into our demo installation right away for testing purpose. The helm charts will be published only in `release`. 

You have to specify the tag in the helm charts for the image tags in `develop` branch already, so you need to know what tag version you will want to use. So the easiest way to publish a new version is:

- create your feature in `develop`, 
- check for latest tag, set next tag number in helm charts
- merge into release, set tag on this merge commit
- `git push --all`