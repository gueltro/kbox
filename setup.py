from  KNode import *
from crypto_sign import *
from Crypto.Cipher import PKCS1_v1_5

kbox_path = "/home/gueltro/kbox/"
key_path = kbox_path + ".key/"


## Interactive setup for a root directory
def setup_root(key_name=None):
	
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
	

	
