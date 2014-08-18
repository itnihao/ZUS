%define	mysql_user	mysql
%define mysql_home	/data/mysql
%define	mysql_data	%{mysql_home}/data
Name:		mysql
Version:	5.6.20
Release:	1%{?dist}
Summary:	MySQL client programs and shared libraries

Group:		Application/Databases
License:	BSD
URL:		http://www.mysql.com/
Source0:	http://cdn.mysql.com/Downloads/MySQL-5.6/%{name}-%{version}.tar.gz
Source1:	mysql.init
Source2:	my.cnf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 		gperf, perl, readline-devel, openssl-devel
BuildRequires: 		gcc-c++, ncurses-devel, zlib-devel
BuildRequires: 		libtool automake autoconf gawk
BuildRequires: 		perl(Socket)
Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig,initscripts
Requires(postun):	initscripts
Provides:               msqlormysql mysql-server libmysqlclient_16
Obsoletes:              mysql mysql-server libmysqlclient_16
Conflicts:              MySQL-server
AutoReqProv:            no

%description
MySQL is one of the world's most popular open source database

%prep
%setup -q


%build
export DESTDIR=%{buildroot}
cmake \
-DCMAKE_INSTALL_PREFIX=/data/mysql \
-DMYSQL_DATADIR=/data/mysql/data \
-DSYSCONFDIR=/data/mysql/ \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DMYSQL_UNIX_ADDR=/data/mysql/mysql.sock \
-DMYSQL_TCP_PORT=3306 \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1 \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci
make -j %{?_smp_mflags}
mkdir -p /data/mysql
mkdir -p /data/mysql/data

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}/ install
install -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/mysql
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{mysql_home}/my.cnf

%clean
rm -rf %{buildroot}

%pre
grep -q mysql /etc/passwd || %{_sbindir}/groupadd %{mysql_user} >/dev/null 2>&1
grep -q mysql /etc/passwd || %{_sbindir}/useradd -g %{mysql_user} %{mysql_user}>/dev/null 2>&1

%preun
if [ $1 -eq 0 ]; then
    /sbin/service mysql stop >/dev/null 2>&1
    /sbin/chkconfig --del mysql
    /usr/sbin/userdel -f %{mysql_user} >/dev/null 2>&1
    /bin/rm /etc/init.d/mysql -f >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add mysql
chown -R mysql.mysql /data/mysql
./data/mysql/scripts/mysql_install_db --datadir=/data/mysql/data/ --basedir=/data/mysql/ --user=mysql
service mysql restart
ln -s /data/mysql/lib/libmysqlclient.so.18 /usr/lib64/libmysqlclient.so.18 >/dev/null 2>&1
#chmod 664 /data/mysql/binlog -R

%postun
rm -rf /data/mysql 
rm -rf /home/mysql 

%files
%defattr(-,root,root,-)
%doc
%{mysql_home}/
%{_initrddir}/mysql

%changelog