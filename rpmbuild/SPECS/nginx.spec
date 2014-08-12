%define	nginx_user	nginx
%define	nginx_group	nginx
%define	nginx_home	/data/nginx
%define	nginx_logdir	%{nginx_home}/logs
%define	nginx_confdir	%{nginx_home}/conf
%define	nginx_datadir	%{nginx_home}
%define	nginx_web	%{nginx_home}/html

Name:		nginx		
Version:	1.4.7
Release:	1%{?dist}
Summary:	High Performance Web Server

Group:		Applications/Server
License:	GPL
URL:		http://nginx.org/
Source0:	http://nginx.org/download/%{name}-%{version}.tar.gz
Source1:	nginx.init
Source2:	nginx.conf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	pcre-devel,zlib-devel
Requires:	pcre,zlib,openssl
Requires(pre):	shadow-utils
Requires(post):	chkconfig
Requires(preun):	chkconfig,initscripts
Requires(postun):	initscripts

%description
nginx is a HTTP and reverse proxy serve

%prep
%setup -q

%build
export DESTDIR=%{buildroot}
./configure \
--user=%{nginx_user} \
--group=%{nginx_group} \
--prefix=%{nginx_home}
make 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
chmod 0755 %{buildroot}%{nginx_home}/sbin/nginx
install -p -D -m 0755 %{SOURCE1} /etc/init.d/nginx
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{nginx_confdir}/nginx.conf
install -p -d -m 0644 %{buildroot}%{nginx_logdir}
install -p -d -m 0644 %{buildroot}%{nginx_web}
install -p -d -m 0644 %{buildroot}%{nginx_home}/conf.d

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -M %{nginx_user} >/dev/null 2>&1

%preun
if [ $1 -eq 0 ]; then
    /sbin/service nginx stop >/dev/null 2>&1
    /sbin/chkconfig --del nginx
    /usr/sbin/userdel -f %{nginx_user} >/dev/null 2>&1
    /bin/rm /etc/init.d/nginx -f >/dev/null 2>&1
    /bin/rm %{nginx_home} -rf >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add nginx
/etc/init.d/nginx restart >/dev/null 2>&1 

%postun
if [ $1 -ge 1 ]; then
    /etc/init.d/nginx restart >/dev/null 2>&1 
fi

%files
%defattr(-,root,root,-)
%doc
%{nginx_datadir}/
%{nginx_home}/sbin/nginx
%dir	%{nginx_confdir}
%dir	%{nginx_web}
%dir	%{nginx_logdir}
%dir	%{nginx_home}/conf.d
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/nginx.conf.default
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/nginx.conf
%config(noreplace) %{nginx_confdir}/mime.types

%changelog