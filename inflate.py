from KNode import *

home_dir = os.environ['HOME']

kbox_path = home_dir + '/kbox'

def inflate(kn_name,priv_key):
	root  = KNode([line for line in open(kbox_path+"/.kbox/."+kn_name+'.kn','r')])
	root.populate(priv_key,kbox_path)
	
