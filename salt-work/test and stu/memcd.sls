memcached-install:
  pkg.installed:
    - name: memcached
    - require:
      - file: /etc/yum.repos.d/omnslm.repo
  
  service.running:
    - name: memcached
    - enable: True
    - require:
      - pkg: memcached-install
