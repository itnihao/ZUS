%define	nginx_user	nginx
%define	nginx_group	%{nginx_user}
%define	nginx_home	%{_localstatedir}/lib/nginx
%define	nginx_home_tmp	%{nginx_home}/tmp
%define	nginx_logdir	%{_localstatedir}/log/nginx
%define	nginx_confdir	%{_sysconfdir}/nginx
%define	nginx_datadir	%{_datadir}/nginx
%define	nginx_webroot	%{nginx_datadir}/html
%define	version		1.7.0.1

Name:		ngx_openresty
Version:	%{version}
Release:	1
Summary:	Robust, small and high performance HTTP and reverse proxy server	
Group:		System Environment/Daemons
License:	BSD
URL:		http://nginx.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:	pcre-devel,zlib-devel,openssl-devel,perl,
#Requires:	pcre,openssl,gd

Source0:	http://openresty.org/download/ngx_openresty-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	virtual.conf
Source4:	ssl.conf
Source5:	%{name}.sysconfig
Source6:	nginx.conf
Source7:	default.conf
Source100:	index.html
Source101:	404.html
Source102:	50x.html

%description
openresty is an HTTP(S) server,HTTP(S) reverse proxy and IMAP/POP3
proxy server written by agentzh.

%prep
%setup -q

%build
./configure \
    --user=%{nginx_user} \
    --group=%{nginx_group} \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{nginx_confdir}/%{name}.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --http-uwsgi-temp-path=%{nginx_home_tmp}/uwsgi \
    --http-scgi-temp-path=%{nginx_home_tmp}/scgi \
    --pid-path=%{_localstatedir}/run/%{name}.pid \
    --lock-path=%{_localstatedir}/lock/subsys/%{name} \
    --with-http_ssl_module \
    --with-pcre \
    --with-http_realip_module \
    --with-http_stub_status_module \
    --with-luajit 
make 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} 

%clean
rm -rf ${buildroot}

%pre
if [ $1 == 1 ];then
    %{_sbindir}/useradd -c "Nginx user" -s /bin/false -r -d %{nginx_home} %{nginx_user} 2>/dev/null 
fi

%post
if [$1 == 1 ];then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 =  0 ];then
    /sbin/server %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root,-)
%doc

%changelog
