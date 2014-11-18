datadazongshi-dir:
  file.directory:
    - name: /data/dazongshi
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 777
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

dataweb-dir:
  file.directory:
    - name: /data/web
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

dataconfig-dir:
  file.directory:
    - name: /data/config
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

datadb-dir:
  file.directory:
    - name: /data/conf/db
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

datafight-dir:
  file.directory:
    - name: /data/fightdata
    - user: nobody
    - group: nobody
    - file_mode: 777
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

eaccelerator-dir:
  file.directory:
    - name: /dev/shm/eaccelerator_data
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

redis-backup:
  file.directory:
    - name: /data/redisbase
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

mysql-backup:
  file.directory:
    - name: /data/database
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

backup-redis:
  file.directory:
    - name: /backup/redisbase/
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

backup-mysql:
  file.directory:
    - name: /backup/database/
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

rsync-backup:
  file.directory:
    - name: /data/backup
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

backup-script-dir:
  file.directory:
    - name: /usr/local/uuzuback/
    - user: root
    - group: root
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
