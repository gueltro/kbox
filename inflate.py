from KNode import *
kbox_path = "/home/gueltro/kbox"

def inflate(kn_name,priv_key):
	root  = KNode([line for line in open(kbox_path+"/.kbox/."+kn_name+'.kn','r')])
	root.populate(priv_key,kbox_path)
	
