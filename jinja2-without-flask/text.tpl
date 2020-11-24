{% if data.truth %}
{{data.name}} had a little {{data.animal}}.
{% else %}
{{data.animal}} had a little {{data.name}}.
{% endif %}
{% for color in data.colors %}
    {{data.name}} had a little {{color}} {{data.animal}}
{% endfor %}
{% include 'hdr.tpl' %}
