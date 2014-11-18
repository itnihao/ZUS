<?php
$config = array(
        'center' => array(
                'addr' => '0.0.0.0',
                'port' => '9090',
        ),
        'memcache'      => array(
                'host'  => 'unix:///var/run/memcached/static.sock',
                'port'  => '0',
        ),
        'redis' => array(
                'host'  => '/var/run/redis/redis.sock',
                'port'  => '0',
        ),
);
?>
