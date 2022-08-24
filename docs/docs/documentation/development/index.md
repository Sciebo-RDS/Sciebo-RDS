---
displayed_sidebar: developmentSidebar
---

# Development

## Gitlab Branching Workflow

We follow the [Gitlab-flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html), so our default branch is called `develop` and can be changed exclusively through pull requests via Github (don't let the fact that we are using the Git**lab**-flow on Git**hub** confuse you). When a certain amount of features are done, they are merged into `release`. From there, we set a tag and publish the changes in helm and docker repositories.