redis_source:
  file.managed:
    - name: /tmp/redis-2.8.13.tar.gz
    - unless: test -e /tmp/redis-2.8.13.tar.gz
    - source: salt://redis/files/redis-2.8.13.tar.gz

extract_redis:
  cmd.run:
    - cwd: /tmp
    - names: 
      - tar xvf redis-2.8.13.tar.gz
    - unless: test -d redis-2.8.13
    - require:
      - file: redis_source

redis_compile:
  cmd.run:
    - cwd: /tmp/redis-2.8.13/
    - names:
      - make
    - require:
      - cmd: extract_redis
redis_dir:
  cmd.run:
    - names:
      - mkdir -p /data/redis/{etc,database,run,sbin,bin}
    - unless: test -d /data/redis/etc/
    - require:
      - cmd: redis_compile
redis_file:
  cmd.run:
    - names:
      - cp /tmp/redis-2.8.13/src/redis-server /data/redis/sbin/
      - cp /tmp/redis-2.8.13/src/redis-cli /data/redis/bin/
    - unless: test -e /data/redis/sbin/redis-server
    - require:
      - cmd: redis_dir