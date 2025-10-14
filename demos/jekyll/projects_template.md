---
title: "Projects"
permalink: /projects/
layout: single
classes: wide
header:
  overlay_image: /assets/images/herb-interlocked.jpeg
---

Research organized by project.

{% for project_data in site.data.projects %}
  {% assign project_name = project_data[0] %}
  {% assign project = project_data[1] %}

<div id="{{ project_name }}" class="project-section" style="margin-top: 2em; padding-top: 1em; border-top: 1px solid #e0e0e0;">

## {{ project.title }}

  {% if project.status or project.website %}
<div style="margin-bottom: 1em;">
    {% if project.status %}
      {% if project.status == "active" %}
  <span class="btn btn--success btn--small">{{ project.status | capitalize }}</span>
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

  {% if project.publications.size > 0 %}

### Publications

    {% for pub in project.publications %}
<div class="publication-entry" style="margin-bottom: 1.2em; padding-left: 0.5em;">

  <div class="publication-title" style="margin-bottom: 0.2em;">
    {% if pub.pdf_url %}
  <a href="{{ pub.pdf_url }}">{{ pub.title }}</a>
    {% else %}
  {{ pub.title }}
    {% endif %}
  </div>

  <div class="publication-meta" style="font-size: 0.9em; color: #666;">
    {{ pub.authors }} — {{ pub.venue }}
    {% if pub.note %}
    <br><strong>{{ pub.note }}</strong>
    {% endif %}
  </div>

</div>
    {% endfor %}

  {% endif %}

</div>

{% endfor %}

