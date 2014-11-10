/tmp/demo.txt:
  file.managed:
    - source: salt://fileserver/demo.txt
    - user: root
    - group: root
    - mode: 644
