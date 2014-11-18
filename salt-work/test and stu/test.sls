testfile:
  file.managed:
    - name: /tmp/test.txt
    - source: salt://fileserver/test.txt
    - template: jinja
    - user: root
    - group: root
    - mode: 644

