#!/usr/bin/env python 
import os

def gamedb():
	grains={}
	ip=os.popen('/sbin/ifconfig|grep "inet addr"|awk \'{print $2}\'|awk -F\':\' \'{print $2}\'').readlines()[1]
	strip=str(ip.split()[0])
	gamedbcmd="/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h192.168.0.100 nslm_vietnam_gm -e \"select game_dbname from server where server_ip='%s' and status='0'\"" %str(strip)
	gamedb = os.popen(str(gamedbcmd)).readlines()[1]
	grains['gamedb']=str(gamedb.split()[0])
	serveridcmd="/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h192.168.0.100 nslm_vietnam_gm -e \"select dc_server_id from server where server_ip='%s' and status='0'\"" %str(strip)
	serverid=os.popen(str(serveridcmd)).readlines()[1]
	grains['serverid']=str(serverid.split()[0])
	gameidcmd="/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h192.168.0.100 nslm_vietnam_gm -e \"select game_id from server where server_ip='%s' and status='0'\"" %str(strip)
	gameid=os.popen(str(gameidcmd)).readlines()[1]
	grains['gameid']=str(gameid.split()[0])
	opidcmd="/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h192.168.0.100 nslm_vietnam_gm -e \"select operator_id from server where server_ip='%s' and status='0'\"" %str(strip)
	opid=os.popen(str(opidcmd)).readlines()[1]
	grains['opid']=str(opid.split()[0])
	serverurlcmd="/data/mysql/bin/mysql -udbmanager -peyDqNafZ6pq39Rah -h192.168.0.100 nslm_vietnam_gm -e \"select server_url from server where server_ip='%s' and status='0'\"" %str(strip)
	serverurl=os.popen(str(serverurlcmd)).readlines()[1]
	grains['serverurl']=str(serverurl.split()[0])
	return grains

