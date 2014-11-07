#!/usr/bin/env python
#coding=utf-8
import urllib2,json,sys
from termcolor import colored

def help():
	print colored("Exp:\n",'red')
	print colored("python demo.py -f iplist.txt\n",'blue')
	print colored("python demo.py -c ipaddr\n",'blue')

def figure(ipaddr):
	url="http://ip.taobao.com/service/getIpInfo.php?ip="
	addr=url + ipaddr
	try:
		result=urllib2.urlopen(addr,timeout=10).readline()
		content=json.loads(result,encoding="utf-8")
		if content['code'] == 0:
			print content['data']['ip']+ ' '+ content['data']['country']
		else:
			print 'urllib content return code not 0'
	except:
		print "urllib read faild"

if __name__ == '__main__':
	if len(sys.argv) == 1:
		help()
		sys.exit()
	if sys.argv[1] == '-f':
		ipf=open(sys.argv[2],'r').readlines()
		for ip in ipf:
			figure(ip)
	elif sys.argv[1] == '-c':
		ip=sys.argv[2]
		figure(ip)
	else:
		help()
		sys.exit()
