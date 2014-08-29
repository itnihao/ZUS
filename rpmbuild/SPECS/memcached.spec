%define     memcached_home /data/memcached

Name:		memcached
Version:	1.4.20
Release:	1%{?dist}
Summary:	memcached

Group:		Application/Server
License:	BSD
URL:		http://www.memcached.org
Source0:	http://www.memcached.org/files/%{name}-%{version}.tar.gz 
Source1:    memcached.init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	libevent, libevent-devel
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig,initscripts
Requires(postun):   initscripts

%description
memcached

%prep
%setup -q

%build
export DESTDIR=%{buildroot}
./configure --prefix=%{memcached_home}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/memcached
install -d -p -m 0644 %{buildroot}%{memcached_home}/var
install -d -p -m 0644 %{buildroot}%{memcached_home}/var/run

%clean
rm -rf %{buildroot}

%preun
/sbin/service memcached stop >/dev/null 2>&1
/sbin/chkconfig --del memcached
/bin/rm /etc/init.d/memcached -f >/dev/null 2>&1

%post
chmod +x /etc/init.d/memcached
/sbin/chkconfig --add memcached
service memcached restart >/dev/null 2>&1 

%postun
rm /data/memcached -rf

%files
%defattr(-,root,root,-)
%doc
%{memcached_home}/
%{_initrddir}/memcached

%changelog

