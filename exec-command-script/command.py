#!/usr/bin/env python
#by orbs
import paramiko
import Queue
import getopt
import threading
import sys
import datetime

def usage():
    print '''
        \033[41mExp:\033[0m\n
        \033[42mpython demo.py -F iphost.txt -M 'command'\033[0m\n
    '''

def ssh(queue_get,command):
    try:
        ipaddr=queue_get[0]
        passwd=queue_get[1]
        shport=queue_get[2]
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ipaddr,port=int(shport),username="root",password=passwd)
        stdin,stdout,stderr=ssh.exec_command(command)
        print "--------------------%s--------------------""\033[42msuccess\033[0m\n" %(str(ipaddr))
        ssh.close()
    except Exception,err:
        print "--------------------%s--------------------""\033[41m%s\033[0m" %(ipaddr,err)
        ssh_error=open("error.log","a")
        ssh_error.write("%s\t\t%s\t\t%s\n" %(now,ipaddr,err))
        ssh_error.close()
        pass

if __name__ == '__main__':
    try:
        opts,args=getopt.getopt(sys.argv[1:],"(h)F:M:",["help","cmd=","command="])
        now=datetime.datetime.now()
        if len(sys.argv) == 1:
            usage()
            sys.exit()
        if sys.argv[1] in ("-H","-h","-help"):
            usage()
            sys.exit()
        elif sys.argv[1] in ("-F","--cmd="):
            for opt,arg in opts:
                if opt in ("-F","--cmd="):
                    iphost=arg
                if opt in ("-M","--command="):
                    command=arg
            hosts=open(iphost)
            threads=[]
            sshqueue=Queue.Queue(maxsize=0)
            for host in hosts.readlines():
                if len(host) == 1 or host.startswith('#'):
                    continue
                f=host.split()
                sshqueue.put(f)
            hosts.close()
            for x in xrange(0,sshqueue.qsize()):
                if sshqueue.empty():
                    break
                mutex = threading.Lock()
                mutex.acquire()
                mutex.release()
                threads.append(threading.Thread(target=ssh, args=(sshqueue.get(),command)))
            for t in threads:
                t.start()
                t.join()
        else:
            print "\033[31m error args\033[0m"
    except Exception,err:
            usage()
            print err