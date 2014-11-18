nginx-install:
  pkg.installed:
    - name: nginx
    - require:
      - file: /etc/yum.repos.d/omnslm.repo

vhost-dir:
  file.directory:
    - name: /data/nginx/conf/vhosts
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

nginx-root-dir:
  file.directory:
    - name: /data/dazongshi/web/main
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

ssl-dir:
  file.directory:
    - name: /data/nginx/conf/ssl
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
    
cert-crt:
  file.managed:
    - name: /data/nginx/conf/ssl/certificate.crt
    - source: salt://fileserver/nginx/certificate.crt
    - user: nobody
    - group: nobody
    - mode: 644
    - require:
      - pkg: nginx-install

cert-key:
  file.managed:
    - name: /data/nginx/conf/ssl/somo.vn-primary.key
    - source: salt://fileserver/nginx/somo.vn-primary.key
    - user: nobody
    - group: nobody
    - mode: 644
    - require:
      - pkg: nginx-install

nginx-vhosts-uuzu-conf:
  file.managed:
    - name: /data/nginx/conf/vhosts/t.mm.uuzu.com.conf
    - source: salt://fileserver/nginx/t.mm.uuzu.com.conf
    - template: jinja
    - user: nobody
    - group: nobody
    - require:
      - pkg: nginx-install

nginx-vhosts-default-conf:
  file.managed:
    - name: /data/nginx/conf/vhosts/default.conf
    - source: salt://fileserver/nginx/default.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: nginx-install

nginx-fastcgi-conf:
  file.managed:
    - name: /data/nginx/conf/fastcgi_params
    - source: salt://fileserver/nginx/fastcgi_params
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: nginx-install

nginx-conf:
  file.managed:
    - name: /data/nginx/conf/nginx.conf
    - source: salt://fileserver/nginx/nginx.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: nginx-install
  service.running:
    - name: nginx
    - enable: True
    - watch:
      - file: nginx-vhosts-default-conf
      - file: nginx-vhosts-uuzu-conf
      - file: nginx-fastcgi-conf
      - file: nginx-conf
    - require:
      - pkg: nginx-install
      - file: nginx-vhosts-default-conf
      - file: nginx-vhosts-uuzu-conf
      - file: nginx-fastcgi-conf
      - file: nginx-conf

