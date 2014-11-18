php-install:
  pkg.installed:
    - name: php-fpm
    - require:
      - file: /etc/yum.repos.d/omnslm.repo

php-path:
  file.managed:
    - name: /usr/local/webserver/php/bin/php-path.sh
    - source: salt://fileserver/php-fpm/php-path.sh
    - user: root
    - group: root
    - mode: 755
    - require:
      - pkg: php-install

php-ini-conf:
  file.managed:
    - name: /usr/local/webserver/php/lib/php.ini
    - source: salt://fileserver/php-fpm/php.ini
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: php-install

msgpack:
  file.managed:
    - name: /usr/local/webserver/php/lib/php/extensions/no-debug-non-zts-20100525/msgpack.so
    - source: salt://fileserver/php-fpm/msgpack.so
    - user: root
    - group: root
    - mode: 777
    - require:
      - pkg: php-install

EpollServer:
  file.managed:
    - name: /usr/local/webserver/php/lib/php/extensions/no-debug-non-zts-20100525/EpollServer.so
    - source: salt://fileserver/php-fpm/EpollServer.so
    - user: root
    - group: root
    - mode: 777
    - require:
      - pkg: php-install

php-fpm-conf:
  file.managed:
    - name: /usr/local/webserver/php/etc/php-fpm.conf
    - source: salt://fileserver/php-fpm/php-fpm.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: php-install

php-fpm:
  service.running:
    - name: php-fpm
    - watch:
      - file: php-ini-conf
      - file: php-fpm-conf
    - require:
      - pkg: php-install
