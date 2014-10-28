#!/bin/bash
#init openstack on ubuntu
function init() {
	echo '''
	deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
	deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
	deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
	deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
	deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
	deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
	deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
	deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
	deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
	deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
	'''>/etc/apt/sources.list
	apt-get autoclean
	apt-get -y update
	apt-get -y upgrade
	apt-get -y install ntp python-dev bridge-utils python-mysqldb
	echo '''
	127.127.1.0
	'''>>/etc/ntp.conf
	service ntp restart
	inner_ip=$(ifconfig eth0 | grep -E "([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})" | awk -F" " '{print $2}' | cut -d":" -f2 | grep -E "^192\.|^10\.")
}

function init_mysql() {
	#mysql password here set admin
	apt-get -y install libmysqlclient-dev mysql-client mysql-server
	sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/my.cnf
	apt-get install -y rabbitmq-server
}

function init_keystone() {
	apt-get -y install keystone
	mysql -uroot -padmin -e "create database keystone;"
	mysql -uroot -padmin -e "grant all privileges on keystone.* to 'keystone'@'localhost' identified by 'keystone';"
	mysql -uroot -padmin -e "grant all privileges on keystone.* to 'keystone'@'%' identified by 'keystone';"
	sed -i 's#^connection.*#connection = mysql://keystone:keystone@$inner_ip/keystone#' /etc/keystone/keystone.conf
	sed -i 's/^#admin_token.*/admin_token=ADMIN/' /etc/keystone/keystone.conf
	sed -i 's@^log_dir.*@log_dir=/var/log/keystone/@' /etc/keystone/keystone.conf
	service keystone restart
	keystone-manage db_sync
	export OS_SERVICE_TOKEN=ADMIN
	export OS_SERVICE_ENDPOINT=http://$inner_ip:35357/v2.0
	#create super account
	keystone user-create --name=admin --pass=admin --email=admin@example.com
	keystone role-create --name=admin
	keystone tenant-create --name=admin --description="admin tenant"
	keystone user-role-add --user=admin --tenant=admin --role=admin
	keystone user-role-add --user=admin --tenant=admin --role=_member_
	#create demo user
	keystone user-create --name=demo --pass=demo --email=demo@example.com
	keystone tenant-create --name=demo --description="demo tenant"
	keystone user-role-add --user=demo --role=_member_ --tenant=demo
	#create service account
	keystone tenant-create --name=service --description="service tenant"
	#create service API of endpoint
	keystone service-create --name=keystone --type=identity --description="openstack identity"
	#create endpoint
	keystone endpoint-create --service-id=$(keystone service-list|awk '/identity/ {print $2}')  \
	--publicurl=http://$outer_ip:5000/v2.0 \
	--internalurl=http://$inner_ip:5000/v2.0 \
	--adminurl=http://$inner_ip:35357/v2.0
	echo '''
	export OS_TENANT_NAME=admin
	export OS_USERNAME=admin
	export OS_PASSWORD=admin
	export OS_AUTH_URL="http://$outer_ip:5000/v2.0/"
	'''>/root/cred
	
	echo '''
	export OS_USERNAME=admin
	export OS_PASSWORD=admin
	export OS_TENANT_NAME=admin
	export OS_AUTH_URL=http://$inner_ip:35357/v2.0
	'''>/root/admin_cred
}

