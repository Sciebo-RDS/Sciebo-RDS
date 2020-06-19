---
title: Einführung
subtitle: Architecture documentation with Arc42

menu:
  doc:
    parent: architecture
weight: 401
---

## Einführung und Ziele

Die nachfolgende Dokumentation der Architektur zu den *sciebo Research Data Services* wird federführend von Peter Heiss (peter.heiss@uni-muenster.de) erstellt und gepflegt. Zuallererst soll die Kernaufgabe des Systems genannt werden und anschließend eine ausführliche Aufgabenstellung erläutert werden.

### Kernaufgabe

Das System bietet Brückenfunktionalitäten zu bereits bestehenden Forschungsdaten-Services und unterstützt den Forschenden bei der Arbeit in Sciebo bei seinem Forschungsdatenmanagement von der Projektentwicklung bis hin zur Publikation und Archivierung. Die wichtigsten Aspekte dabei sind die niederschwelligen Dienste, Wiederverwendung von bestehenden Diensten, die Integration des Systems in Sciebo und die User Experience.

### Aufgabenstellung

Die Antragsdokumente zu diesem Projekt für die DFG beschreiben viele der Aufgabenstellungen sehr ausführlich. Sie sind im **sciebo RDS**-spezifischen Ordner in Sciebo unter `sciebo RDS/Dokumente-DFG/DFG-Antrag_sciebo_RDS_final.pdf` zu finden. Im Folgenden sind diese auf das Wesentliche zusammengefasst.

| ID  | Anforderung                         | Erklärung                                                                                                                           |
| --- | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| M-1 | Integration in Sciebo               | Forschende sind bereits mit Sciebo vertraut.                                                                                        |
| M-2 | Niederschwellige Dienste            | Eine einfache Handhabung garantiert auch langfristige Nutzung.                                                                      |
| M-3 | bietet Brückenfunktionalitäten      | Bereits bestehende Services werden durch Brückenfunktionalitäten verbunden.                                                         |
| M-4 | Integration von externen Services   | Es wird vermieden neue Entwicklungen anzustoßen, durch die Nachnutzung von bereits bestehenden Services und Infrastrukturen.        |
| M-5 | adaptiert externe Expertenwerkzeuge | Die Tools der Forschenden sollen bei den Brückenfunktionalitäten integriert werden.                                                 |
| M-6 | bietet grundlegendes FDM            | Dafür werden Funktionalitäten für die Erschließung von Forschungsdaten entwickelt.                                                  |
| M-7 | durchgehende Arbeitsweisen          | Das FDM wird von der Projektentwicklung über die operative Arbeit bis hin zur Publikation und Archivierung durchgehend unterstützt. |

Legende: M = Muss, O = Optional

Die folgende Abbildung ist eine symbolische Einordnung der zu erzeugenden Softwarearchitektur in die vorhandenen internen und externen Services.

![Anforderungscluster](/images/anforderungscluster.svg)

Eine genaue Auflistung sämtlicher anzubindenen Services und Repositorien ist im Antrag auf S. 15 zu finden.

### Qualitätsziele

In der folgenden Tabelle werden Ziele und Anforderungen genannt, welche für Stakeholder bei der Bedienung und der User Experience der Services dienlich sein sollen.

| ID  | Prio  | Qualitätsziel | Erläuterung                                                                                                                                          |
| --- | :---: | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q-1 |   2   | Performance   | Das System verarbeitet die Anfragen der Nutzer möglichst instantan oder asynchron, sodass die Nutzer keine Verzögerung in ihrem Arbeitsablauf haben. |
| Q-2 |   1   | Flexibilität  | Neue Funktionen lassen sich ohne großen Aufwand hinzufügen. Neue Services lassen sich anbinden.                                                      |
| Q-3 |   1   | Sicherheit    | Die Nutzerdaten werden bei der Verarbeitung nicht verändert, Datenschutz wird berücksichtigt. Nutzerdaten bleiben Eigentum des Nutzers.              |
| Q-4 |   2   | Korrektheit   | Die Nutzerführung und Verständigung der Funktionalitäten ist für nicht technikaffine Fachbereiche nachvollziehbar und entspricht den Erwartungen.    |
| Q-5 |   3   | Durchgehend   | Die Nutzerführung hat einen durchgehend sinnvollen Arbeitsablauf bzw. können die Nutzer einen eigenen Ablauf verwenden.                              |
| Q-6 |   3   | Transparenz   | Die Verarbeitung von Daten ist transparent gestaltet und die Software als Open-Source zur Verfügung gestellt.                                        |
| Q-7 |   1   | Monitoring    | Sämtliche Services und Aufträge sowie deren Status können jederzeit eingesehen werden.                                                               |

Legende: Prioritätenskala 1 (besonders wertvoll) bis 4 (wird angestrebt)

(TODO) Szenarien hinzufügen (siehe Szenarien.pdf und S. 43 von Eff. Arch. von Starke)

### Stakeholder

Eine komplette Liste aller Beteiligten ist im *sciebo RDS* Ordner zu finden unter `Organisatorisches/`zu finden in den Dateien `ORGA sciebo RDS.docx` und `Projekt scieboRDS Adressliste.docx`. Im Folgenden sollen lediglich Namen oder zur Einfachheit Gruppen genannt werden.

| Rolle              | Kontakt                       | Erwartungshaltung                                                                                                                    |
| ------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Abteilung: F&E     | Jörg Lorenz, Immanuel Normann | Informationen und Erfahrungen über Entwicklung und Deployment von Microservices werden Abteilungsübergreifend weitergegeben.         |
| Antragsstellende   | -                             | -                                                                                                                                    |
| Entwickelnde       | sciebo RDS                    | Neue Features können ohne große Seiteneffekte integriert werden. Dokumentation soll Architektur und Entscheidungen beschreiben.      |
| Forschende         | v.A. Forscher der Universität | (Aktuell durch UDE betrachtet.)                                                                                                      |
| Sciebo Betreibende | Holger Angenent               | Ein Mehrwert für die Nutzenden ist aus der Dokumentation erkennbar. Eine Kooperation zu CERN Mesh ist durch die Architektur möglich. |
| Sciebo Nutzer      | v.A. Studierende              | Bedienbarkeit von Sciebo nicht beeinflusst. Perspektivenwechsel von Nutzer zu Forschender muss möglich sein.                         |
| ULB Projektleitung | Holger Przibytzin             | Eine Übersicht und Beschreibung der Architektur zur Kommunikation der Projektführung.                                                |
