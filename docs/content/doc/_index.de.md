---
title: Dokumentation
subtitle: Alles was du wissen musst über die *Dokumentation*
weight: -999
---

## Arbeitsablauf

Wir benutzen Github als Ablage für den Quelltext. Als CI/CD Platform nutzen wir Gitlab und dessen eigene Runner, welche auch externen Personen zur Verfügung stehen durch eine Anbindung an das Github Repositorium.
Diese werden automatisiert verwendet und dessen definierte Aufgaben angestoßen, sobald eine relevante Codezeile geändert wird. Dabei entstehen in Folge von erfolgreichen Testfällen ein Container (aktuell verwenden wir dafür Docker), welche im Gitlab-internen Paketeordner abgelegt wird, sodass von dort aus Kubernetes die erzeugten Container herunterladen und verwenden kann. Diese Pakete sind öffentlich zugänglich.

In der hier vorliegenden Dokumentation wird die Funktionsweise und Konzepte mittels einer Arc42 Dokumentation, sowie die durch RDS implementierten Schnittstellen mittels OpenAPIv3 und definierten Bibliotheken mittels Funktionsdeklarationen und DocString übersichtlich beschrieben.

For a general understanding, what RDS is and what it does, you should read the following two chapters.

Um ein allgemeines Verständnis für das RDS System und dessen Funktionen zu bekommen, sollten die folgenden beiden Kapitel gelesen werden.

## Konzeptionierung

Die Projekt- und Zielbeschreibung befindet sich [hier](/de/page/about/) und sollten ebenfalls gelesen werden.
Das RDS System wurde als Middleware entwickelt, welche es einfach macht mit internen und externen Diensten zu kommunizieren innerhalb einer bereits existierenden Nutzerumgebung.

![RDS Core as middleware](/images/rds-overview-middleware.png)

Aktuell gibt es eine Schnittstelle zwischen Owncloud und Zenodo. Weitere Konnektoren sind in Vorbereitung.

## Erste Schritte

Das Nutzerhandbuch und viele Fragen befinden sich [hier](/de/doc/manual/faq/).

Für Administratoren befindet sich die [Installationsanleitung hier](/de/doc/getting-started/k8s/).

Die Arc42 Dokumentation, welche sich an Softwareentwickler wendet, befindet sich [hier](/de/doc/arc42/indroduction/). Anschließend empfiehlt sich noch die Lektüre der automatisch generierten Dokumentation aller Microservices, welche im RDS System zur Anwendung kommen.

Falls noch andere Fragen übrig bleiben und Probleme auftreten, können diese in unserem [Issue Tracker](https://github.com/Sciebo-RDS/Sciebo-RDS/issues) gestellt oder kommuniziert werden.