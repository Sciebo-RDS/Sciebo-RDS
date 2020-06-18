---
title: Kontextabgrenzung
subtitle: Architecture documentation with Arc42

menu:
  doc:

    parent: architecture

weight: 403
mermaid: false
---

## Kontextabgrenzung

### Fachlicher Kontext

Bei der folgenden Abbildung handelt es sich um eine Abgrenzung des zu erstellenden Sciebo RDS Systems zu allen verwendeten Services. Gleichzeitig wird ein erster Hinweis auf die Kommunikationsdaten gegeben. Anschließend folgt eine Tabelle zur besseren Erläuterung von verwendeten Begriffen innerhalb des Bildes. Hierbei handelt es sich explizit nicht um eine Erläuterung des zu erzeugenden Systems, sondern dessen Einbettung in bestehende Services.

Bei der Darstellung handelt es sich um ein UML-Diagramm. Bei der fachlichen Abgrenzung sollen allerdings Datenströme und -Flüsse dargestellt werden, sodass zur Vereinfachung die Pfeile die "Fließrichtung" der Daten darstellt. Die Deklarierung der Pfeile mit `<<flow>>` wurde für die bessere Lesbarkeit weggelassen.

| Element          | Bedeutung                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| User             | Fasst sämtliche Arten von Benutzern zusammen, u.a. Studierende, Forschende und Administrierende                              |
| DMP              | Kurzform für Datenmanagementpläne, dokumentiert den Umgang mit Forschungsdaten seitens der Nutzer.                           |
| Veröffentlichung | Fasst sämtliche Arten von Veröffentlichungen und Archivierung von Forschungsdaten zusammen.                                  |
| Pfeilrichtung    | Dokumentiert den Datenfluss                                                                                                  |
| ?                | Noch zu dokumentieren (TODO)                                                                                                 |
| Authenticator    | Authentifiziert den Nutzer gegenüber einem System, in diesem Fall Sciebo.                                                    |
| uni-internal     | Dies sind Webdienste, welche innerhalb der WWU betrieben werden.                                                             |
| uni-external     | Dies sind Webdienste, welche außerhalb der WWU (und damit außerhalb der Zuständigkeit) betrieben werden. *Datenschutzrisiko* |

![umfangreiche Kontextabgrenzung via UMLet](/images/kontextabgrenzung_umfeld.svg)

#### Beschreibung der externen Schnittstellen

| Service       | Beschreibung                                                           |
| ------------- | ---------------------------------------------------------------------- |
| CLARIN        | European Research Infrastructure for Language Resources and Technology |
| ePIC          | Consortium for Persistent Identifiers in the context of eScience       |
| Zenodo        | Open Science Repository entwickelt durch das CERN                      |
| Rosetta       | Archivierungssoftware und -dienst des Landes NRW                       |
| RD-Repository | Forschungsdatenrepository                                              |
| arXiv.org     | Ein öffentlicher Dokumentenserver der naturwissenschaftlichen Fächer   |

### Technischer Kontext

In folgender Abbildung ist die Kontextabgrenzung dargestellt mit den jeweils verwendeten Protokollen. Auffällig hierbei ist die ausschließlche Nutzung von HTTPS und REST. Dies liegt daran, dass im Auftragsdokument dies bereits so festgelegt wurde.

![umfangreiche technische Kontextabgrenzung](/images/kontextabgrenzung_umfeld_technisch.svg)

**\<optional: Erläuterung der externen technischen Schnittstellen\>**

**\<Mapping fachliche auf technische Schnittstellen\>**

## Lösungsstrategie {#section-solution-strategy}

