%define     zabbix_user     zabbix
%define     zabbix_home     /data/zabbix
Name:		zabbix-orbs
Version:    2.2.5	
Release:	1%{?dist}
Summary:	zabbix agentd

Group:		Applications/Server
License:	BSD
URL:		http://www.zabbix.com
Source0:	http://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.2.5/%{name}-%{version}.tar.gz
Source1:    zabbix_agentd.conf 
Source2:    zabbix_agentd
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:      net-snmp, net-snmp-devel, curl, curl-devel, perl-DBI
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig,initscripts
Requires(postun):   initscripts

%description
zabbix agentd

%prep
%setup -q


%build
export DESTDIR=%{buildroot}
./configure \
        --prefix=%{zabbix_home} \
        --enable-agent


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/zabbix_agentd
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{zabbix_home}/etc/zabbix_agentd.conf

%clean
rm -rf %{buildroot}

%pre
grep -q zabbix /etc/passwd || %{_sbindir}/groupadd %{zabbix_user} >/dev/null 2>&1
grep -q zabbix /etc/passwd || %{_sbindir}/useradd -g %{zabbix_user} %{zabbix_user}>/dev/null 2>&1

%preun
/sbin/service zabbix_agentd stop >/dev/null 2>&1
/sbin/chkconfig --del zabbix_agentd
/usr/sbin/userdel -f %{zabbix_user} >/dev/null 2>&1
/bin/rm /etc/init.d/zabbix_agentd -f >/dev/null 2>&1

%post
/sbin/chkconfig --add zabbix_agentd
service zabbix_agentd restart >/dev/null 2>&1 

%postun
rm /home/zabbix -rf
rm /data/zabbix -rf

%files
%defattr(-,root,root,-)
%doc
%{zabbix_home}/
%{_initrddir}/zabbix_agentd

%changelog

