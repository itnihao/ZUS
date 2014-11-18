#!/bin/bash
inner_ip=$(ifconfig|grep -E "([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})" | awk -F" " '{print $2}' | cut -d":" -f2 | grep -E "^192\.|^10\.")
/bin/hostname $inner_ip
sed -i "s/^HOSTNAME.*/HOSTNAME=$inner_ip/" /etc/sysconfig/network
rpm -Uvh http://ftp.linux.ncsu.edu/pub/epel/6/i386/epel-release-6-8.noarch.rpm
sed -i 's/^#//' /etc/yum.repos.d/epel.repo
sed -i 's/^mirrorlist/#mirrorlist/' /etc/yum.repos.d/epel.repo
yum -y install salt-minion
rpm -e epel-release-6-8.noarch
yum clean all
yum makecache
sed -i "s/^#master: salt/master: 192.168.0.100" /etc/salt/minion
