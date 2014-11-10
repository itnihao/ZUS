{% set nginx_user = 'nobody' %}
nginx_conf:
  file.managed:
    - name: /usr/local/openresty/nginx/conf/nginx.conf
    - source: salt://fileserver/nginx.conf
    - template: jinja
    - defaults:
      nginx_user: {{ nginx_user }}
      num_cpus: {{ grains['num_cpus'] }}
