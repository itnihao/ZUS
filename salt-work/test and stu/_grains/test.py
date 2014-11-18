def test():
	grains={}
	for line in open("/etc/issue"):
		if "CentOS" in line:
			patch=str(line.split()[2])
	grains['patch']=patch
	return grains
