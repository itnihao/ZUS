{% for vhostname in pillar['vhost'] %}
{{ vhostname['name'] }}:
  file.managed:
    - name: {{ vhostname['target'] }}
    - source: salt://fileserver/vhost.conf
    - template: jinja
    - defaults:
      server_name: {{ grains['fqdn_ipv4'][0] }}
      log_name: {{ vhostname['name'] }}
{% endfor %}
