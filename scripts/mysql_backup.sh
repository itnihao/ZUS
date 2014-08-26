#!/bin/bash
#by orbs
#email - -
#script is about complete backup and incremental backup mysql database
RED(){
    echo -e "\e[31m"$1" \e[m"
}
GREEN(){
    echo -e "\e[32m"$1" \e[m"
}
user="root"
password="123456"
host="127.0.0.1"
innobackupex=/usr/bin/innobackupex
mysql_etc=/data/mysql/my.cnf
backup_dir=/data/xtraback
logfile=/data/backup_logfile
pidfile=/data/backup.pid

function pre_check() {
    if [ ! -d ${backup_dir} ];then
        mkdir ${backup_dir}
    else
        GREEN "backup dir exists"
    fi
    if [ ! `rpm -q |grep percona-xtrabackup >/dev/null 2>&1` ];then
        yum -y install perl-DBD-mysql perl-Time-HiRes >/dev/null 
        rpm -ivh http://www.percona.com/downloads/XtraBackup/XtraBackup-2.2.3/binary/redhat/6/x86_64/percona-xtrabackup-2.2.3-4982.el6.x86_64.rpm 
    else
        GREEN "percona-xtrabackup is already installed"
    fi
}
[ ! -f $pidfile ] && touch ${pidfile}
_PID=`cat ${pidfile}`
if [ `ps ax|awk '{print $1}'|grep -v "grep"|grep -c "${_PID}"` -eq 1 ];then 
    GREEN "innobackupex progress is already running"
    exit 1
else
    echo $$ >${pidfile}
fi                           
function bakup_all() {
    cd $backup_dir
    innobackupex --user=$user --password=$password --host=$host --defaults-file=$mysql_etc --use-memory=10M --throttle=20 --stream=tar $backup_dir |gzip - > backup_all.tar.gz >/dev/null 
    RETVAL=$?
    if [ $RETVAL -eq 0 ];then
        GREEN "Complete backup success"
        rm -rf ${pidfile}
        cd ${backup_dir}
        /bin/tar zxfi backup_all.tar.gz xtrabackup_checkpoints
    else
        RED "Complete backup faild"
    fi
}
#function backup_irc() {

#}


bakup_all

