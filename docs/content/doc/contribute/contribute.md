---
title: Submit your work
subtitle: How you can contribute to this project
weight: 10000

menu:
  doc:
    parent: contrib
---

If you would like to contribute, there are several different possibilities.

## Translations

You can make the fastest contribution with the translation. If you find an error in one of the translations of the software, you can make a change on [Transifex](https://www.transifex.com/university-of-munster/sciebo-rds/), which we will check and if necessary take over.

In the following graphic you can see which languages still need your support. If you can't find a language you know, please contact us at Github / E-Mail / Transifex.
{{<rawhtml>}}
<a href="https://www.transifex.com/university-of-munster/sciebo-rds/translate/" target="_bank"><img border="0" src="https://www.transifex.com/projects/p/sciebo-rds/resource/plugins-owncloud-rds-l10n-templates-rds-pot--master/chart/image_png"/></a>
{{</rawhtml>}}

## Developments

If you have programming skills or want to help with the programming work, you can also use the [Github-Workflow](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) to place a pull request on the platform. We will then look at your changes and accept them if they meet the following criteria. You can also find ideas and help on Github in the [Issues](https://github.com/Sciebo-RDS/Sciebo-RDS/issues).

---

## Apply changes

### Changes to Microservice components

To apply the changes to a running instance, the corresponding charts in the [Helm-Repo](https://github.com/Sciebo-RDS/charts) must be updated. This requires a new chart for each component. In addition, the corresponding [All-](https://github.com/Sciebo-RDS/charts/blob/master/charts/all/Chart.yaml#L5) or [Dev-](https://github.com/Sciebo-RDS/charts/blob/master/charts/dev/Chart.yaml#L5)Chart must be edited when changes are made, so that they also set up the correct container. The corresponding tag for such a container is taken from the [Pipeline Number](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/pipelines/67380) in Gitlab. These tags serve as identifiers for the containers created from the pipeline in the [Gitlab Registry](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/container_registry).
Once a chart is updated, the [Chart version](https://github.com/Sciebo-RDS/charts/blob/master/charts/all/Chart.yaml#L5) should always be incremented to communicate the changes to the appropriate tools. A github pipeline in Helm-Repo will make the changes available online when a [git push] is performed.

If a new microservice has been added, the proxy must be adjusted in the [installation help repo](https://github.com/Sciebo-RDS/getting-started) (in the [configuration.yaml](https://github.com/Sciebo-RDS/getting-started/blob/master/deploy/configuration.yaml.example#L22)). If this does not happen, the requests will be forwarded to the wrong DNS server and will not be processed in the RDS system. The changes to proxies made by [kubectl -f configuration.yaml] must be applied by deleting and restarting the deployments, otherwise they will not be applied to the pods.

### Changes to the documentation

Currently, documentation changes are only applied by the Gitlab pipeline when changes are made to microservice components. This will be improved in the future.

### Changes to the integrations

{{<callout "info">}}
Currently only the integration into ownCloud via a plugin exists.
{{</callout>}}

To include changes to the ownCloud app in the ownCloud marketplace, these changes must first be displayed as a [Pull Request](https://github.com/Sciebo-RDS/plugin-ownCloud). If these changes are to be included in the main thread of the git repo, the version number in the [info.xml](https://github.com/Sciebo-RDS/plugin-ownCloud/blob/master/rds/appinfo/info.xml) must now be raised and the [signature.json](https://github.com/Sciebo-RDS/plugin-ownCloud/blob/master/rds/appinfo/signature.json) regenerated. The signature is automatically built and offered in the [github pipeline](https://github.com/Sciebo-RDS/plugin-ownCloud/releases). The resulting [tar.gz] file must be uploaded to the [Marketplace](https://marketplace.owncloud.com/account/products) afterwards. Now the change is available for each instance and can be updated using ownCloud's own processes.

Translated with www.DeepL.com/Translator (free version)
