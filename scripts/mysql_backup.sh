#!/bin/bash
#by orbs
dbuser="root"
dbpass=""
dbhost=""
dbport=3306
dbconf="/data/mysql/my.cnf"
mysql=$(which mysql)
xtrabackup="xtrabackup"
innobackupex="innobackupex"
bak_dir="/data/backup/"
last_incr_point="/data/backup/"
date=$(date +"%F-%H-%M")
log_file="${dbhost}_${date}.log"
xtrabackup_package="percona-xtrabackup"
retval=0
reds () {
	echo -e "\e[31m "$1" \e[m"
}
yellows () {
	echo -e "\e[33m "$1" \e[m"
}

function check_xtrabackup () {
	#check xtrabackup package
	if [ $(rpm -qa|grep percona-xtrabackup |cut -c1-18) == "percona-xtrabackup"} ];then
		yellows "xtrabackup_package is exists" >>${log_file}
	else
		yum -y install perl-Time-HiRes perl-DBD-MySQL
		rpm -ivh http://www.percona.com/downloads/XtraBackup/XtraBackup-2.2.3/binary/redhat/6/x86_64/percona-xtrabackup-2.2.3-4982.el6.x86_64.rpm
	fi
	#check rsync package
	if [ $(which rsync |cut -c10-) == ${rsync} ];then
		yellows  "RSYNC is exists" >>${log_file}
	else
		yum -y install rsync >>${log_file}
	fi
}

function all_back () {
	yellows "All backup" >>${log_file}
	yellows "innobackupex --use-memory=10M --user=${dbuser} --password=${password} --defaults-file=${dbconf} ${bak_dir}" >>${log_file}
	${innobackupex} --use-memory=10M --throttl=20 --user=${dbuser} --password=${password} --defaults-file=${dbconf}  ${bak_dir}
	$retval=$?
	if [ $retval -eq 0 ];then
		yellows "complete backup mysql succ" >>${log_file}
	else
		reds "complate backup mysql faild">>${log_file}
	fi
}

function inc_back () {

}
