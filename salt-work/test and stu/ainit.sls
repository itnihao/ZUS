omnslm-repo:
  file.managed:
    - name: /etc/yum.repos.d/omnslm.repo
    - source: salt://fileserver/ainit/omnslm.repo
    - user: root
    - group: root
    - mode: 644

base-repo:
  file.managed:
    - name: /etc/yum.repos.d/CentOS-Base.repo
    - source: salt://fileserver/ainit/CentOS-Base.repo
    - user: root
    - group: root
    - mode: 644

disable-service:
  service.dead:
    - names:
      - rpcbind
      - qpidd
      - portmap
      - acpid
      - atd
      - cups
      - haldaemon
      - ipv6tables
      - nfslock
      - sendmail
      - bluetooth
      - rpcidmapd
      - yum-updatesd
postfix-disable:
  pkg.removed:
    - name: postfix
    - name: nfs-utils

base-package:
  pkg.installed:
    - names:
      - lrzsz
      - nc
      - python-redis
      - sysstat
      - screen
      - ntp
    - require:
      - file: /etc/yum.repos.d/CentOS-Base.repo
      - file: /etc/yum.repos.d/omnslm.repo

iptables:
  file.managed:
    - name: /etc/sysconfig/iptables
    - source: salt://fileserver/ainit/iptables
    - user: root
    - group: root
    - mode: 600
  service:
    - running
    - watch:
      - file: /etc/sysconfig/iptables

sshd:
  service:
    - running
    - enable: True
    - relaod: True
    - watch:
      - file: /etc/ssh/sshd_config
    - require:
      - file: /etc/ssh/sshd_config
  file.managed:
    - name: /etc/ssh/sshd_config
    - source: salt://fileserver/ainit/sshd_config
    - user: root
    - group: root
    - mode: 600

dns-service:
  file.managed:
    - name: /etc/resolv.conf
    - source: salt://fileserver/ainit/resolv.conf
    - user: root
    - group: root
    - mode: 644

sudo-service:
  file.managed:
    - name: /etc/sudoers
    - source: salt://fileserver/ainit/sudoers
    - user: root
    - group: root
    - mode: 440

modprobe-conf:
  file.managed:
    - name: /etc/modprobe.d/modprobe.conf
    - source: salt://fileserver/ainit/modprobe.conf
    - user: root
    - group: root
    - mode: 644

limits-conf:
  file.managed:
    - name: /etc/security/limits.conf
    - source: salt://fileserver/ainit/limits.conf
    - user: root
    - group: root
    - mode: 644

selinux-conf:
  cmd.wait:
    - name: /usr/sbin/setenforce 0
    - watch:
      - file: /etc/selinux/config
  file.managed:
    - name: /etc/selinux/config
    - source: salt://fileserver/ainit/selinux-config
    - user: root
    - group: root
    - mode: 644

sysctl-conf:
  cmd.wait:
    - name: /sbin/sysctl -p
    - watch:
      - file: /etc/sysctl.conf
  file.managed:
    - name: /etc/sysctl.conf
    - source: salt://fileserver/ainit/sysctl.conf
    - user: root
    - group: root
    - mode: 644

profile:
  file.managed:
    - name: /etc/profile
    - source: salt://fileserver/ainit/profile
    - user: root
    - group: root
    - mode: 644

rclocal-conf:
  file.managed:
    - name: /etc/rc.d/rc.local
    - source: salt://fileserver/ainit/rc.local
    - user: root
    - group: root
    - mode: 755

