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
<div style="margin-bottom: 1.5em;">
  <div style="margin-bottom: 0.3em;">
    {% if pub.pdf_url %}
      <a href="{{ pub.pdf_url }}"><strong>{{ pub.title }}</strong></a>
    {% else %}
      <strong>{{ pub.title }}</strong>
    {% endif %}
  </div>
  <div style="color: #666; margin-bottom: 0.3em;">
    {% for author in pub.authors %}{{ author.name }}{% unless forloop.last %}, {% endunless %}{% endfor %}
  </div>
  <div style="margin-bottom: 0.3em;">
    {{ pub.venue }}
    {% if pub.note %}<br><strong>{{ pub.note }}</strong>{% endif %}
  </div>
  {% if pub.project_ids.size > 0 %}
  <div>
    {% for pid in pub.project_ids %}
      <a href="/projects/#{{ pid }}" class="btn btn--info btn--small" style="margin: 0.1em;">{{ pid }}</a>
    {% endfor %}
  </div>
  {% endif %}
</div>
{% endfor %}

{% endfor %}
{% endfor %}
