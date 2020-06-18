---
title: Kriterien
subtitle: Was dein Microservice bieten muss.

menu:
  doc:
    parent: contrib

mermaid: true
weight: 10007
---

## Definition of Done

Hier werden alle Eigenschaften aufgelistet, welche ein Microservice und dessen zugehörige Dateien erfüllen müssen, um akzeptiert und in das Ökosystem von RDS aufgenommen zu werden.

### Für einen Microservice existiert

- einen eigenen Ordner im (Mono-)Repo
- eine gitlab-ci-Datei, welche ein
    - Testen der nachfolgenden Anforderungen,
    - erfolgreiches Kompilieren und
    - Bauen eines Docker-Images ermöglicht.
        - Das Docker-Image wird in der Gitlab-Registry abgelegt
        - Das Docker-Image wird anhand des jeweiligen JobID anhand eines Tags markiert
        - Das Docker-Image wird im Master bei einem Merge zusätzlich anhand eines Tags als latest markiert
- eine funktionierende Kubernetes-Konfiguration in Form von Helm-Charts zum Deployen des Microservices in desselbigen
    - mit einer Ingress-,
    - einer Deployment- (mit einer Liveness- und/oder Readiness-Probe) und
    - einer Service-Konfiguration

### Für das Testen existiert

- für jede komplexere Funktion mindestens ein Unit-Test mit einem sprachenspezifischen Testframework (PHPUnit, JUnit, PyTest, Jest, etc), welcher folgende Fälle beinhaltet
    - eine Standardeingabe mit erwarteten Parametern
    - eine Null-Eingabe bei einem Parameter oder Null-Eingaben bei allen Parametern
    - für sämtliche Randfälle, welche beim Sprint Planning identifiziert und in der Implementation geprüft werden
- für jede extern anzubindende Funktion (meist fremde API-Endpunkte) ein Contract-Unit-Test mittels Pact
    - die dabei entstehende Pact-Datei wird im dafür entsprechenden Gitlab-Projekt automatisch abgelegt

### Für den Betrieb werden folgende Aspekte berücksichtigt:

- Der Microservice bietet Prometheus-typische Metriken über ein API-Endpunkt an
    - Zusätzliche Metriken wurden beim Sprint Planning entschieden und in einem entsprechenden Sprint Backlog festgehalten
- Die Dokumentation der Software ist mindestens für extern verfügbaren Funktionen (sind als public deklariert oder API-Endpunkte) vorhanden und beinhaltet
    - die API-Endpunkte sind durch OpenAPI v3 dokumentiert
    - Funktionen sind mittels DocString-Kommentare dokumentiert
        - eine Webseiten-Dokumentation nach etablierten Standard wird generiert und entsprechend der Projektstandards abgelegt
- Der Microservice nutzt die Opentracing-Technologie und greift entsprechende IDs auf und erstellt selbst eigene Spans und liefert diese zurück, sodass Jaeger diese erhalten und verarbeiten kann.

