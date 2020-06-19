---
title: Documentation
subtitle: How to contribute to documentation.

menu:
  doc:
    parent: contrib

mermaid: true
weight: 10005
---

In the [/docs](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/docs) folder in the main Git repository directory, you'll find all the source code for the website you're currently viewing. The source code is processed by the [Hugo](https://gohugo.io/getting-started/installing/) program inside the Gitlab CI pipeline. A new folder named *public* is created and moved to the web server. This means that it is very easy to make changes to the documentation.

All that is required is to create a new [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) with the necessary changes. Once the changes have been viewed and accepted, they will be available on the website.

The */docs/content/doc* folder contains all the pages in [Markdown](https://gohugo.io/content-management/formats/#learn-markdown) that constitute the technical documentation, which includes [the current file here](https://github.com/Sciebo-RDS/Sciebo-RDS/tree/master/docs/content/doc/contribute/documentation.de.md). 

In the other folders under */docs/content/content* news or articles (*/docs/content/post*), as well as various pages (*/docs/content/page*) outside the technical documentation can be created and edited.

Hugo offers many conveniences for creation and formatting. Further functions are also available through the [Theme](https://jimmyjames.github.io/justdocs/home/) used. Especially the callouts are especially helpful for the creation of clear texts.

You can view your changes locally with an installed Hugo application. The following command starts a server at [http://localhost:1313](http://localhost:1313):

```bash
hugo server
```
