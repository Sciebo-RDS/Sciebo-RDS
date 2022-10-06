---
displayed_sidebar: developmentSidebar
---

# Development
This part of the documentation will show you how to extend Sciebo RDS to match your needs.  
If you have questions to discuss or you just want to say Hi, join our [Gitter Chat](https://gitter.im/Sciebo-RDS/community)!
## Gitlab Branching Workflow

We follow the [Gitlab-flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html). Our default branch is called `develop` and can be changed exclusively through pull requests via Github (don't let the fact that we are using the Git**lab**-flow on Git**hub** confuse you).

When a certain amount of features are done, they are merged into `release`. From there we will set a tag and publish the changes in helm and docker repositories.