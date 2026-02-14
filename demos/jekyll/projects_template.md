---
title: "Projects"
permalink: /projects/
layout: single
classes: wide
---

{% assign projects = site.data.lab.projects %}
{% assign pubs = site.data.lab.publications %}

{% for project in projects %}
<div id="{{ project.id }}" style="margin-top: 2em; padding-top: 1em; border-top: 1px solid #e0e0e0;">

## {{ project.title }}

{% if project.status or project.website %}
<div style="margin-bottom: 1em;">
  {% if project.status %}
    {% if project.status == "active" %}
      <span class="btn btn--success btn--small">Active</span>
    {% else %}
      <span class="btn btn--secondary btn--small">{{ project.status | capitalize }}</span>
    {% endif %}
  {% endif %}
  {% if project.website %}
    <a href="{{ project.website }}" target="_blank" class="btn btn--primary btn--small">Website</a>
  {% endif %}
</div>
{% endif %}

{% if project.description %}
<p class="notice">{{ project.description }}</p>
{% endif %}

{% if project.publication_ids.size > 0 %}
### Publications

{% for pub_id in project.publication_ids %}
  {% assign pub = pubs | where: "bib_id", pub_id | first %}
  {% if pub %}
<div style="margin-bottom: 1.2em; padding-left: 0.5em;">
  <div style="margin-bottom: 0.2em;">
    {% if pub.pdf_url %}
      <a href="{{ pub.pdf_url }}">{{ pub.title }}</a>
    {% else %}
      {{ pub.title }}
    {% endif %}
  </div>
  <div style="font-size: 0.9em; color: #666;">
    {% for author in pub.authors %}{{ author.name }}{% unless forloop.last %}, {% endunless %}{% endfor %} — {{ pub.venue }}
    {% if pub.note %}<br><strong>{{ pub.note }}</strong>{% endif %}
  </div>
</div>
  {% endif %}
{% endfor %}
{% endif %}

</div>
{% endfor %}
