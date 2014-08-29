repository
===
搭建本地网络YUM
```
/data/repo/6.5/x86_64/目录下存放定制的RPM包

createrepo -o /data/repo/6.5/x86_64/
命令用于创建本地源
```

Nginx环境
```
/data/nginx/conf.d/repo.conf
```

```
orbs.repo客户端repo文件
192.168.1.10假设为YUM服务器IP
```