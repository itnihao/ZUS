#!/usr/bin/python
#coding:utf-8
import paramiko
import sys
import datetime
import threading
import Queue
import getopt
from termcolor import colored
def usage():
	print colored("e.g.",'red')
	print colored("exp:",'red')
	print colored("\tpython demo.py -c iplistfile -m command",'blue')
	print colored("iplistfile.",'red')
	print colored("\tipaddress sshport sshpasswd",'blue')
def ssh(queue_get,cmd):
	try:
		ipaddr=queue_get[0]
		ipport=queue_get[1]
		passwd=queue_get[2]
		socket=paramiko.SSHClient()
		socket.load_system_host_keys()
		socket.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		socket.connect(hostname=ipaddr,port=ipport,username='root',password=passwd)
		stdin,stdout,stderr=socket.exec_command(cmd)
		if str(stderr.read()) == "":
			print colored("%s----------[%s] :)",'green') %(str(ipaddr),cmd)
			ssh_info_log=open("loginfo.log","a")
			ssh_info_log.write("%s\t[%s]\tsucc\n" %(ipaddr,cmd))
			ssh_info_log.close()
		else:
			print colored("%s----------exec[%s] :(",'red') %(str(ipaddr),cmd)
			ssh_info_log=open("loginfo.log","a")
			ssh_info_log.write("%s\t[%s]\tfaild\n" %(ipaddr,cmd))
			ssh_info_log.close()
		socket.close()
	except Exception,err:
		print colored("%s----------[%s] :(",'red') %(str(ipaddr),err)
		ssh_info_log=open("loginfo.log","a")
		ssh_info_log.write("%s\t[%s]\n" %(ipaddr,err))
		ssh_info_log.close()
		pass

if __name__ == '__main__':
	try:
		opts,args= opts, args = getopt.getopt(sys.argv[1:], "(hH)c:m:", ["help","cmd=","command=",])
		if len(sys.argv) == 1:
			usage()
			sys.exit()
		if sys.argv[1] in ("-h","-H","--help"):
			usage()
			sys.exit()
		elif sys.argv[1] in ("-c","--cmd"):
			for opt,arg in opts:
				if opt in ("-c","--cmd"):
					iplist=arg
				if opt in ("-m","--command="):
					cmd=arg
			file=open(iplist)
			threads = []
			myqueue = Queue.Queue(maxsize = 0)
			for line in file.readlines():
				if len(line) == 1:
					continue
				ipline=line.split()
				myqueue.put(ipline)
			file.close()
			for x in xrange(0,myqueue.qsize()):
				if myqueue.empty():
					break
				mutex = threading.Lock()
				mutex.acquire()
				mutex.release()
				threads.append(threading.Thread(target=ssh,args=(myqueue.get(),cmd)))
			for t in threads:
				t.start()
				t.join()
		else:
			print "args error"
	except Exception,err:
		usage()
		print err
