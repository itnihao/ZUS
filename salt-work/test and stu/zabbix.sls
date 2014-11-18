zabbix-install:
  pkg.installed:
    - name: zabbix-agent
    - require:
      - file: /etc/yum.repos.d/omnslm.repo

zabbix-agent-conf:
  file.managed:
    - name: /etc/zabbix/zabbix_agentd.conf
    - source: salt://fileserver/zabbix/zabbix_agentd.conf
    - template: jinja
    - user: nobody
    - group: nobody
    - require:
      - pkg: zabbix-install
  service.running:
    - name: zabbix-agent
    - enable: True
    - watch:
      - file: /etc/zabbix/zabbix_agentd.conf
    - require:
      - pkg: zabbix-install

