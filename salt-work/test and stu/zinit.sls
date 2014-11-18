config_center:
  file.managed:
    - name: /data/config/config_center.php
    - source: salt://fileserver/php-fpm/config_center.php
    - user: root
    - group: root
    - mode: 644

nslm-dir:
  file.directory:
    - name: /data/nslm_log
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

centerlog-dir:
  file.directory:
    - name: /data/nslm_log/center_log
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
    
socket-dir:
  file.directory:
    - name: /data/nslm_log/socket_log
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
queue-dir:
  file.directory:
    - name: /data/nslm_log/queue_log
    - user: nobody
    - group: nobody
    - file_mode: 644
    - dir_mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

uuzuback:
  file.managed:
    - file: /etc/uuzuback.conf
    - source: salt://fileserver/uuzuback.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644
