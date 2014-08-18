%define	nginx_user	nginx
%define	nginx_group	nginx
%define	nginx_home	/data/nginx

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
make -j %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}/ install
install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/nginx
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{nginx_home}/conf/nginx.conf
install -p -d -m 0644 %{buildroot}%{nginx_home}/conf.d
%clean
rm -rf %{buildroot}

%pre
grep -q nginx /etc/passwd || %{_sbindir}/groupadd %{nginx_group} >/dev/null 2>&1
grep -q nginx /etc/passwd || %{_sbindir}/useradd -g %{nginx_user} %{nginx_user}>/dev/null 2>&1

%preun
if [ $1 -eq 0 ]; then
    /sbin/service nginx stop >/dev/null 2>&1
    /sbin/chkconfig --del nginx
    /usr/sbin/userdel -f %{nginx_user} >/dev/null 2>&1
    /bin/rm /etc/init.d/nginx -f >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add nginx
service nginx restart >/dev/null 2>&1 

%postun
rm /home/nginx -rf
rm /data/nginx -rf

%files
%defattr(-,root,root,-)
%doc
%{nginx_home}/
%{nginx_home}/conf.d
%{_initrddir}/nginx

%changelog