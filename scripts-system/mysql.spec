Name: mysql
Version:5.6.21
Release: %(echo $RELEASE)%{?dist}
License: GPL
URL: http://downloads.mysql.com/archives/get/file/mysql-5.5.37.tar.gz
Group: applications/database
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root 
BuildRequires: cmake
Packager: wangheng.wh@alibaba-inc.com
Autoreq: no
#Source: %{name}-%{version}.tar.gz
prefix: /usr/local/mysql
Summary: MySQL 5.6.21

%description 
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software.

%define MYSQL_USER mysql
%define MYSQL_GROUP mysql
%define __os_install_post %{nil}

%build
cd $OLDPWD/../
CFLAGS="-O3 -g -fno-exceptions -static-libgcc -fno-omit-frame-pointer -fno-strict-aliasing"
CXX=g++
CXXFLAGS="-O3 -g -fno-exceptions -fno-rtti -static-libgcc -fno-omit-frame-pointer -fno-strict-aliasing"
export CFLAGS CXX CXXFLAGS

cmake .                                                  \
  -DSYSCONFDIR:PATH=%{prefix}                            \
  -DCMAKE_INSTALL_PREFIX:PATH=%{prefix}                  \
  -DCMAKE_BUILD_TYPE:STRING=Release                      \
  -DENABLE_PROFILING:BOOL=ON                             \
  -DWITH_DEBUG:BOOL=OFF                                  \
  -DWITH_VALGRIND:BOOL=OFF                               \
  -DENABLE_DEBUG_SYNC:BOOL=OFF                           \
  -DWITH_EXTRA_CHARSETS:STRING=all                       \
  -DWITH_SSL:STRING=bundled                              \
  -DWITH_UNIT_TESTS:BOOL=OFF                             \
  -DWITH_ZLIB:STRING=bundled                             \
  -DWITH_PARTITION_STORAGE_ENGINE:BOOL=ON                \
  -DWITH_INNOBASE_STORAGE_ENGINE:BOOL=ON                 \
  -DWITH_ARCHIVE_STORAGE_ENGINE:BOOL=ON                  \
  -DWITH_BLACKHOLE_STORAGE_ENGINE:BOOL=ON                \
  -DWITH_PERFSCHEMA_STORAGE_ENGINE:BOOL=ON               \
  -DDEFAULT_CHARSET=utf8                                 \
  -DDEFAULT_COLLATION=utf8_general_ci                    \
  -DWITH_EXTRA_CHARSETS=all                              \
  -DENABLED_LOCAL_INFILE:BOOL=ON                         \
  -DWITH_EMBEDDED_SERVER=0                               \
  -DINSTALL_LAYOUT:STRING=STANDALONE                     \
  -DCOMMUNITY_BUILD:BOOL=ON                              \
  -DMYSQL_SERVER_SUFFIX='-r5436';

make -j `cat /proc/cpuinfo | grep processor| wc -l`

%install
cd $OLDPWD/../
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, %{MYSQL_USER}, %{MYSQL_GROUP})
%attr(755, %{MYSQL_USER}, %{MYSQL_GROUP}) %{prefix}/*

%pre

%post
ln -s %{prefix}/lib %{prefix}/lib64

%preun

%changelog