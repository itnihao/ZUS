#!/usr/bin/env python
#coding=utf8

import urllib2,sys,json,argparse
from urllib2 import URLError
class zabbix_tools:
	def __init__(self):
		self.url=("http://10.0.5.216/zabbix/api_jsonrpc.php")
		self.header={"Content-Type":"application/json"}

	def user_login(self):
		data = json.dumps({
			"jsonrpc":"2.0",
			"method":"user.login",
			"params":{"user":"kongzz","password":"kongzz"},
			"id":0
			})
		request=urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])
		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			print "\033[041m 用户认证失败，请检查 !\033[0m", e.code
		else:
			response=json.loads(result.read())
			result.close()
			self.authID=response['result']
			return self.authID

	def get_host(self,hostip=""):
		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"host.get",
			"params":{"output":"extend","filter":{"host":hostip}},
			"auth":self.user_login(),
			"id":1,
			})
		request=urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key, self.header[key])
		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			if hasattr(e,'reason'):
				print "Failed to reach zabbix server",e.reason
			elif hasattr(e,'code'):
				print "The zabbix cannot fulfil the request", e.code
		else:
			response=json.loads(result.read())
			result.close()
			if len(response['result']) == 0:
				print "HostName: \033[31m%s 没有添加\033[0m " %hostip
			else:
				for host in response['result']:
					status={"0":"OK","1":"Disabled"}
					available={"0":"Unknown","1":"Available","2":"Unavailable"}
					if len(hostip) == 0:
						print "HostID: %s\t HostName:%s\t Status:\033[32m%s\033[0m\t Available: \033[31m%s\033[0m" %(host['hostid'],host['name'],status[host['status']],available[host['available']])
					else:
						print "HostID: %s\t HostName:%s\t Status:\033[32m%s\033[0m\t Available: \033[31m%s\033[0m" %(host['hostid'],host['name'],status[host['status']],available[host['available']])
						return host['hostid']

	def get_template(self,template_name=""):
		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"template.get",
			"params":{"output":"extend","filter":{"name":template_name}},
			"auth":self.user_login(),
			"id":1,
			})
		request=urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])
		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			print "Error is: ",e
		else:
			response=json.loads(result.read())
			result.close()
			for temp in response['result']:
				if len(template_name) == 0:
					print "Template: \033[31m%s\033[0m\t ID: %s" %(temp['name'],temp['templateid'])
				else:
					self.templateID=response['result'][0]['templateid']
					print "Template Name: \033[31m%s\033[0m " %template_name
					return response['result'][0]['templateid']

	def get_group(self,group_name=""):
		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"hostgroup.get",
			"params":{"output":"extend","filter":{"name":group_name}},
			"auth":self.user_login(),
			"id":1,
			})
		request=urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])

		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			print "Error is:", e
		else:
			response=json.loads(result.read())
			result.close()
			for grp in response['result']:
				if len(group_name) == 0:
					print "Group: \033[31m%s\033[0m\t GroupID: %s" %(grp['name'],grp['groupid'])
				else:
					print "Group: \033[31m%s\033[0m\t GroupID: %s" %(grp['name'],grp['groupid'])
					self.groupID=grp['groupid']
					return grp['groupid']

	def del_host(self,hostid):
		hostid_list=[]
		for i in hostid.split(','):
			var={}
			var['hostid']=self.get_host(i)
			hostid_list.append(var)

		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"host.delete",
			"params":hostid_list,
			"auth":self.user_login(),
			"id":1
			})
		request=urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])

		try:
			result=urllib2.urlopen(request)
		except Exception as e:
			print "Error is: ",e
		else:
			result.close()
			print "Host: \033[041m %s \033[0m\t删除完毕" %hostid

	def create_host(self,hostip,group_name,template_name):
		if self.get_host(hostip):
			print "\033[041m主机 %s 已经添加\033[0m" %hostip
			sys.exit(1)
		group_list=[]
		template_list=[]
		for i in group_name.split(','):
			var={}
			var['groupid']=self.get_group(i)
			group_list.append(var)
		for i in template_name.split(','):
			var={}
			var['templateid']=self.get_template(i)
			template_list.append(var)
		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"host.create",
			"params":{
				"host":hostip,
				"interfaces":[{
					"type":1,
					"main":1,
					"useip":1,
					"ip":hostip,
					"dns":"",
					"port":"10050",
					}],
				"groups":group_list,
				"templates":template_list,
				},
			"auth":self.user_login,
			"id":1
			})
		request = urllib2.Request(self.url, data)
		for key in self.header:
			request.add_header(key,self.header[key])

		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			print "Error is:", e
		else:
			response=json.loads(result.read())
			resutl.close()
			print "添加主机: \033[42m%s\031[0m \t ID: \033[31m%s\033[0m" %(hostip,response['result']['hostids'])

	def host_disable(self,hostip):
		data=json.dumps({
			"jsonrpc":"2.0",
			"method":"host.update",
			"params":{"hostid":self.get_host(hostip),"status":1},
			"auth":self.user_login(),
			"id":1
			})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])

		try:
			result=urllib2.urlopen(request)
		except URLError as e:
			print "Error is:", e
		else:
			response=json.loads(result.read())
			result.close()
			print "主机目前状态:"
			print self.get_host(hostip)


if __name__ == '__main__':
	zabbix=zabbix_tools()
	parser=argparse.ArgumentParser(description='zabbix api ',usage='%(prog)s [options]')
	parser.add_argument('-H','--host',nargs='?',dest='hostlist',default='host',help='查询全部主机信息')
	parser.add_argument('-G','--group',nargs='?',dest='grouplist',default='group',help='查询全部主机群组信息')
	parser.add_argument('-T','--template',nargs='?',dest='templatelist',default='template',help='查询全部模版信息')
	parser.add_argument('-C','--add-host',dest='addhost',help='添加主机,多个主机之间使用分号')
	parser.add_argument('-D','--delete',dest='deletehost',nargs='+',help='删除主机,多个主机之间使用分号')
	parser.add_argument('-d','--disable',dest='disablehost',nargs=1,help='禁用主机')
	parser.add_argument('-v','--version',action='version',version='%(prog)s 1.0.1')
	if len(sys.argv) == 1:
		print parser.print_help()
	else:
		args=parser.parse_args()
		if args.hostlist != 'host':
			if args.hostlist:
				zabbix.get_host(args.hostlist)
			else:
				zabbix.get_host()
		if args.grouplist != 'group':
			if args.grouplist:
				zabbix.get_group(args.grouplist)
			else:
				zabbix.get_group()
		if args.templatelist != 'template':
			if args.templatelist:
				zabbix.get_template(args.templatelist)
			else:
				zabbix.get_template()
		if args.addhost:
			zabbix.create_host(args.addhost[0],args.addhost[1],args.addhost[2])
		if args.deletehost:
			zabbix.del_host(args.deletehost[0])
		if args.disablehost:
			zabbix.host_disable(args.disablehost)
