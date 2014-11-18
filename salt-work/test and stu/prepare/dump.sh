#!/bin/bash
inner_ip=$(ifconfig|grep -E "([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})" | awk -F" " '{print $2}' | cut -d":" -f2 | grep -E "^192\.|^10\.")
gamedb_name=$(/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 nslm_vietnam_gm -e "select game_dbname  from server where server_ip='$inner_ip' and status='0'")
/data/mysql/bin/mysqldump -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 mysql > /srv/salt/fileserver/mysql/mysql.sql
/data/mysql/bin/mysqldump -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 nsvietnam_static > /srv/salt/fileserver/mysql/static.sql
/data/mysql/bin/mysqldump -udbmanager -peyDqNafZ6pq39Rah -h127.0.0.1 $gamedb_name > /srv/salt/fileserver/mysql/game.sql
