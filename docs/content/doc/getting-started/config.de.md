---
title: Konfiguration
subtitle: Wie konfiguriert man RDS

menu:
  doc:
    parent: installation
weight: 301
---

Man benötigt den Ordner "deploy" aus dem Github Repositorium.

```bash
git clone https://github.com/Sciebo-RDS/Sciebo-RDS.git
cd ScieboRDS/deploy
```

{{<callout info>}}
Falls nur die Helm Charts benötigt werden, kann mit folgendem Befehl das Helm Chart Repositorium hinzugefügt werden.

```bash
helm repo add sciebo-rds https://sciebo-rds.github.io/charts/
```
{{</callout>}}

Darin sind sämtliche Dateien enthalten, welche zur Konfiguration und Installation benötigt werden.

Um die Installation anzupassen, sind mehrere Dateien anzupassen. Dafür liegen im deploy- und in den verschiedenen Microservice-Ordnern ".example"-Dateien, welche kopiert und umbenannt werden sollen und anschließend ggfs. inhaltlich anzupassen sind.

```bash
cp kustomization.yaml.example kustomization.yaml
nano kustomization.yaml
```

In der kustomization.yaml werden u.a. die Proxies definiert, welche möglicherweise in der Umgebung notwendig sind. Dadurch können die Microservices auch außerhalb des Clusters verfügbare Services erreichen, falls der Cluster keine eigene weltweite IP besitzen sollte. Falls unbekannt, sollten Details zur Proxykonfiguration beim lokalen Netzwerkadministrator in Erfahrung gebracht werden können. 

Für alle Microservices, die eingesetzt werden sollen, gilt, dass potentiell weitere Anpassungen vorgenommen werden können. Somit wird sichergestellt, dass das System auch wirklich die Services aufsetzt, welche der Nutzer einsetzen möchte.

In den Ordnern der verschiedenen Services sind hierfür wieder "example"-Dateien enthalten, genauer "values.yaml.example", welche wie oben beschrieben umbenannt werden müssen. Innerhalb der Dateien können nun die entsprechenden Daten für die Services lokal angepasst werden, falls das nötig ist. 

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Sobald diese Anpassungen getätigt wurden, kann der Cluster installiert werden.

Falls die Kommunikation zwischen Plugins und Cluster durch eine HTTPS-Verbindung abgesichert werden soll, was dringend empfohlen wird, so kann mittels des Shellskriptes [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) ein entsprechendes Zertifikat erstellt und als Secret hinterlegt werden. Das Skript muss dahingehend angepasst werden, für welche Domain das Zertifikat ausgestellt werden soll.
