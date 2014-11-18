mysql-backup-script:
  file.managed:
    - name: /usr/local/uuzuback/mysql_backup.sh
    - source: salt://fileserver/crond/mysql_backup.sh
    - user: root
    - group: root
    - mode: 644

redis-backup-script:
  file.managed:
    - name: /usr/local/uuzuback/redis_backup.sh
    - source: salt://fileserver/crond/redis_backup.sh
    - user: root
    - group: root
    - mode: 644

uuzu-backup-script:
  file.managed:
    - name: /usr/local/uuzuback/uuzuback_client.py
    - source: salt://fileserver/crond/uuzuback_client.py
    - user: root
    - group: root
    - mode: 644

crond-script:
  file.managed:
    - name: /var/spool/cron/root
    - source: salt://fileserver/crond/cron-root
    - user: root
    - group: root
    - mode: 644

crond-run:
  service.running:
    - name: crond
    - enable: True
    - watch:
      - file: /var/spool/cron/root
