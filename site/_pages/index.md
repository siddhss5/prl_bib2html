---
title: "Home"
permalink: /
layout: single
classes: wide
---

{% assign pubs = site.data.lab.publications %}
{% assign people = site.data.lab.people %}
{% assign current = people | where: "status", "current" %}
{% assign alumni = people | where: "status", "alumni" %}
{% assign projects = site.data.lab.projects %}

<div style="margin-bottom: 2em; font-size: 1.05em;">
This site is generated automatically from BibTeX files using <a href="https://github.com/siddhss5/prl_bib2html">labdata</a>.
It showcases <strong>{{ pubs.size }}</strong> publications, <strong>{{ current.size }}</strong> current members, <strong>{{ alumni.size }}</strong> alumni, and <strong>{{ projects.size }}</strong> research projects.
</div>

## Browse

- [**Publications**](/publications/) — Full list of papers with search, abstracts, and BibTeX
- [**People**](/people/) — Current members, alumni, and collaborators
- [**Projects**](/projects/) — Research projects with linked publications

---

## Recent Publications

{% assign recent = pubs | slice: 0, 10 %}
{% for pub in recent %}
{% include publication.html pub=pub %}
{% endfor %}

[View all {{ pubs.size }} publications &rarr;](/publications/)
