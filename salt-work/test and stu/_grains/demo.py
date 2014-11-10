#!/usr/bin/env python
import commands
def demo():
	content={}
	content['disk_num'] = commands.getoutput('fdisk -l|grep Disk|wc -l')
	return content