function init_glance () {
	apt-get install -y glance python-glanceclient
	mysql -uroot -padmin -e "create database glance;"
	mysql -uroot -padmin -e "grant all privileges on glance.* to 'glance'@'localhost' identified by 'glance';"
	mysql -uroot -padmin -e "grant all privileges on glance.* to 'glance'@'%' identified by 'glance';"
	keystone user-create --name=glance --pass=glance --email=glance@example.com
	keystone user-role-add --user=glance --tenant=service --role=admin
	keystone service-create --name=glance --type=image --description="openstack image service"
	keystone endpoint-create --service-id=$(keystone service-list|awk '/image/ {print $2}') \
	--publicurl=http://192.168.85.128:9292 \
	--internalurl=http://192.168.2.61:9292  \
	--adminurl=http://192.168.2.61:9292
	sed -i 's/^backend.*/backend = mysql/' /etc/glance/glance-api.conf 
	sed -i 's#sqlite_db.*#connection = mysql://glance:glance@192.168.2.61/glance#' /etc/glance/glance-api.conf
	sed -i '/^rabbit_host/irpc_backend = rabbit' /etc/glance/glance-api.conf
	sed -i 's/^rabbit_host.*/rabbit_host = 192.168.2.61/' /etc/glance/glance-api.conf
	sed -i "s#auth_host.*#auth_host = 192.168.2.61#" /etc/glance/glance-api.conf
	sed -i '/keystone_auth/a\auth_uri = http://192.168.2.61:5000' /etc/glance/glance-api.conf
	sed -i 's/^admin_tenant_name.*/admin_tenant_name = service/' /etc/glance/glance-api.conf
	sed -i 's/^admin_user.*/admin_user = glance/' /etc/glance/glance-api.conf
	sed -i 's/^admin_password.*/admin_password = glance/' /etc/glance/glance-api.conf
	sed -i '/paste_deploy/a\flavor = keystone' /etc/glance/glance-api.conf
	
	sed -i 's#sqlite_db.*#connection = mysql://glance:glance@192.168.2.61/glance#' /etc/glance/glance-registry.conf
	sed -i 's/^backend.*/backend = mysql/' /etc/glance/glance-registry.conf
	sed -i '/keystone_auth/a\auth_uri = http://192.168.2.61:5000' /etc/glance/glance-registry.conf
	sed -i "s#auth_host.*#auth_host = 192.168.2.61#" /etc/glance/glance-registry.conf
	sed -i 's/^admin_tenant_name.*/admin_tenant_name = service/' /etc/glance/glance-registry.conf
	sed -i 's/^admin_user.*/admin_user = glance/' /etc/glance/glance-registry.conf
	sed -i 's/^admin_password.*/admin_password = glance/' /etc/glance/glance-registry.conf
	sed -i '/paste_deploy/a\flavor = keystone' /etc/glance/glance-registry.conf
	mysql -uroot -padmin -e "alter table glance.migrate_version convert to character set utf8 collate utf8_unicode_ci;"
	service glance-api restart
	service glance-registry restart
	glance-manage db_sync
}

function init_nove() {
	apt-get -y install nova-api nova-cert nova-conductor nova-consoleauth \
	nova-novncproxy nova-scheduler python-novaclient nova-volume \
	nova-compute nova-compute-kvm nova-doc nova-network 
	mysql -uroot -padmin -e "create database nova;"
	mysql -uroot -padmin -e "grant all privileges on nova.* to 'nova'@'localhost' identified by 'nova';"
	mysql -uroot -padmin -e "grant all privileges on nova.* to 'nova'@'%' identified by 'nova';"
	keystone user-create --name=nova --pass=nova --email=nova@example.com
	keystone user-role-add --user=nova --tenant=service --role=admin
	keystone service-create --name=nova --type=compute --description="openstack compute"
	keystone endpoint-create \
	--service-id=$(keystone service-list | awk '/ compute / {print $2}') \
	--publicurl=http://192.168.85.128.:8774/v2/%\(tenant_id\)s \
	--internalurl=http://192.168.2.61:8774/v2/%\(tenant_id\)s \
	--adminurl=http://192.168.2.61:8774/v2/%\(tenant_id\)s
	echo '''
	rpc_backend = rabbit
	rabbit_host = 192.168.2.61
	my_ip = 192.168.2.61
	vncserver_listen = 192.168.2.61
	vncserver_proxyclient_address = 192.168.2.61
	auth_strategy = keystone

	[keystone_authtoken]
	auth_uri = http://192.168.2.61:5000
	auth_host = 192.168.2.61
	auth_port = 35357
	auth_protocol = http
	admin_tenant_name = service
	admin_user = nova
	admin_password = nova

	[database]
	connection = mysql://nova:nova@192.168.2.61/nova
	''' >>/etc/nova/nova.conf
	
	nova-manage db sync
	service nova-api restart
	service nova-cert restart
	service nova-conductor restart
	service nova-consoleauth restart
	service nova-novncproxy restart
	service nova-scheduler restart
}

