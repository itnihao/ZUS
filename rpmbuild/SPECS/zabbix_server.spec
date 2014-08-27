%define     zabbix_user     zabbix
%define     zabbix_home     /data/zabbix
Name:		zabbix-orbs
Version:    2.2.5	
Release:	1%{?dist}
Summary:	zabbix server

Group:		Applications/Server
License:	BSD
URL:		http://www.zabbix.com
Source0:	http://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.2.5/%{name}-%{version}.tar.gz
Source1:    zabbix_server.conf 
Source2:    zabbix_server.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:      net-snmp, net-snmp-devel, curl, curl-devel, perl-DBI
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig,initscripts
Requires(postun):   initscripts

%description
zabbix server

%prep
%setup -q


%build
export DESTDIR=%{buildroot}
./configure \
        --prefix=%{zabbix_home} \
        --with-mysql=/data/mysql/bin/mysql_config \
        --with-net-snmp \
        --with-libcurl \
        --enable-server \
        --enable-agent


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/zabbix_server
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{zabbix_home}/etc/zabbix_server.conf
install -p -d -m 0644 %{buildroot}%{zabbix_home}/html
install -p -d -m 0644 %{buildroot}%{zabbix_home}/database
cp frontends/php/* %{buildroot}%{zabbix_home}/html/ -R
cp database/mysql/* %{buildroot}%{zabbix_home}/database/ -R

%clean
rm -rf %{buildroot}

#%pre
#grep -q zabbix /etc/passwd || %{_sbindir}/groupadd %{zabbix_user} >/dev/null 2>&1
#grep -q zabbix /etc/passwd || %{_sbindir}/useradd -g %{zabbix_user} %{zabbix_user}>/dev/null 2>&1
#mysql -uroot -p123456 -e "create database zabbix;"
#mysql -uroot -p123456 -e "grant all on zabbix.* to 'zabbix'@'localhost' identified by '123456';"

#%preun
#/sbin/service zabbix_server stop >/dev/null 2>&1
#/sbin/chkconfig --del zabbix_server
#/usr/sbin/userdel -f %{zabbix_user} >/dev/null 2>&1
#/bin/rm /etc/init.d/zabbix_server -f >/dev/null 2>&1

#%post
#/sbin/chkconfig --add zabbix_server
#service zabbix_server restart >/dev/null 2>&1 

#%postun
#rm /home/zabbix -rf
#rm /data/zabbix -rf

%files
%defattr(-,root,root,-)
%doc
%{zabbix_home}/
%{_initrddir}/zabbix_server

%changelog

