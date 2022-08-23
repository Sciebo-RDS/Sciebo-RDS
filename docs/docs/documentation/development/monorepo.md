# Monorepo

We use a monorepo to make it easier to track related changes. It means, you will find all relevant files in a single git repository. You find this repository when you click on the Github Icon top right.

We used to have multiple repos, but this meant that changes were spread across many repos, making it almost impossible to track changes. Therefore, the following will give an impression of the individual services. If you want to contribute, you have to follow this rules (especially the RDS folder) or create your own repo for your own connector service.

| Foldername      | Description                          |
| --------------- | ------------------------------------ |
| charts          | Helm charts                          |
| docs            | Website with documentation           |
| getting-started | Files for easy deployment            |
| RDS             | The code for the connector services. |
| Root            | Metafiles and configuration          |

# Git Branching workflow

We are following the [gitlab-flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html), so our default branch called `develop` can be changed exclusively through pull requests via github. After a certain amount of features are done, it will be merged into `release`. From there, we will set a tag and publish the changes in helm and docker repositories.
