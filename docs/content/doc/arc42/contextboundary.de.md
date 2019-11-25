---
title: Kontextabgrenzung
subtitle: Architecture documentation with Arc42

menu:
  doc:
    parent: arch
weight: 203
---

## Kontextabgrenzung

### Fachlicher Kontext

Bei der folgenden Abbildung handelt es sich um eine Abgrenzung des zu erstellenden Sciebo RDS Systems zu allen verwendeten Services. Gleichzeitig wird ein erster Hinweis auf die Kommunikationsdaten gegeben. Anschließend folgt eine Tabelle zur besseren Erläuterung von verwendeten Begriffen innerhalb des Bildes. Hierbei handelt es sich explizit nicht um eine Erläuterung des zu erzeugenden Systems, sondern dessen Einbettung in bestehende Services.

Bei der Darstellung handelt es sich um ein UML-Diagramm. Bei der fachlichen Abgrenzung sollen allerdings Datenströme und -Flüsse dargestellt werden, sodass zur Vereinfachung die Pfeile die "Fließrichtung" der Daten darstellt. Die Deklarierung der Pfeile mit `<<flow>>` wurde für die bessere Lesbarkeit weggelassen.

![umfangreiche Kontextabgrenzung via UMLet](/images/kontextabgrenzung_umfeld.svg)

|     Element      |                                                          Bedeutung                                                           |
|------------------|------------------------------------------------------------------------------------------------------------------------------|
|       User       |               Fasst sämtliche Arten von Benutzern zusammen, u.a. Studierende, Forschende und Administrierende                |
|       DMP        |              Kurzform für Datenmanagementpläne, dokumentiert den Umgang mit Forschungsdaten seitens der Nutzer.              |
| Veröffentlichung |                 Fasst sämtliche Arten von Veröffentlichungen und Archivierung von Forschungsdaten zusammen.                  |
|  Pfeilrichtung   |                                                 Dokumentiert den Datenfluss                                                  |
|        ?         |                                                 Noch zu dokumentieren (TODO)                                                 |
|  Authenticator   |                          Authentifiziert den Nutzer gegenüber einem System, in diesem Fall Sciebo.                           |
|   uni-internal   |                               Dies sind Webdienste, welche innerhalb der WWU betrieben werden.                               |
|   uni-external   | Dies sind Webdienste, welche außerhalb der WWU (und damit außerhalb der Zuständigkeit) betrieben werden. *Datenschutzrisiko* |

#### Beschreibung der externen Schnittstellen

|    Service    |                              Beschreibung                              |
|---------------|------------------------------------------------------------------------|
|    CLARIN     | European Research Infrastructure for Language Resources and Technology |
|     ePIC      |    Consortium for Persistent Identifiers in the context of eScience    |
|    Zenodo     |           Open Science Repository entwickelt durch das CERN            |
|    Rosetta    |            Archivierungssoftware und -dienst des Landes NRW            |
| RD-Repository |                       Forschungsdatenrepository                        |
|   arXiv.org   |  Ein öffentlicher Dokumentenserver der naturwissenschaftlichen Fächer  |

### Technischer Kontext

In folgender Abbildung ist die Kontextabgrenzung dargestellt mit den jeweils verwendeten Protokollen. Auffällig hierbei ist die ausschließlche Nutzung von HTTPS und REST. Dies liegt daran, dass im Auftragsdokument dies bereits so festgelegt wurde.

![umfangreiche technische Kontextabgrenzung](/images/kontextabgrenzung_umfeld_technisch.svg)


**\<optional: Erläuterung der externen technischen Schnittstellen\>**

**\<Mapping fachliche auf technische Schnittstellen\>**

## Lösungsstrategie {#section-solution-strategy}

