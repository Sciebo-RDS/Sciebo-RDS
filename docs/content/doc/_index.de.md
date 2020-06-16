---
title: Dokumentation
subtitle: Alles was du wissen musst über die *Dokumentation*
weight: -999
---

## Arbeitsablauf

Wir benutzen Github als Ablage für den Quelltext. Als CI/CD Platform nutzen wir Gitlab und dessen eigene Runner, welche auch externen Personen zur Verfügung stehen durch eine Anbindung an das Github Repositorium.
Diese werden automatisiert verwendet und dessen definierte Aufgaben angestoßen, sobald eine relevante Codezeile geändert wird. Dabei entstehen in Folge von erfolgreichen Testfällen ein Container (aktuell verwenden wir dafür Docker), welche im Gitlab-internen Paketeordner abgelegt wird, sodass von dort aus Kubernetes die erzeugten Container herunterladen und verwenden kann. Diese Pakete sind öffentlich zugänglich.

In der hier vorliegenden Dokumentation wird die Funktionsweise und Konzepte mittels einer Arc42 Dokumentation, sowie die durch RDS implementierten Schnittstellen mittels OpenAPIv3 und definierten Bibliotheken mittels Funktionsdeklarationen und DocString übersichtlich beschrieben.
