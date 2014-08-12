%define	nginx_user	ngnix
%define	nginx_group	nginx
%define	nginx_home	/data/nginx
%define	nginx_logdir	/data/nginx/logs
%define	nginx_confdir	/data/nginx/conf
%define	nginx_datadir	/data/nginx
%define	nginx_web	/data/nginx/html

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
nginx is a HTTP and reverse proxy server

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
install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/nginx
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{nginx_confdir}/nginx.conf
install -p -d -m 0644 %{buildroot}%{nginx_logdir}
install -p -d -m 0644 %{buildroot}%{nginx_web}
install -p -d -m 0644 %{buildroot}%{nginx_home}/conf.d

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -c "Nginx user" -s /bin/false -r -d %{nginx_home} %{nginx_user} 2>/dev/null

%preun
if [ $1 = 0 ]; then
    /sbin/service nginx stop >/dev/null 2>&1
    /sbin/chkconfig --del nginx
fi

%post
/sbin/chkconfig --add nginx

%postun
if [ $1 -ge 1 ]; then
    /sbin/service nginx restart > /dev/null 2>&1 
fi

%files
%defattr(-,root,root,-)
%doc
%{nginx_datadir}/
%{nginx_home}/sbin/nginx
%{_initrddir}/nginx
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