|  ID  |                  Aufgabe                   |                                                      Lösungsansatz                                                      |
|------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| L-1  |          Nachhaltige Architektur           |                Ein Microservice-Ansatz wird bereits bestehende und neue Services miteinander verbinden.                 |
| L-2  | asynchrone Kommunikation zwischen Services |                        Ein Messaging-System übernimmt die Gewährleistung des Nachrichtenversand.                        |
| L-3  |     geringer Aufwand für neue Features     |  Der Microservice-Ansatz fußt auf Self-Contained Systems, wodurch Frontend, Logik und Backend zusammen erzeugt werden.  |
| L-4  |          Datenerhebung trotz SCS           | Es wird ein Frontend-Server aufgesetzt, welcher die Frontends der Microservice sammelt, darstellt und Daten weitergibt. |
| L-5  |         Flexibilität der Software          |                  Durch die SCS kann jedes Problem durch einen eigenen Technologiestack gelöst werden.                   |
| L-6  |        Wartbarkeit, Skalierbarkeit         |  Es werden beim Deployment Docker und Kubernetes verwendet und Gitlab als Integrations-, Test- und Deploymentpipeline.  |
| L-7  |    Authentifizierung und Authorisierung    | Die Architektur verwendet OAuth2 als Mechanik, um die Aufgaben legitim gegenüber Sciebo oder anderen IDP durchzuführen. |
| L-8  |        verschlüsselte Kommunikation        |                  Die externe Kommunikation (z.B. zu REST-API) geschieht vorzugsweise über HTTPS / SSL.                  |
| L-9  |                    RB-9                    |           Reverse Proxy und Caching-Server als Frontend-Server zur Auslieferung von HTML, CSS und JavaScript.           |
| L-10 |              Datenspeicherung              |         Sämtliche Nachrichten sind Stateless. Falls dennoch notwendig, werden Daten im Cloudspeicher abgelegt.          |

| Q-Merkmal | Szenario | Maßnahmen |
|-----------|----------|-----------|
|           |          |           |

(TODO)

### Frontend-Server, Open-Host Service und Messaging-Systeme

Aufgrund der hohen Komplexität der Kommunikation zwischen Frontend-Server und Services bei L-4 und dessen zentrale Rolle für die gesamte Architektur, ist ein Grundverständnis für die Funktionsweise der Nachrichtenübermittlung für die weitere Arbeit mit der Architektur notwendig. Deshalb wird im Folgenden der Ansatz des Open-Host Services, des Frontend-Servers und des Messaging-Systems beschrieben. Dafür wird der Bausteinsicht, welche im nächsten Kapitel näher erläutert wird, vorausgegriffen werden mit einer reduzierten Blackboxdarstellung auf der ersten Ebene.

![Ein erster Blick der Kommunikation in der ersten Ebene der Bausteinsicht](/images/blackbox_ebene1.svg) (TODO)

Der Frontend-Server (hier als RDPM für *Research data project manager* bezeichnet) stellt die Schnittstelle zwischen Nutzer und System dar. Dabei kommt die Kommunikation vor allem durch die Microservices zustande, sodass das Frontend sich vor allem auf die Auslieferung und Verarbeitung von Daten konzentrieren kann. Dafür müssen vom RDPM entsprechende Schnittstellen als Open-Host-System zur Verfügung zu stellen.

Die Kommunikation zwischen den Microservices findet über eine LAN-Verbindung statt. Aufgrund der hohen Komplexität und der hohen Interoperabilität der angestrebten Architektur ist es notwendig, sich um mögliche Garantien wie Nachrichtenerhalt oder Nachrichtenwiederherstellung bei Hardwareausfall Gedanken zu machen. Aus diesem Grund wird ein weiteres System in die Architektur integriert: das *Messaging System* über welches sämtliche Kommunikation verläuft. Dies entspricht dem Lösungsansatz L-2. Das Messaging-System verfolgt ein Push-Pull-Prinzip bzw. ein [Pub-Sub-Messaging](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern).
Dieser Umstand wird auch im nächsten Bild dargestellt. Dabei wurden die angebundenen Services unter einem einzigen *Service* als Beispiel der Anbindung zusammengefasst. Zur Veranschaulichung für die Integration von generischen Microservices wurden drei verschiedene Microservices eingezeichnet.

![Blackbox Darstellung eines vereinfachten Gesamtsystems](/images/blackbox_ebene1_2.svg)

