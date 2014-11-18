mysql-install:
  pkg.installed:
    - name: mysql
    - require:
      - file: /etc/yum.repos.d/omnslm.repo
  cmd.run:
    - name: /data/mysql/scripts/mysql_install_db --user=mysql --datadir=/data/mysql/var/ --basedir=/data/mysql && touch /var/run/mysql_install.lock
    - unless: test -f /var/run/mysql_install.lock
  file.managed:
    - name: /etc/my.cnf
    - source: salt://fileserver/mysql/my.cnf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: mysql

mysql-grant:
  file.managed:
    - name: /tmp/mysql.sql
    - source: salt://fileserver/mysql/mysql.sql
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: mysql-install
  cmd.run:
    - name: /etc/init.d/mysqld restart ; /data/mysql/bin/mysql mysql < /tmp/mysql.sql && touch /var/run/mysql_grant.lock && /etc/init.d/mysqld restart
    - unless: test -f /var/run/mysql_grant.lock
    - require:
      - pkg: mysql-install
      - file: /tmp/mysql.sql

mysqld-running:
  service.running:
    - name: mysqld
    - enable: True
    - require:
      - pkg: mysql-install
      - file: /etc/my.cnf

mysql-static:
  file.managed:
    - name: /tmp/static.sql
    - source: salt://fileserver/mysql/static.sql
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: mysql-install
  cmd.run:
    - name: /data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 -e 'create database nsvietnam_static DEFAULT CHARACTER SET utf8' && /data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 nsvietnam_static < /tmp/static.sql && touch /var/run/mysql_static_db_create.lock
    - unless: test -f /var/run/mysql_static_db_create.lock
    - require:
      - file: /tmp/static.sql

mysql-game:
  file.managed:
    - name: /tmp/game.sql
    - source: salt://fileserver/mysql/game.sql
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: mysql-install
  cmd.run:
    - name: /data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 -e 'create database {{ grains['gamedb']}}  DEFAULT CHARACTER SET utf8' && /data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 {{ grains['gamedb']}} < /tmp/game.sql && touch /var/run/mysql_game_db_create.lock
    - unless: test -f /var/run/mysql_game_db_create.lock
    - require:
      - file: /tmp/game.sql

percona-xtrabackup:
  file.managed:
    - name: /tmp/percona-xtrabackup-2.0.1-446.rhel5.x86_64.rpm
    - source: salt://fileserver/mysql/percona-xtrabackup-2.0.1-446.rhel5.x86_64.rpm
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /tmp && rpm -i percona-xtrabackup-2.0.1-446.rhel5.x86_64.rpm
    - unless: which xtrabackup
