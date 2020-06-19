---
title: Dokumentation
subtitle: Wie Du an der Dokumentation teilhaben kannst.

menu:
  doc:
    parent: contrib

mermaid: true
weight: 10005
---

Die Dokumentation kann auf zwei Wegen bearbeitet werden. Die Online Variante wird empfohlen, da hier keine Installation von Applikationen wie Git oder Hugo notwendig sind.

## Online

Github bietet die Möglichkeit die Dateien, welche sich im Repositorium von Git befinden, direkt zu bearbeiten. Dies ist ausführlich in deren [Dokumentation beschrieben](https://help.github.com/en/github/managing-files-in-a-repository/editing-files-in-your-repository). Dafür sind keinerlei Applikationen außer einem Browser notwendig. Navigiere dafür in den [Dokumentationsordner im RDS Repositorium](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/docs).

{{<callout "info">}}
Achte darauf, dass Du beim Speichern einen neuen *Pull Request* erstellst bzw. den richtigen Zweig (Branch) auswählst, damit deine Änderungen auch gesichtet und von den Entwicklern eingepflegt werden können. Solange kein Pull Request vorhanden ist, können deine Änderungen nicht übernommen werden.
{{</callout>}}

## Offline

Im Ordner [/docs](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/docs) im Hauptverzeichnis des Git Repositoriums findest Du den gesamten Quelltext zu der Webseite, die Du gerade betrachtest. Der Quelltext wird durch das Programm [Hugo](https://gohugo.io/getting-started/installing/) innerhalb der Gitlab-CI Pipeline verarbeitet. Anschließend existiert ein neuer Ordner namens *public*, welches auf den Webserver verschoben wird. Dies bedeutet, dass es sehr einfach ist, Änderungen an der Dokumentation durchzuführen.

Dafür wird nur ein neuer [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) mit den notwendigen Änderungen erstellt. Sobald die Änderungen gesichtet und akzeptiert wurden, sind sie auf der Webseite verfügbar.

Im Ordner */docs/content/doc* sind alle Seiten in [Markdown](https://gohugo.io/content-management/formats/#learn-markdown) gespeichert, welche die technische Dokumentation darstellen, zu der auch [die aktuelle Datei hier](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/docs/content/doc/contribute/documentation.de.md) gehört. 

In den anderen Ordnern unter */docs/content* können Neuigkeiten oder Artikel (*/docs/content/post*), sowie verschiedene Seiten (*/docs/content/page*) außerhalb der technischen Dokumentation erstellt und bearbeitet werden.

Hugo bietet bei der Erstellung und Formatierung viele Annehmlichkeiten an. Weitere Funktionen sind außerdem durch das verwendete [Theme](https://jimmyjames.github.io/justdocs/home/) verfügbar. Vor allem die Callouts sind besonders hilfreich bei der Erstellung übersichtlicher Texte.

Deine Veränderungen kannst Du lokal mit einer installierten Hugo-Applikation ansehen. Der folgende Befehl startet einen Server unter [http://localhost:1313](http://localhost:1313):

```bash
hugo server
```