Vereinfacht ausgedrückt wird die Kommunikation zwischen Frontend-Server und Microservices lediglich um die Komponente des Messaging Systems erweitert. Die höhere Komplexität der Architektur erhöht die Stabilität und die genannten Garantien brauchen nicht mehr von jedem Microservice selbst implementiert zu werden. Dies reduziert die Fehleranfälligkeit bei der Kommunikation, da sich hier auf bestimmte Regeln wie ein Nachrichtenprotokoll bei der Serviceinitialisierung geeinigt wird.

Um die Kommunikation zwischen den entwickelnden Teams der jeweiligen Microservices nach L-1 auf ein Mindestmaß zu reduzieren, muss das Frontend-System durch die Microservices gesteuert werden können. Dafür wird eine Schnittstelle vom Frontend angeboten, einem sogenannten [Open-Host Service](http://ddd.fed.wiki.org/view/open-host-service). Diese nimmt Anfragen entgegen, welche das Verhalten des Servers ändern oder den Funktionsumfang entsprechend der gestellten Anfragen und der übermittelten Daten erweitern. Dieser Open-Host Service wird vor allem dann eingesetzt, wenn ein neuer Microservice an das Messaging-System angeschlossen wird.

Da es sich um ein Frontend-Server handelt, welcher vor allem auf moderne Technologien aufsetzt, werden bei der Initialisierung von einem Microservice vor allem HTML-Code, sowie API-Endpunkte benötigt, welche der Microservice nach außen hin anbieten soll. Die statischen Dateien wie HTML, JavaScript (kurz JS) oder CSS werden durch ein gemeinsames Git-Repo zur Verfügung gestellt, in dem die statischen Dateien der Microservices als Submodule eingebunden sind. Dieser Aufbau wird im kommenden Kapitel der [Bausteinsicht der Ebene 2](#frontendserver) mit technischen Details dargestellt. Die folgenden Annahmen liegen dieser Funktionalität zugrunde: die API-Endpoints sind zur Laufzeit unveränderlich und HTML-Dateien dürfen nur durch einen entsprechenden Git-Befehl wie `git pull` verändert werden.

Das folgende Schaubild veranschaulicht den Ablauf für einen einzigen Microservice exemplarisch am genannten Beispiel (im Kapitel [Laufzeitsicht](#laufzeitsicht) wird dies noch mit Sequenzdiagrammen ausführlicher beschrieben). Die Pfeile symbolisieren dabei die Flussrichtung der Daten und welchem Zweck diese dienen, wobei die Zahl zu Beginn der Beschreibung die Reihenfolge der Abarbeitung festlegt.

> *#FIXME Hinweis: Der folgende Ablauf ist nicht der aktuelle Zustand des Prototypen. Dieser sendet einfach sämtliche Anfragen an den Message Broker und gibt den HTTP-Code 201 (Created) zurück. Stellt man dieselbe Anfrage nocheinmal, so wird nachgeschaut, ob es bereits eine Antwort durch den Message Broker gab. Falls ja, wird die hinterlegte Antwort mit dem HTTP-Code 200 (OK), andernfalls der Code 202 (Accepted) gesendet. Dadurch können auch langwierige Aufgaben vollzogen und dessen Antwortstatus ermittelt werden. Der Microservice-Entwickler trägt dafür die Verantwortung mit den entsprechenden HTTP-Codes umzugehen und Anfragen gegebenenfalls durch seine JavaScript-Anwendung erneut zu senden. [Weitere Erklärungen zur Funktionsweise](https://farazdagi.com/2014/rest-and-long-running-jobs/)*

> *Dieses "Fehlverhalten" des Prototyps soll jedoch in Zukunft an den hier beschriebenen Abläufen angeglichen werden. Vor allem weil aktuell sämtliche Anfragen ohne Überprüfung bedient und weitergeleitet werden, sodass der Message Broker auch Anfragen erhält, welche von keinem Microservice bedient werden, sodass diese Anfragen ins Leere laufen und der Webserver stets HTTP-Code 201 senden wird, da er niemals eine Antwort erhalten wird. Dies ist nicht nur unter performance und technischer Sicht bedenklich. Für ein Szenario, indem ein Microservice sämtliche Anfragen erhalten möchte, sehe ich aktuell auch keine Anwendung, trotz dem dieses durch die hier geplanten Abläufe durch entsprechende Anpassungen der Frontend-Anwendung möglich sein wird. Die Vorgehensweise mit den HTTP-Codes wird allerdings übernommen werden und die Dokumentation, vor allem die Sequencediagramme, entsprechend angepasst.*

![Blackbox Darstellung eines vereinfachten Gesamtsystems bei der Initialisierung eines Microservices](/images/blackbox_initializing2.svg)

Das Absenden der Informationen über die Endpoints wird mittels einem wohldefinierten Schema über das Messaging-System versendet, sodass der Frontend-Server genau weiß, wie er damit umzugehen hat und die Nutzerinformationen an das Event-Thema weiterzuleiten hat, sodass jeder interessierte Microservice diese selbstständig herausfiltern kann und sie entsprechend bearbeiten kann. Natürlich hat vor allem der Microservice an diesen Informationen Interesse, welcher den Endpoint erzeugt hat. Durch die eventbasierte Architektur können aber auch alle anderen Services sich an diesen Informationen bedienen, wodurch schnellere Arbeitswege möglich werden.

Aufgrund des zu erwartenden hohen Durchsatzes von Events, müssen die Nachrichten sehr schnell und ressourceneffizient gefiltert werden können: Dies geschieht wieder mit den genannten Schemata, welche eine schnelle Filterung zulassen. Durch das Messaging-System ist es außerdem gewährleistet, dass gleiche Interessensgruppen keine Nachricht mehrfach erhalten, wodurch ein hoher Durchsatz und die vertikale Skalierbarkeit von Services garantiert werden kann.

Die verwendeten Kommunikationskanäle zwischen Frontend-Server und den Microservices können natürlich auch für die Kommunikation zwischen den Microservices selbst verwendet werden, wodurch ein hoher Datenaustausch auch zwischen diesen möglich ist. Vor allem das Prinzip des Events und des Schemas ermöglicht es auf Aktionen anderer Microservices zu reagieren ohne mit deren Entwicklerteam Rücksprache über ein einheitliches Protokoll halten zu müssen.

Eine weitere Besonderheit der Architektur ist der Abruf von Informationen mittels einer REST-API. Aufgrund der angestrebten hohen Skalierbarkeit kann eine naive Implementierung der API nicht zielführend sein. Aus diesem Grund bedient sich der hier verfolgte Ansatz einer asynchronen Alternative, welche u.a. auf [medium.com](https://medium.com/@grzegorzolechwierowicz/long-computations-over-rest-http-in-python-4569b1187e80) näher beschrieben wird. Das Ziel dabei ist es auf Verzögerungen (z.B. durch Netzwerklatenz oder hohe Nachfrage) skalierbar reagieren zu können. Das folgende Bild veranschaulicht einen möglichen Ablauf einer API-Abfrage.

![Ein GET-Request der API.](/images/api-callbacks.svg)

Die weiteren Request-Typen (POST, PUT, DELETE) unterscheiden sich lediglich in der fehlenden Abfrage im Cache, sodass auf die Antwort des Microservice gewartet wird, welcher die Anfrage bearbeitet. Dies verhindert, dass eine neue GET-Anfrage gestellt wird, bevor Daten im Microservice geändert werden, sodass der Nutzer z.B. nach seiner POST-Anfrage anschließend auch die neuen Informationen mit einer GET-Anfrage abfragen kann. Durch einen Cache-Server können häufig abgefragte Daten beschleunigt werden, da sich die Daten im Microservice außerhalb von Anfragen nicht ändern. Bei einer verändernden Anfrage wird der entsprechende Eintrag im Cache invalidiert und neu geladen.

![Eine verändernde Request (POST, PUT, DELETE, ...) der API.](/images/api-callbacks-changes.svg)

Mehr Informationen zu den Themen Frontend-Server, Open-Host-Service und Messaging-Systeme können im Buch *E. Wolff - Microservices* gefunden werden.