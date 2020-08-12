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

Darin sind sämtliche Dateien enthalten, welche zur Konfiguration und Installation benötigt werden.

{{<callout info>}}
Die Helm Charts können im [Repositorium](https://github.com/Sciebo-RDS/charts) eingesehen werden.
{{</callout>}}

## Configuration

Um die Installation anzupassen, sind mehrere Dateien anzupassen. Dafür liegen im `deploy` Ordner mehrere `.example` Dateien, welche kopiert und umbenannt werden sollen und anschließend ggfs. inhaltlich anzupassen sind.

```bash
cp configuration.yaml.example configuration.yaml
nano configuration.yaml
```

In der `configuration.yaml` werden u.a. die Proxies definiert, welche möglicherweise in der Umgebung notwendig sind. Dadurch können die Microservices auch außerhalb des Clusters verfügbare Services erreichen, falls der Cluster keine eigene weltweite IP besitzen sollte. Falls unbekannt, sollten Details zur Proxykonfiguration beim lokalen Netzwerkadministrator in Erfahrung gebracht werden können. 

Für alle Microservices, die eingesetzt werden sollen, gilt, dass potentiell weitere Anpassungen vorgenommen werden können und müssen. Falls die Standardwerte für den Einsatz ausreichen, so sind keine Änderungen notwendig, außer in den Konnektorendiensten. Um Werte abzuändern, ist eine `values.yaml` Datei notwendig. Um alle verfügbaren Parameter einzusehen, ist ein Blick in das [Helm Chart Repo](https://github.com/Sciebo-RDS/charts/tree/master/charts) empfohlen.

Da die Konnektorendienste zusätzliche Informationen zur OAuth-Authentifizierung benötigt wie die ID und das Secret, benötigen diese eine values.yaml Datei. 
Im `deploy` Ordner ist wieder eine `example`-Datei vorhanden, genauer `values.yaml.example`, welche wie oben beschrieben umbenannt werden müssen. Innerhalb der Datei können nun die entsprechenden Daten für die Services lokal angepasst werden, falls das nötig ist. 

```bash
cp values.yaml.example values.yaml
nano values.yaml
```

Sobald die Anpassungen getätigt wurden, kann das System installiert werden.


### Namespace

Es wird empfohlen einen eigenen [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) für RDS im Kubernetes-Cluster zu erzeugen (z.B. *research-data-services*).

{{<callout warning>}}
If you do not follow the commands in this section, all commands must be completed respectively and the tools provided in what follows cannot be used straightforwardly. So you need to adjust all commands in the makefile to your needs or execute them manually and at your chosen namespace per hand.
Falls die folgenden Anweisungen nicht ausgeführt werden, 
{{</callout>}}

If you want to create a namespace, rename the file `namespace.yaml.example` to `namespace.yaml` and apply it. You can use the following commands to do this.

Um einen Namespace zu erstellen, sollte die Datei `namespace.yaml.example` in `namespace.yaml` umbenannt werden. Die darin enthaltenen Informationen können mit dem folgenden Befehlen angewendet werden.

{{<tabs>}}
{{<tab "bash" "Apply namespace">}}cp namespace.yaml.example namespace.yaml
nano namespace.yaml
make install_namespace
kubectl config set-context --current --namespace=$(sed -n 's/name: \(.*\)/\1/p' < namespace.yaml | head -n 1)
{{</tab>}}

{{<tab "bash" "Remove namespace">}}kubectl config set-context --current --namespace=default
make uninstall_namespace
{{</tab>}}
{{</tabs>}}

Anschließend wird das Angeben eines Kontexts für jeden Aufruf des Kubectl-Befehls (auch: Helm) obsolet, da der angegebene Namespace als Default verwendet wird. Ist dies nicht gewünscht, müssen sämtliche Befehle entsprechend ergänzt werden und die im Folgenden zur Verfügung gestellten Hilfsmittel können nicht ohne Weiteres verwendet werden.

### Verschlüsselung

Falls die Kommunikation zwischen Plugins und Cluster durch eine HTTPS-Verbindung abgesichert werden soll, was dringend empfohlen wird, so kann mittels des Shellskriptes [create_certs.sh](https://github.com/Sciebo-RDS/Sciebo-RDS/blob/master/deploy/create_certs.sh) ein entsprechendes Zertifikat erstellt und als Secret hinterlegt werden. Das Skript muss dahingehend angepasst werden, für welche Domain das Zertifikat ausgestellt werden soll.

Mit dem folgenden Befehlen können die benötigten Zertifikate erstellt und verwendet weden.

{{<tabs>}}
{{<tab "bash" "Create and apply ssl cert">}}cp create_cert.sh.example create_cert.sh
nano create_cert.sh
make install_tls
{{</tab>}}

{{<tab "bash" "Delete ssl cert">}}make uninstall_tls
{{</tab>}}
{{</tabs>}}

{{<callout info>}}
Ein bereits existierende Zertifikat sollte als `Secret` unter dem Namen `sciebords-tls-public` gespeichert werden. Das Skript `create_cert.sh` bietet hier ein Beispiel.
Falls ein anderer Name verwendet werden soll, kann der Name in der Datei `values.yaml` unter `global.ingress.tls.secretName` angegeben werden, sodass RDS dieses `Secret` nach einem Neustart verwendet.
{{</callout>}}

## Konfiguration anwenden

Sofern die vorherigen Schritte vollständig ausgeführt wurden, kann nun die Konfiguration auf den Cluster angewendet werden.

{{<tabs>}}
{{<tab "bash" "Apply configuration">}}make install_configuration
{{</tab>}}

{{<tab "bash" "Undoing configuration">}}make uninstall_configuration
{{</tab>}}
{{</tabs>}}