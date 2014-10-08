#!/usr/bin/env python 
#by orbs
#version 
#email 
#doc
from processing import Process,Queue
import paramiko,sys,os
from termcolor import colored

#def USAGE():
#	print '''
#		\033[41mExp:\033[0m\n
#		\033[41mExec command\033[0m\t\t\033[42mpython demo.py -C iphost command\033[0m\n
#		\033[41mUpload file\033[0m\t\t\033[42mpython demo.py -F iphost sourcefile destdir\033[0m\n
#		\033[41mFormat iphost:\033[0m\t\t\033[42m10.0.0.1 57522 passwd\033[0m\n
#		\033[41mFormat command:\033[0m\t\t\033[42mone command per line\033[0m
#	'''

def USAGE():
	print colored("Exp:\n",'red')
	print colored("Exec command\t\tpython demo.py -C iphost command\n",'blue')
	print colored("Upload file\t\tpython demo -F iphost sourcefile destdir\n",'blue')

def SSH(queue,command):
	try:
		ipaddr=queue[0]
		sshport=queue[1]
		passwd=queue[2]
		ssh=paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=ipaddr,port=int(sshport),username='root',password=passwd)
		stdin,stdout,stderr=ssh.exec_command(command)
		if str(stderr.read()) == "":
			print colored("----------%s----------[%s] :)",'green') %(str(ipaddr),command)
		else:
			print colored("----------%s----------exec[%s] :(",'red') %(str(ipaddr),command)
		ssh.close()
	except Exception,err:
		print colored("----------%s----------%s",'red') %(str(ipaddr),err)

def TRANS(queue,source,destdir):
	try:
		ipaddr=queue[0]
		sshport=queue[1]
		passwd=queue[2]
		trans=paramiko.Transport((ipaddr,int(sshport)))
		trans.connect(username='root',password=passwd)
		sftp=paramiko.SFTPClient.from_transport(trans)
		sftp.put(os.path.join(os.getcwd(),source),os.path.join(destdir,source))
		print colored("----------%s----------upload %s sucess :)",'green') %(str(ipaddr),source)
		trans.close()
	except Exception,err:
		print colored("----------%s----------",'red') %err

def exe():
	queue=Queue()
	hostfile_line=open(sys.argv[2],'r').readlines()
	command_file=open(sys.argv[3],'r').readlines()
	for command_line in command_file:
		command_list=command_line.split('\n')
		command=''.join(command_list)
		for hostfile in hostfile_line:
			eachline=hostfile.split()
			queue.put(eachline)
			eachline=Process(target=SSH,args=(queue.get(),str(command)))
			eachline.start()
	eachline.join()

def load():
	queue=Queue()
	hostfile_line=open(sys.argv[2],'r').readlines()
	source=sys.argv[3]
	destdir=sys.argv[4]
	for hostfile in hostfile_line:
		eachline=hostfile.split()
		queue.put(eachline)
		eachline=Process(target=TRANS,args=(queue.get(),source,destdir))
		eachline.start()
	eachline.join()
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		USAGE()
		sys.exit()
	if sys.argv[1] == '-C':
		exe()
	elif sys.argv[1] == '-F':
		load()
	else:
		USAGE()
		sys.exit()
