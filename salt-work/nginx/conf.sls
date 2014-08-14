{% set nginx_user = 'nginx' + ' ' + 'nginx' %}
include:
  - nginx.install

nginx_conf:
  file.managed:
    - name: /data/nginx/conf/nginx.conf
    - source: salt://nginx/files/nginx.conf
    - template: jinja
    - defaults:
      nginx_user: {{ nginx_user }}
      nginx_cpus: {{grains['num_cpus']}}
nginx_service:
  file.managed:
    - name: /etc/init.d/nginx
    - source: salt://nginx/files/nginx.init
    - user: root
    - mode: 755
  cmd.run:
    - names:
      - /sbin/chkconfig --add nginx
      - /sbin/chkconfig nginx on
    - unless: /sbin/chkconfig --list nginx
  service.running:
    - name: nginx
    - enable: True
    - reload: True
    - watch:
      - file: /data/nginx/conf/*.conf
	  -	file: /data/nginx/conf.d/*.conf