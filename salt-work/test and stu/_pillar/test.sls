/tmp/test.conf:
  file.managed:
    - source: salt://fileserver/test.conf.jinja
    - template: jinja
