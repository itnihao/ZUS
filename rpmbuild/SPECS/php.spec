%define     php_home    /data/php
Name:                   php-orbs		
Version:	            5.5.15
Release:	            1%{?dist}
Summary:	            php
Group:                  Applications/Server
License:                GPL
URL:                    http://php.net/
Source0:                http://cn2.php.net/distributions/%{name}-%{version}.tar.gz
Source1:                php.init
Source2:                php-fpm.conf
Source3:                php.ini
BuildRoot:              %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:          bzip2-devel, curl-devel, libpng-devel, libjpeg-devel, zlib-devel 
BuildRequires:          libmcrypt-devel, readline-devel,openssl-devel, mhash-devel 
BuildRequires:          libpng, libjpeg, zlib, gd, openssl, freetype, gd-devel, libmcrypt
BuildRequires:          php-mysql, php-pdo, php-common
BuildRequires:          mysql-orbs 
Requires(pre):          shadow-utils
Requires(post):         chkconfig
Requires(preun):        chkconfig,initscripts
Requires(postun):       initscripts 

%description
php

%prep
%setup -q

%build
export DESTDIR=%{buildroot}
./configure \
        --prefix=/data/php \
        --with-config-file-path=/data/php/etc \
        --with-mysql=/data/mysql \
        --with-mysqli=/data/mysql/bin/mysql_config \
        --enable-fpm \
        --with-openssl \
        --with-gd \
        --with-zlib \
        --with-curl \
        --with-libxml \
        --with-png \
        --with-jpeg \
        --with-freetype \
        --with-mcrypt \
        --with-mhash \
        --enable-soap \
        --enable-xml \
        --enable-sockets \
        --enable-safe-mode \
        --enable-bcmath \
        --enable-mbstring 
make 

%install
make install INSTALL_ROOT=%{buildroot}
install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/php
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{php_home}/etc/php-fpm.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{php_home}/lib/php.ini
rm -rf %{buildroot}/.channels/.alias/pear.txt %{buildroot}/.channels/.alias/pecl.txt %{buildroot}/.channels/__uri.reg %{buildroot}/.channels/pear.php.net.reg %{buildroot}/.channels/pecl.php.net.reg %{buildroot}/.depdb %{buildroot}/.depdblock %{buildroot}/.filemap %{buildroot}/.lock %{buildroot}/.channels/.alias/phpdocs.txt %{buildroot}/.channels/doc.php.net.reg >/dev/null 2>&1
rm -rf %{buildroot}/.registry/.channel.pecl.php.net %{buildroot}/.registry/.channel.doc.php.net/ %{buildroot}/.registry/.channel.__uri/ >/dev/null 2>&1
rm -rf %{buildroot}/.channels/ >/dev/null 2>&1
rm -rf %{buildroot}/.registry/ >/dev/null 2>&1

%preun
/sbin/service php stop >/dev/null 2>&1
/sbin/chkconfig --del php
/bin/rm /etc/init.d/php -f >/dev/null 2>&1

%post
chmod +x /etc/init.d/php
/sbin/chkconfig --add php
service php restart >/dev/null 2>&1
grep php  /etc/profile >/dev/null || echo '''PATH=$PATH:/data/php/bin; export PATH''' >>/etc/profile
. /etc/profile 

%postun
rm /data/php -rf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
%{php_home}
%{_initrddir}/php

%changelog
