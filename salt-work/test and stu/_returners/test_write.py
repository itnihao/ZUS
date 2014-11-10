def __virtual__():
	return 'test_write'

def returner(ret):
	f=open('/tmp/return.txt','a+')
	f.write('aaaaa\n')
	f.close()
