[![pipeline status](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/badges/master/pipeline.svg)](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/commits/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/bb2f184b5e422e1366bd/maintainability)](https://codeclimate.com/github/Sciebo-RDS/Sciebo-RDS/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bb2f184b5e422e1366bd/test_coverage)](https://codeclimate.com/github/Sciebo-RDS/Sciebo-RDS/test_coverage)

# Sciebo research data services

Documentation: https://www.research-data-services.org

## Explanation of the folder structure

We use a monorepo to make it easier to track related changes. We used to have multiple repos, but this meant that changes were spread across many repos, making it almost impossible to track.
Therefore, the following will give an impression of the individual services.
If you want to contribute, you have to follow this rules (especially the RDS folder) or create your own repo for your own connector service.

| Foldername      | Description                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------- |
| charts          | Helm charts                                                                                                      |
| docs            | Website with documentation                                                                                       |
| getting-started | Files for easy deployment                                                                                             |
| RDS             | The code for the [connector services](https://www.research-data-services.org/doc/impl/infrastructure/ecosystem/). |
| Root            | Metafiles and configuration                                                                                      |