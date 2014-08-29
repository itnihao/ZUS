%define     varnish_user    varnish 
%define     varnish_home    /data/varnish
Name:		varnish
Version:	4.0.1
Release:	1%{?dist}
Summary:	varnish

Group:		Application/Cache
License:	BSD
URL:		https://www.varnish-cache.org
Source0:	https://repo.varnish-cache.org/source/%{name}-%{version}.tar.gz
Source1:    varnish.init
Source2:    varnish
Source3:    varnish.vcl
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	pcre, pcre-devel, python-docutils, pkgconfig, 
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig,initscripts
Requires(postun):   initscripts

%description
varnish

%prep
%setup -q


%build
export DESTDIR=%{buildroot}
./configure --prefix=%{varnish_home} --enable-debugging-symbols --enable-developer-warnings
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d -p -m 0644 %{buildroot}%{varnish_home}/etc
install -d -p -m 0644 %{buildroot}%{varnish_home}/var/run
install -D -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/varnish
install -D -p -m 0755 %{SOURCE2} %{buildroot}%{varnish_home}/etc/varnish
install -D -p -m 0755 %{SOURCE3} %{buildroot}%{varnish_home}/etc/default.vcl

%clean
rm -rf %{buildroot}

%pre
grep -q varnish /etc/passwd || %{_sbindir}/useradd -s /sbin/nologin %{varnish_user}>/dev/null 2>&1

%preun
/sbin/service varnish stop >/dev/null 2>&1
/sbin/chkconfig --del varnish
/usr/sbin/userdel -f %{varnish_user} >/dev/null 2>&1
/bin/rm /etc/init.d/varnish -f >/dev/null 2>&1

%post
/sbin/chkconfig --add varnish
service varnish restart >/dev/null 2>&1 

%postun
rm /home/varnish -rf
rm /data/varnish -rf

%files
%defattr(-,root,root,-)
%doc
%{varnish_home}/
%{_initrddir}/varnish

%changelog

