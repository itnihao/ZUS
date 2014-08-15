include:
  - redis.install
redis_conf:
  file.managed:
    - name: /data/redis/etc/redis.conf
    - source: salt://redis/files/redis.conf
    - unless:
      - test -d /data/redis/etc
      - test -d /data/redis/database
redis_service:
  file.managed:
    - name: /etc/init.d/redis
    - source: salt://redis/files/redis.init
    - user: root
    - mode: 755
  cmd.run:
    - names:
      - /sbin/chkconfig --add redis
      - /sbin/chkconfig redis on
    - unless: /sbin/chkconfig --list redis
  service.running:
    - name: redis
    - enable: True
    - watch:
      - file: /data/redis/etc/redis.conf