| ID   | Aufgabe                                    | Lösungsansatz                                                                                                                                       |
| ---- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| L-1  | Nachhaltige Architektur                    | Ein Microservice-Ansatz wird bereits bestehende und neue Services miteinander verbinden.                                                            |
| L-2  | asynchrone Kommunikation zwischen Services | Ein Messaging-System kann die Gewährleistung des Nachrichtenversand für Aufgaben übernehmen.                                                        |
| L-3  | geringer Aufwand für neue Features         | Es wird die [Clean Architecture](/de/doc/arc42/contextboundary/#section-solid-arch) mit Microservices implementiert.                                |
| L-4  | Datenerhebung durch Plugins                | Die Integration von RDS in verschiedenen Plattformen wird mit dem jeweils vorhanden Pluginsystem realisiert.                                        |
| L-5  | Flexibilität der Software                  | Die Clean Architecture erlaubt es, dass ein Problem jeweils mit dem dafür besten Technologiestack unabhängig von anderen Stacks gelöst werden kann. |
| L-6  | Wartbarkeit, Skalierbarkeit                | Es werden beim Deployment auf Docker und Kubernetes und Gitlab als Integrations-, Test- und Deploymentpipeline gesetzt.                             |
| L-7  | Authentifizierung und Authorisierung       | Die Architektur verwendet OAuth2 als Mechanik, um die Aufgaben legitim gegenüber Sciebo oder anderen Diensten durchzuführen.                        |
| L-8  | verschlüsselte Kommunikation               | Die externe Kommunikation (z. B. zu REST-API) geschieht grundsätzlich über HTTPS / SSL.                                                             |
| L-9  | RB-9                                       | Reverse Proxy und Caching-Server als Frontend-Server zur Auslieferung von HTML, CSS und JavaScript und Annahme von API-Anfragen.                    |
| L-10 | Datenspeicherung                           | Grundsätzlich sind Microservices sind Stateless. Falls notwendig, werden Daten im Cloudspeicher in Schicht 3 der Clean Architecture abgelegt.       |

## Szenarien

| Qualitätsmerkmal                          | Szenario                      | Maßnahmen                                                                                                            |
| ----------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| L-3                                       | neues Feature implementieren. | Clean Architecture ermöglicht Verknüpfung von Diensten und schnelle Implementierung von neuen Features.              |
| Integration von RDS in bestehende Systeme | RDS in Dienst integrieren.    | API-Endpunkte und ein Sicherheitssystem werden angeboten. Integration mit plattformspezifischen Eigenheiten mgölich. |

### Clean Architecture {#section-solid-arch}

Die [SOLID-Prinzipien](https://de.wikipedia.org/wiki/Prinzipien_objektorientierten_Designs#SOLID-Prinzipien) sind in der (Enterprise) Softwareentwicklung bereits mit Erfolg angewendet worden und ist in der Praxis für [seine hohe Wartbarkeit und Agilität](https://www.informatik-aktuell.de/entwicklung/methoden/solid-die-5-prinzipien-fuer-objektorientiertes-softwaredesign.html) bekannt.

Weitergedacht auf eine Architektur hat dies bereits 2012 der Autor [Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), bezeichnet dies jedoch als *Clean Architecture* und beschreibt dies ausführlich in seinem gleichnamigen Buch. Da die Architektur lediglich ein Konzept beschreibt, wie ein System aufgebaut werden kann und das Konzept der Microservices als ein Deployment-Konzept angesehen ist, können diese beiden Konzepte kombiniert werden. Darüber hat auch [Martin ebenfalls geschrieben](https://blog.cleancoder.com/uncle-bob/2014/10/01/CleanMicroserviceArchitecture.html), man sollte jedoch seiner Meinung nach erforschen, welche Vor- und Nachteile man dadurch erhält und die Architektur auch ohne Microservices funktionieren können soll und muss.

{{<callout info>}}
Um diese Dokumentation nicht weiter zu verlängern, sei hier ausdrücklich auf die Links im vorangegangen Abschnitt verwiesen. Andernfalls ab hier angenommen, dass das Konzept der Clean Architecture beim Leser verstanden wurde.
{{</callout>}}

Vor allem sollte hier das Konzept der Schichten genannt werden und das der Abhängigkeiten.

![Clean Architecture](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg)
Quelle: https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg

Das Servicesystem in RDS ist auf Grundlage dieser Konzepte aufgebaut worden und ist als Diagramm im [Service Ökosystem](/de/doc/impl/infrastructure/ecosystem/) in dieser Dokumentation abgebildet.

Dabei werden...
-  in der äußersten Schicht die Services zugezählt, welche externe und interne Dienste an RDS anbindet. Aus diesem Grund werden die Container in dieser Schicht *Ports* genannt.
- in der mittleren Schicht enthält die Services, welche Features implementieren. Aus diesem Grund werden die Container hier *Use Cases* bezeichnet.
- in der innersten Schicht Services zusammengefasst, welche Informationen abspeichern oder so essentiell für das gesamte System sind, dass sie nicht weggelassen werden können. Hier werden die Container als *Central* benannt.

In der Linkübersicht dieser Dokumentation ist diese Aufteilung der Microservices wiederzufinden.

### Konzept der Integration

Grundsätzlich wird die Integration der RDS Applikation durch das plattformspezifische Pluginsystem vorgenommen.

Aufgrund der diversen Landschaft der Software, muss RDS eine möglichst hohe Integrationsvielfalt bereitstellen. Aus diesem Grund wurde die Entscheidung getroffen, diese Verantwortung an die Zielplattform abzugeben: Es muss ein Pluginsystem geben, welches die Integration von Third-Party-Applications erlaubt. Aus diesem Grund implementiert RDS lediglich API-Endpunkte und stellt diese zur Weiterverwendung bereit. Als erste Zielplattform wurde Owncloud gewählt. Weitere Integrationen sind möglich, müssen sich aber an das Oauth2-Konzept halten.

RDS nutzt den ersten Token, welchen er für einen Nutzer einer Integrationsplattform erhält als Haupttoken, sodass alle anschließend hinzugefügten Tokens, welche demselben Nutzer und Integrationsplattform zugeordnet werden, als verbundene Dienste interpretiert werden und dem Nutzer zur Auswahl angeboten werden. Daraus folgert sich auch die Nutzung von eindeutigen Nutzernamen oder IDs für jeweils eine Integrationsplattform. Es kann zwar mehrfach dieselbe Nutzername oder ID in RDS vorkommen, aber muss eindeutig mit der Integrationsplatform als Information zugeordnet werden können. 

Aus diesem Grund ist es auch leicht möglich, neue Integrationen durch andere Plattformen zu implementieren, da der neue Dienst Oauth2 anbieten muss und dem Nutzer selbst die Möglichkeit geben muss sich gegenüber RDS mit diesem zu authorisieren. Anschließend können alle durch RDS angebundenen Dienste dem Nutzer zur Auswahl gegeben und authorisiert werden, sodass RDS sich diesen gegenüber im Namen des Nutzer authorisieren kann. Dafür bietet RDS viele verschiedene API-Endpunkte, damit die Integration sich lediglich auf das Anzeigen und Absenden von Anfragen konzentrieren kann und nicht mehr auf die Implementierung von komplexen Algorithmen.

### Sicherheitskonzept

Aktuell wird das Sicherheitskonzept überarbeitet ([Siehe Issue 12](https://github.com/Sciebo-RDS/Sciebo-RDS/issues/12)). Daher wird dieser Abschnitt noch einmal überarbeitet.
