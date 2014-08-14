nginx_source:
  file:
    - managed
    - name: /tmp/nginx-1.4.7.tar.gz
    - unless: test -e /tmp/nginx-1.4.7.tar.gz
    - source: salt://nginx/files/nginx-1.4.7.tar.gz

extract_nginx:
  cmd.run:
    - cwd: /tmp
    - names:
      - tar xvf nginx-1.4.7.tar.gz
    - unless: test -d nginx-1.4.7
    - require:
      - file: nginx_source

nginx_user:
  user.present:
    - name: nginx
    - createhome: False
    - shell: /sbin/nologin

nginx_pkg:
  pkg.installed:
    - names:
      - gcc
      - openssl-devel
      - pcre-devel
      - zlib-devel

nginx_compile:
  cmd.run:
    - cwd: /tmp/nginx-1.4.7
    - names: 
      - ./configure --prefix=/data/nginx 
      - make
      - make install
    - require:
      - cmd: extract_nginx
      - pkg: nginx_pkg
    - unless: test -d /data/nginx
nginx_make:
  cmd.run:
    - cwd: /tmp/nginx-1.4.7
    - names:
      - make
    - require:
      - pkg: nginx_pkg
      - cmd: nginx_compile

nginx_install:
  cmd.run:
    - cwd: /tmp/nginx-1.4.7
    - names:
      - make install
    - require:
      - pkg: nginx_pkg
      - cmd: nginx_make
nginx_dir:
  cmd.run:
    - names:
      - mkdir /data/nginx/conf.d/
    - require:
      - cmd: nginx_compile