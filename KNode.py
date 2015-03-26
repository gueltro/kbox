import json
import hashlib
import os
from connect import push,pull
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random


class KNode:

    def __init__(self, strings=None):
        # User-given file or directory name
        self.name =None
        # Secret to identify file
        self.secret = None
        # Bit to determine if this is a file or directory
        self.q = None
        # Write secret
        self.ws = None
        # The ASE key to decrypt the contents
        self.key = None
        # List of public keys of users with read access
        self.readers = None
        # List of ASE keys encrypted under the public key of each user
	self.readers_keys= None
        self.writers = None
        # If directory, contents is a list of KNodes
        # If file, contents is the text contents
        self.contents = None
        # Parent of this KNode (None if this node is the root)
        self.parent =  None
	# Timestamp of last modification
	self.timestamp = None
        # time to parse the
        if strings!=None:
            self.parse_child_block(strings)

	

    def fillup(self):
        if self.q!=0: 
            return False
        else:
            self.contents= "".join(pull(self.to_cipher(),self.getKey(),self.readers))
	
    
    ## Write this KNode in path 
    def dump(self,path):
	if not  os.path.isdir(path + "/.kbox/"):
		os.mkdir(path + "/.kbox/")
	f = open(path + "/.kbox/." +self.name+ ".kn" ,"w")
	f.write(self.this_to_text())
	f.close()
            

    # populate contents of the CNode
    def populate(self,priv_key,path):
	self.dump(path)
    	self.gen_key(priv_key)
	if self.q==1:
	    os.mkdir(path+"/"+self.name)
	    self.get_children()
            for child in self.contents:
                child.parent=self
                child.populate(priv_key,path+"/"+self.name)
    	if self.q==0:
		rem = open(path+"/"+self.name+".rem",'w')
		rem.write("token")	
		rem.close() 

    def get_children(self):
	    self.contents=[]
	    strings=pull(self.to_cipher(),self.getKey(),self.readers)
	    name=strings.pop(0)
            if self.q==1:
                while(1):
                    try:
                        x=KNode(strings)
                        self.contents+=[x]
                    except:
                        break

    def remove_child(self, child, priv_key):
        if self.q != 1:
            print "ERROR: Cannot remove child from a file"
        else:
            for c in self.contents:
                if c == child:
                    print "Removing " + child.name + " from " + self.name
                    self.contents.remove(c)
                    push(self.to_cipher(),self.to_text(),self.getKey(),"",priv_key)
                    return
        print "ERROR: child " + child_name + " not found in " + self.name
            

    def gen_key(self,priv_key):
		
		for cipher in self.readers_keys:			
			tempkey = self.key_decrypt(cipher.decode('hex'),priv_key)
			if tempkey != 0:	
				self.key= tempkey
				return
		self.key="NoPerm"
	
    def key_decrypt(self,ciphertext,priv_key):
	key = RSA.importKey(priv_key)
	dsize = SHA.digest_size
	sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15
	cipher = PKCS1_v1_5.new(key)
	message = cipher.decrypt(ciphertext, sentinel)

	digest = SHA.new(message[:-dsize]).digest()
	if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
		return message[:-dsize]

	else:
                return 0

	

    # Returns the hash of the file name concatenated H(n|s|q)
    def to_cipher(self):
        return hashlib.sha224(self.name+self.secret+str(self.q)).hexdigest()

    # Query server for the file, decrypt, and verify contents
    def get_decrypted_file_and_verify(hashName, ASE):
        pass

    def getKey(self):
        return self.key.decode("hex")

    def parse_child_block(self,strings):
        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="NAME": raise Exception("parse error")
        self.name=S[1].rstrip()

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="BIT": raise Exception("parse error")
        self.q=int(S[1])
        if self.q==1:
            self.contents=[]
        else:
            self.contents=None

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="SECRET": raise Exception("parse error")
        self.secret=S[1].rstrip()

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="WRITERS": raise Exception("parse error")
        self.writers=[st.decode("hex") for st in json.loads(S[1])]

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="READERS": raise Exception("parse error")
        self.readers=[st.decode("hex") for st in json.loads(S[1])]

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="WS": raise Exception("parse error")
        self.ws=json.loads(S[1])

        s=strings.pop(0)
        S=s.split(":")
        if S[0]!="KEY": raise Exception("parse error")
        #print "readers_keys"+S[1]
        self.readers_keys=[st.decode("hex") for st in json.loads(S[1])]

    def this_to_text(self):
        s=""
        s+="NAME:"
        s+=self.name
        s+="\n"

        s+="BIT:"
        s+=str(self.q)
        s+="\n"

        s+="SECRET:"
        s+=self.secret
        s+="\n"

        s+="WRITERS:"
        hex_writers=[st.encode("hex") for st in self.writers]
	s+=json.dumps(hex_writers, ensure_ascii=False)
        s+="\n"

        s+="READERS:"
	hex_readers=[st.encode("hex") for st in self.readers]
        s+=json.dumps(hex_readers, ensure_ascii=False)
        s+="\n"

        s+="WS:"
        s+=json.dumps(self.ws, ensure_ascii=False)
        s+="\n"

        s+="KEY:"
	hex_readers_keys= [st.encode("hex") for st in self.readers_keys]
        s+=json.dumps(hex_readers_keys, ensure_ascii=False)
        s+="\n"

        return s

    def to_text(self):
        if self.q==0:
            s=""
            if self.contents!=None:
                s+=self.contents
        else:
            s="NAME:"+self.name+"\n"
            for i in self.contents:
                s+=i.this_to_text()
        return s

    ##Set permission recursively on current knode
    def set_perm(self,new_readers,password,priv_key):

	new_readers_keys = []
	for pub_s in new_readers:
		
		##Encrypt AES key under each reader public key
		message = hashlib.sha256(password).hexdigest() 
		h = SHA.new(message)
		key = RSA.importKey(pub_s)
		cipher = PKCS1_v1_5.new(key)
		ciphertext = cipher.encrypt(message+h.digest()).encode("hex")
		new_readers_keys.append(ciphertext)
	
	##Apply permission to children
        self.set_perm_rec(new_readers,new_readers_keys,priv_key,message)

    def set_perm_rec(self,new_readers,new_readers_keys,priv_key,message):
	self.readers = new_readers 
	self.readers_keys = new_readers_keys
        self.key=message
        push(self.parent.to_cipher(),self.parent.to_text(),self.parent.getKey(),"",priv_key)
	push(self.to_cipher(),self.to_text(),self.getKey(),"",priv_key)
	
	if self.q == 0:
		return
			
	for child in self.contents:
		child.set_perm_rec(new_readers,new_readers_keys,priv_key,message)
	

 
