from  KNode import *
from crypto_sign import *
from inflate import inflate
from setup import setup_root
from  connect import *
from delocate import *
import sys
import os

home_dir = os.environ['HOME']

kbox_path = home_dir + '/kbox'

#(pub_key,priv_key) =  import_key(home_dir + "/kbox/.key/") 


order = sys.argv[1]
try:
	argument = sys.argv[2]
except:
	argument = ''


#orders = ['show-roots','show','push','pull','']

def pull_file(argument):
		argument = os.path.realpath(argument)
		path = '/'.join(argument.split('/')[:-1])+'/.kbox/.'+argument.split('/')[-1][:-4]+'.kn'
		#print "Pulling "+ path+'...'
		strings = [line for line in open(path,'r')]
		k = KNode(strings)
		k.gen_key(priv_key)
		k.fillup()
		os.remove(argument)
		f = open(argument[:-4],'w')
		f.write(k.contents)
		f.close


def pull_dir(argument):
	for file in os.listdir(argument):
		newargument = argument +'/'+file
		
		if os.path.isdir(newargument) and '.kbox' not in argument :
			pull_dir(newargument)
		if os.path.isfile(newargument) and '.rem' not in argument:
			pull_file(newargument)


if order == 'show-roots':
	for file in os.listdir(kbox_path+'/.kbox'):
		print file[1:-3]
		
		
if order == 'show' and '.'+argument+'.kn' in os.listdir(kbox_path+'/.kbox'):
	inflate(argument,priv_key)
	
if order == 'pull':
	argument = os.path.realpath(argument)
	if os.path.isfile(argument):
		pull_file(argument)
	if os.path.isdir(argument):
		pull_dir(argument)



if order == 'push' or order =='free' and os.path.isfile(argument) or os.path.isdir(argument) and '.kbox' not in argument:
	argument = os.path.realpath(argument)
	parent_path = path = '/'.join(argument.split('/')[:-2])+'/.kbox/.'+argument.split('/')[-2]+'.kn'
	k = KNode([line for line in open(parent_path,'r')])
	k.gen_key(priv_key)
	k.get_children()	
	if os.path.isfile(argument) and '.rem' not in argument:
		push_file(argument,k,priv_key)
	if os.path.isdir(argument) and '.kbox' not in argument:
		push_dir(argument,k,priv_key)
	push(k.to_cipher(),k.to_text(),k.getKey(),"dfsd",priv_key)
	if order =='free':
		os.remove(argument)
		open(argument+'.rem', 'a').close()


if order == 'setup':
        setup_identity() 

if order == 'mkroot':
        try:
            arg = sys.argv[2]
        except:
            arg = ""
	setup_root(arg)

if order == 'help':
	os.system('cat ~/kbox/fresh/README')

