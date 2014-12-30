from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


def generate_key_file(path):
	(public_key, private_key) = generate_key()
	store_key(public_key, private_key,path)

def generate_key():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return (public_key, private_key)

def key_to_string(key):
    return key.exportKey('DER')

def string_to_key(key_string):
    return RSA.importKey(key_string)

def store_key(public_key,private_key,path):
	f = open(path,'w')
	f.write(key_to_string(public_key).encode("hex")+"\n")
	f.write(key_to_string(private_key).encode("hex")+"\n")
	f.close()

def import_key(path):
	f = open(path,'r')
	public_key = f.readline()[:-1].decode("hex")
	private_key =f.readline()[:-1].decode("hex")
	return (public_key,private_key)

def sign(message, private_key):
    h = SHA.new()
    h.update(message)
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(h)
    return signature

# returns true if the signature was valid, false otherwise
def verify(message, signature, public_key):
    h = SHA.new()
    h.update(message)
    verifier = PKCS1_v1_5.new(public_key)
    return verifier.verify(h, signature)
