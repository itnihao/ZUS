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
xtrabackup=/usr/bin/xtrabackup
mysql_etc=/data/mysql/my.cnf
backup_dir=/data/xtraback
datetime=$(date +"%F-%H-%M")

function pre_check() {
    if [ ! -d ${backup_dir} ];then
        mkdir ${backup_dir}
    else
        GREEN "backup dir exists"
    fi
    if [ ! -d ${incre_dir} ];then
        mkdir ${incre_dir}
    else
        GREEN "incre dir exists"
    fi
    rpm -qa |grep percona-xtrabackup >/dev/null 2>&1
    RETVAL=$?
    if [ $RETVAL -eq 0 ];then
        GREEN "percona-xtrabackup is already installed"
    else
        yum -y install perl-DBD-mysql perl-Time-HiRes >/dev/null 
        rpm -ivh http://www.percona.com/downloads/XtraBackup/XtraBackup-2.2.3/binary/redhat/6/x86_64/percona-xtrabackup-2.2.3-4982.el6.x86_64.rpm 
    fi
}

function backup_all() {
    cd $backup_dir
    $innobackupex --user=$user --password=$password --host=$host --defaults-file=$mysql_etc --use-memory=10M --throttle=20 --stream=tar $backup_dir |gzip - > $datetime.tar.gz  
    RETVAL=$?
    if [ $RETVAL -eq 0 ];then
        GREEN "Complete backup success"
        cd ${backup_dir}
        /bin/tar zxfi $datetime.tar.gz xtrabackup_checkpoints
    else
        RED "Complete backup faild"
    fi
}
function backup_inc() {
    if [ ! -e $backup_dir/xtrabackup_checkpoints ];then
        RED "Check complete backup not run yet"
        backup_all 
    else
        checkpoints=$(awk '/to_lsn/ {print $3}' $backup_dir/xtrabackup_checkpoints)
        $xtrabackup  --defaults-file=$mysql_etc --backup --user=$user --password=$password --host=$host  --use-memory=10M --throttle=20 --target-dir=$backup_dir/$datetime --incremental-lsn=$checkpoints
        RETVAL=$?
        if [ $RETVAL -eq 0 ];then
            GREEN "incre backup success"
            cd $backup_dir
            cp $backup_dir/$datetime/xtrabackup_checkpoints $backup_dir/xtrabackup_checkpoints
            tar zcvf $datetime.tar.gz $datetime >/dev/null 2>&1
            rm -rf $datetime
        else
            RED "incre backup faild"
        fi
    fi
}

pre_check
backup_inc
