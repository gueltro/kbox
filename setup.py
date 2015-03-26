from  KNode import *
from crypto_sign import *
from Crypto.Cipher import PKCS1_v1_5
import os

home_dir = os.environ['HOME']

kbox_path = home_dir + "/kbox/"
key_path = kbox_path + ".key/"
host_path = kbox_path + ".host"


## Interactive setup for the new identity of the user
def setup_identity():
        if not os.path.isdir(kbox_path):
            os.mkdir(kbox_path)
	if not os.path.isdir(key_path):
		os.mkdir(key_path)
	
        setup_public_key()	
        setup_host()

def setup_host():
    if os.path.isfile(host_path):
       os.remove(host_path)

    host_file = open(host_path,"w") 
    host_name = raw_input("Please enter the host name of the ssh server that you want to use for storage (i.e. bob@1.1.2.3): ") 
    port_number = raw_input("Insert the number of the port where ssh is listening (i.e. 22): ")
    host_file.write(host_name + '\n' + port_number)
    host_file.close()

    permission = raw_input("Would you like to add your ssh key to the server's list of authorized keys? Doing so will enable you to push and pull files using the kbox system without typing the password to your account on the server each time. [See the readme for more info] (y/n) ")

    if permission.lower() == 'y':
	    os.system("cat .ssh/id_rsa.pub | ssh -p " + port_number + " " + host_name + " 'cat >> .ssh/authorized_keys'")
    
    print "Creating kbox directory on the server..."
    os.system("ssh -p " + port_number + " " + host_name + " 'mkdir $HOME/kbox'"


## Interactive setup for a root directory
def setup_root(key_name=None):

        if not os.path.isdir(kbox_path):
            os.mkdir(kbox_path)
	if not os.path.isdir(key_path):
		os.mkdir(key_path)
	if key_name == None:	
		key_name = setup_public_key()	
	if key_name == None:
		return

	(pub_key,priv_key) = import_key(key_path+key_name) 
	x = KNode()

	##Setup knode

	x.name =  raw_input("Pick a name for the root directory you are creating: ")
	x.secret = os.urandom(16).encode("hex")
	x.q = 1
	x.readers = [pub_key.encode("hex")]
	x.readers_keys =[key_encrypt(pub_key)]	
	x.writers=[]
	x.ws=""
	x.contents = []
			
	x.dump(kbox_path)

	x.gen_key(priv_key)
	push(x.to_cipher(),x.to_text(),x.getKey(),"",priv_key)
	os.mkdir(kbox_path+x.name)
	return x	

## Interactive setup for a public key
def setup_public_key():
		while 1:	
			ans = raw_input("Do you want to create a new public key to associated with this knode? (y/n)" ).lower()
			if ans == "y":
				key_name = raw_input("Pick a name for this key: ")
				try:
					generate_key_file(key_path+key_name)
					print "Created new public key: "+key_name
					return key_name
				except:
					print "Error in creating public key"
					return None
					
			if ans == "n":
				"A public key is necessary to create a knode"
				return None 
			else:
				print "your answer must be y or n"



def key_encrypt(pub_key):
	##Generate AES key (message),  encrypt  under each reader public key	
	message = hashlib.sha256(os.urandom(16).encode("hex")).hexdigest()  
	h = SHA.new(message)
	key = RSA.importKey(pub_key)
	cipher = PKCS1_v1_5.new(key)
	ciphertext = cipher.encrypt(message+h.digest()).encode("hex")
	return ciphertext
	

	
