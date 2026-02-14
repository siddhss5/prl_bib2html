---
title: "Publications"
permalink: /publications/
layout: single
classes: wide
---

{% assign pubs = site.data.lab.publications %}
{% assign years = pubs | map: "year" | uniq | sort | reverse %}

{% for year in years %}
## {{ year }}

{% assign year_pubs = pubs | where: "year", year %}
{% assign categories = year_pubs | map: "category" | uniq %}

{% for category in categories %}
### {{ category }}

{% assign cat_pubs = year_pubs | where: "category", category %}
{% for pub in cat_pubs %}
{% include publication.html pub=pub %}
{% endfor %}

{% endfor %}
{% endfor %}
