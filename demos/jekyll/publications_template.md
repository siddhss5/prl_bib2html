---
title: "Publications"
permalink: /publications/
layout: single
classes: wide
header:
  overlay_image: /assets/images/ADA-strawberry.jpg
---

{% assign total_pubs = 0 %}
{% for year_data in site.data.publications %}
  {% for category_data in year_data[1] %}
    {% assign total_pubs = total_pubs | plus: category_data[1].size %}
  {% endfor %}
{% endfor %}

<p class="notice--info">
  <strong>{{ total_pubs }} publications</strong> • 
  For analytics and citations, visit my <a href="http://scholar.google.com/citations?hl=en&user=RCi98EAAAAAJ">Google Scholar page</a> • 
  BiBTeX available on <a href="https://github.com/personalrobotics/pubs">GitHub</a>
</p>

{% for year_data in site.data.publications %}
  {% assign year = year_data[0] %}
  {% assign categories = year_data[1] %}

## {{ year }}

  {% for category_data in categories %}
    {% assign category = category_data[0] %}
    {% assign publications = category_data[1] %}

### {{ category }}

    {% for pub in publications %}
<div class="publication-entry" style="margin-bottom: 1.5em;">

  <div class="publication-title" style="margin-bottom: 0.3em;">
    {% if pub.pdf_url %}
  <a href="{{ pub.pdf_url }}"><strong>{{ pub.title }}</strong></a>
    {% else %}
  <strong>{{ pub.title }}</strong>
    {% endif %}
  </div>

  <div class="publication-authors" style="color: #666; margin-bottom: 0.3em;">
    {{ pub.authors }}
  </div>

  <div class="publication-venue" style="margin-bottom: 0.3em;">
    {{ pub.venue }}
    {% if pub.note %}
    <br><strong>{{ pub.note }}</strong>
    {% endif %}
  </div>

  {% if pub.projects.size > 0 %}
  <div class="publication-projects">
    {% for project in pub.projects %}
      {% if site.data.projects[project] %}
    <a href="/projects/#{{ project }}" class="btn btn--info btn--small" style="margin: 0.1em;">{{ project }}</a>
      {% endif %}
    {% endfor %}
  </div>
  {% endif %}

</div>
    {% endfor %}

  {% endfor %}
{% endfor %}

