security-file:
  file.managed:
    - name: /data/web/security.tar.gz
    - source: salt://fileserver/security/security.tar.gz
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /data/web && tar xf security.tar.gz && touch /var/run/tar.lock
    - unless: test -f /var/run/tar.lock

daemontools:
  file.managed:
    - name: /data/web/daemontools-0.76-uuzu.0.1.x86_64.rpm
    - source: salt://fileserver/security/daemontools-0.76-uuzu.0.1.x86_64.rpm
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /data/web  && rpm -i daemontools-0.76-uuzu.0.1.x86_64.rpm
    - unless: which supervise

security-run:
  cmd.run:
    - name: cd /data/web && sh start_security.sh && touch /var/run/start-security.lock
    - unless: test -f /var/run/start-security.lock

