redis-install:
  pkg.installed:
    - name: redis
    - require:
      - file: /etc/yum.repos.d/omnslm.repo

redis-conf:
  file.managed:
    - name: /data/conf/redis_conf
    - source: salt://fileserver/redis/redis_conf
    - user: root
    - group: root
    - mode: 644
  service:
    - running
    - name: redis
    - enable: True
    - reload: True
    - watch:
      - file: /data/conf/redis_conf
    - require:
      - pkg: redis-install
    