function init_neutron() {
	apt-get install -y neutron-server neutron-plugin-ml2
	mysql -uroot -padmin -e "create database neutron;"
	mysql -uroot -padmin -e "grant all privileges on neutron.* to 'neutron'@'localhost' identified by 'neutron';"
	mysql -uroot -padmin -e "grant all privileges on neutron.* to 'neutron'@'%' identified by 'neutron';"
	keystone user-create --name=neutron --pass=neutron --email=neutron@example.com
	keystone user-role-add --user=neutron --tenant=service --role=admin
	keystone service-create --name=neutron --type=network --description="openstack networking"
	keystone endpoint-create --service-id=$(keystone service-list |awk '/network/ {print $2}') \
	--publicurl=http://192.168.85.128:9696 \
	--internalurl=http://192.168.2.61:9696 \
	--adminurl=http://192.168.2.61:9696
	sed -i 's/^core_plugin.*/core_plugin = ml2/' /etc/neutron/neutron.conf
	sed -i 's/^# service_plugins.*/service_plugins = router/' /etc/neutron/neutron.conf
	sed -i 's/^# auth_strategy.*/auth_strategy = keystone/' /etc/neutron/neutron.conf
	sed -i 's/^# allow_overlapping.*/allow_overlapping_ips = True/' /etc/neutron/neutron.conf
	sed -i 's/^# rpc_backend = .*/rpc_backend = neutron.openstack.common.rpc.impl_kombu/' /etc/neutron/neutron.conf
	sed -i 's/^# rabbit_host .*/rabbit_host = 192.168.2.61/' /etc/neutron/neutron.conf
	sed -i 's/^# notify_nova_on_port_data.*/notify_nova_on_port_data_changes = True/' /etc/neutron/neutron.conf
	sed -i 's/^# notify_nova_on_port_status_changes.*/notify_nova_on_port_status_changes = True/' /etc/neutron/neutron.conf
	sed -i 's@^# nova_url.*@nova_url =http://192.168.2.61:8774/v2@' /etc/neutron/neutron.conf
	sed -i 's/^# nova_admin_username.*/nova_admin_username = nova/' /etc/neutron/neutron.conf
	sed -i 's/^# nova_admin_pass.*/nova_admin_password = nova/' /etc/neutron/neutron.conf
	sed -i 's@^# nova_admin_auth_url .*@nova_admin_auth_url =http://192.168.2.61:35357/v2.0@' /etc/neutron/neutron.conf
	sed -i 's/^admin_tenant_name .*/admin_tenant_name = service/' /etc/neutron/neutron.conf
	sed -i 's/^admin_user .*/admin_user = neutron/' /etc/neutron/neutron.conf
	sed -i 's/^admin_password .*/admin_password = neutron/' /etc/neutron/neutron.conf
	sed -i '/keystone_auth/a\auth_uri = http://192.168.2.61:5000' /etc/neutron/neutron.conf
	sed -i 's#^connection.*#connection = mysql://neutron:neutron@192.168.2.61/neutron#' /etc/neutron/neutron.conf
	
	sed -i 's/^# type_drivers.*/type_drivers = gre/' /etc/neutron/plugins/ml2/ml2_conf.ini
	sed -i 's/^# tenant_network.*/tenant_network_types = gre/' /etc/neutron/plugins/ml2/ml2_conf.ini 
	sed -i 's/^# mechanism_drivers.*/mechanism_drivers = openvswitch/' /etc/neutron/plugins/ml2/ml2_conf.ini
	sed -i 's/^# tunnel_id_ranges.*/tunnel_id_ranges = 1:1000/' /etc/neutron/plugins/ml2/ml2_conf.ini
	sed -i '/securitygroup/a\firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver' /etc/neutron/plugins/ml2/ml2_conf.ini
	sed -i 's/^# enable_security_group.*/enable_security_group = True/' /etc/neutron/plugins/ml2/ml2_conf.ini
	
}