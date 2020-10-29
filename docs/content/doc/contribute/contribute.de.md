---
title: Mitwirken
subtitle: Wie Du dieses Projekt unterstützen kannst.
weight: 10000

menu:
  doc:
    parent: contrib
---

Falls Du beitragen möchtest, gibt es mehrere verschiedene Möglichkeiten.

## Übersetzungen

Den schnellsten Beitrag kannst Du bei der Übersetzung leisten. Sollte Dir ein Fehler in einer der Übersetzungen der Software auffallen, so kannst Du selbstständig eine Änderung auf [Transifex](https://www.transifex.com/university-of-munster/sciebo-rds/) vornehmen, welche wir anschließend überprüfen und gegebenenfalls übernehmen.

Im der folgenden Grafik kannst Du sehen, welche Sprachen noch deine Unterstützung benötigen. Ist eine Sprache nicht dabei, welche Du beherrschst, dann melde Dich gerne bei uns auf Github / E-Mail / Transifex.
{{<rawhtml>}}
<a href="https://www.transifex.com/university-of-munster/sciebo-rds/translate/" target="_bank"><img border="0" src="https://www.transifex.com/projects/p/sciebo-rds/resource/plugins-owncloud-rds-l10n-templates-rds-pot--master/chart/image_png"/></a>
{{</rawhtml>}}

## Entwicklungen

Solltest Du Programmierkenntnisse besitzen bzw. möchtest bei der Programmierarbeit behilflich sein, so kannst Du auch den [Github-Workflow](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) nutzen, um einen Pull Request auf der Plattform abzusetzen. Anschließend werden wir uns deine Änderungen anschauen und akzeptieren, falls es den folgenden Kriterien entspricht. Ideen und Hilfe findest Du ebenfalls auf Github in den [Issues](https://github.com/Sciebo-RDS/Sciebo-RDS/issues).

---

## Änderungen umsetzen

### Änderungen an Microservice-Komponenten

Um die Änderungen in eine laufende Instanz zu übernehmen, müssen die entsprechenden Charts in der [Helm-Repo](https://github.com/Sciebo-RDS/charts) aktualisiert werden. Dafür wird für jede Komponente eine neue Chart benötigt. Außerdem muss bei Änderungen die entsprechende [All-](https://github.com/Sciebo-RDS/charts/blob/master/charts/all/Chart.yaml#L5) oder [Dev-](https://github.com/Sciebo-RDS/charts/blob/master/charts/dev/Chart.yaml#L5)Chart bearbeitet werden, sodass diese auch den korrekten Container aufsetzen. Den entsprechenden Tag für einen solchen Container entnimmt man aus der [Pipeline-Nummer](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/-/pipelines/67380) aus Gitlab. Diese dienen als Identifikator für die aus der Pipeline heraus erzeugten Containern in der [Gitlab-Registry](https://zivgitlab.uni-muenster.de/sciebo-rds/sciebo-rds/container_registry).
Sobald eine Chart aktualisiert wurde, sollte stets die [Chart-Version](https://github.com/Sciebo-RDS/charts/blob/master/charts/all/Chart.yaml#L5) erhöht werden, um die Änderungen an die entsprechenden Tools zu kommunizieren. Eine Github-Pipeline im Helm-Repo werden bei einem `git push` die Änderungen online verfügbar machen.

Falls ein neuer Microservice hinzugefügt wurde, so muss der Proxy in den [Installationshilfen-Repo](https://github.com/Sciebo-RDS/getting-started) angepasst werden (in der [configuration.yaml](https://github.com/Sciebo-RDS/getting-started/blob/master/deploy/configuration.yaml.example#L22)). Sollte dies nicht passieren, so werden die Anfragen an den falschen DNS-Server weitergeleitet und werden somit nicht im RDS-System bearbeitet. Die Änderungen an Proxies durch `kubectl -f configuration.yaml` müssen durch das Löschen und neu aufsetzen von den Deployments aufgespielt werden, da dies ansonsten nicht in die Pods übernommen wird.

### Änderungen an der Dokumentation

Aktuell werden Dokumentationsänderungen lediglich bei Änderungen von Microservice-Komponenten übernommen durch die Gitlab-Pipeline. Hier wird in Zukunft noch nachgebessert.

### Änderungen an den Integrationen

{{<callout "info">}}
Aktuell existiert nur die Integration in ownCloud mittels eines Plugins.
{{</callout>}}

Um Änderungen an der ownCloud-App mit in den Marketplace von ownCloud zu übernehmen, müssen diese Änderungen zuerst als [Pull Request](https://github.com/Sciebo-RDS/plugin-ownCloud) angezeigt werden. Sollten diese Änderungen in den Hauptstrang des Git-Repos übernommen werden, so muss nun die Versionsnummer in der [info.xml](https://github.com/Sciebo-RDS/plugin-ownCloud/blob/master/rds/appinfo/info.xml) angehoben werden und die [signature.json](https://github.com/Sciebo-RDS/plugin-ownCloud/blob/master/rds/appinfo/signature.json) neu generiert werden. Die Signatur wird automatisch in der [Github-Pipeline](https://github.com/Sciebo-RDS/plugin-ownCloud/releases) gebaut und angeboten. Die daraus erzeugte `tar.gz`-Datei muss anschließend in den [Marketplace](https://marketplace.owncloud.com/account/products) hochgeladen werden. Nun ist die Änderung für jede Instanz verfügbar und kann über die ownCloud-eigenen Prozesse aktualisiert werden.
