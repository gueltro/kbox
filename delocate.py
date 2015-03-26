from KNode import *
import os
kbox_path= '/home/gueltro/kbox'


def push_all(root_name,priv_key):
	
 	k = KNode([line for line in open(kbox_path+'/.kbox/'+'.'+root_name+'.kn','r')])
	k.gen_key(priv_key)
	k.get_children()
	
	path = kbox_path+'/'+root_name	
	for file in os.listdir(path):

		if os.path.isfile(path+"/"+file) and '.rem' not in file:
			push_file(path+'/'+file,k,priv_key)

		if os.path.isdir(path+'/'+file) and '.kbox' not in file:
			push_dir(path+'/'+file,k,priv_key)

	push(k.to_cipher(),k.to_text(),k.getKey(),"dfsd",priv_key)	


	
def push_dir(path,parent_knode,priv_key):
	if '.kbox' in path:
		return
	
	path  = os.path.realpath(path)
	name = path.split('/')[-1]
	path_to_parent = '/'.join(path.split('/')[:-1])
	
	if  not os.path.isdir(path_to_parent+'/.kbox'):
		os.mkdir(path_to_parent+'/.kbox')

	#check if there is already a knode for this argument, create it if not 
	if '.'+name+'.kn' in os.listdir(path_to_parent+'/.kbox'):
		k = KNode([line for line in open(path_to_parent+'/.kbox/.'+name+'.kn','r')])		 
	else:
		k = KNode()
		k.name = name
		k.q=1
		k.secret = os.urandom(16).encode('base-64').rstrip()
		k.writers = parent_knode.writers
		k.readers = parent_knode.readers
		k.readers_keys = parent_knode.readers_keys
		k.ws = parent_knode.ws
		k.key = parent_knode.key
		k.dump(path_to_parent)
		k.contents=[]

	k.parent = parent_knode
	k.gen_key(priv_key)

	#update parent with new knode
	if k.name not in [child.name for child in parent_knode.contents]:
		parent_knode.contents += [k]
	else:
		k.get_children()	

	for file in os.listdir(path):

		if os.path.isfile(path+"/"+file) and '.rem' not in file:
			push_file(path+'/'+file,k,priv_key)

		if os.path.isdir(path+'/'+file) and '.kbox' not in file:
			push_dir(path+'/'+file,k,priv_key)

	#push content of the folder	
	push(k.to_cipher(),k.to_text(),k.getKey(),"dfsd",priv_key)	





	
def push_file(path,parent_knode,priv_key):
	if '.rem' in path:
		return
	path  = os.path.realpath(path)
	name = path.split('/')[-1]
	path_to_parent = '/'.join(path.split('/')[:-1])
	

	##check if .kbox folder exists, and create it if not
	if  not os.path.isdir(path_to_parent+'/.kbox'):
		os.mkdir(path_to_parent+'/.kbox')

	#check if there is already a knode for this argument, create it if not 
	if '.'+name+'.kn' in os.listdir(path_to_parent+'/.kbox'):
		k = KNode([line for line in open(path_to_parent+'/.kbox/.'+name+'.kn','r')])		 
	else:
		k = KNode()
		k.name = name
		k.q = 0
		k.secret = os.urandom(16).encode('base-64').rstrip()
		k.writers = parent_knode.writers
		k.readers = parent_knode.readers
		k.readers_keys = parent_knode.readers_keys
		k.ws = parent_knode.ws
		k.key = parent_knode.key
		k.dump(path_to_parent)
	
	k.parent = parent_knode
	k.contents = open(path,"r").read()
	k.gen_key(priv_key)

	#update parent with new knode
	if k.name not in [child.name for child in parent_knode.contents]:
		parent_knode.contents += [k]

	#Push new version of the file
	push(k.to_cipher(),k.to_text(),k.getKey(),"dfsd",priv_key)	
		
