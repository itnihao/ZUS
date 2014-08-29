%define	redis_home	/data/redis
%define	redis_datadir	%{redis_home}/database
Name:		redis
Version:	2.8.13
Release:	1%{?dist}
Summary:	A persistent key-value database

Group:		Applications/Server
License:	BSD
URL:		http://redis.io/
Source0:	http://download.redis.io/releases/%{name}-%{version}.tar.gz
Source1:	redis.init
Source2:	redis.conf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
	
Requires(post):	chkconfig
Requires(postun):	initscripts
Requires(preun):	chkconfig,initscripts	

%description
Redis is an advanced key-value store.

%prep
%setup -q


%build
export DESTDIR=%{buildroot}
make


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -p -d -m 0644 %{buildroot}%{redis_home}
install -p -d -m 0755 %{buildroot}%{redis_home}/etc
install -p -d -m 0755 %{buildroot}%{redis_home}/log
install -p -d -m 0755 %{buildroot}%{redis_home}/run
install -p -d -m 0755 %{buildroot}%{redis_datadir}
install -D -p -m 0755 %{SOURCE1} /etc/init.d/redis
install -D -p -m 0755 src/redis-server %{buildroot}%{redis_home}/sbin/redis-server
install -D -p -m 0755 src/redis-benchmark %{buildroot}%{redis_home}/bin/redis-benchmark
install -D -p -m 0755 src/redis-cli %{buildroot}%{redis_home}/bin/redis-cli 
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{redis_home}/etc/redis.conf


%clean
rm -rf %{buildroot}

%preun
if [ $1 -eq 0 ]; then
    /etc/init.d/redis stop >/dev/null 2>&1
    /sbin/chkconfig --del redis
    /bin/rm /etc/init.d/redis -f >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add redis
/etc/init.d/redis start >/dev/null 2>&1

%postun

%files
%defattr(-,root,root,-)
%doc
%{redis_home}/
%{redis_home}/run
%{redis_datadir}/
%{redis_home}/sbin/redis-server
%{redis_home}/bin/redis-cli
%{redis_home}/bin/redis-benchmark
%{redis_home}/etc/redis.conf


%changelog