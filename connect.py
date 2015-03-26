import hashlib 
from my_crypto import encrypt, decrypt
from crypto_sign import key_to_string, string_to_key, sign, verify
import os

home_dir = os.environ['HOME']

kbox_path = home_dir + "/kbox/"
key_path = kbox_path + ".key/"
config_path = kbox_path + ".config"

hostname = None
port = None

delete_token = 'I DELETED THIS FILE'
debug = 0

# set this to hostname of your server
def read_host_info():
    if os.path.isfile(config_path):
        config_file = open(config_path,"r")
	username = config_file.readline()[:-1]
	host_name = config_file.readline()[:-1]
	set_hostname(host_name)
        port_number = config_file.readline()
	set_port(port_number)
	config_file.close()
    else:
        print "Error: hostname was not configured"


##Get the server's hostname
def get_hostname():
    if hostname == None:
	read_host_info()
    return hostname

##Set the server's hostname
def set_hostname(host):
    global hostname
    hostname = host

##Get the port through which we are communicating with the server
def get_port():
    if port == None:
	read_host_info()
    return port

##Set the port through which we are communicating with the server
def set_port(p):
    global port
    port = p

##Pull a file from the server
##  cipher = the server-side filename
##  key = the key under which the contents are encrypted
##  public_keys = a list of the public_keys of users with write access
##
def pull(cipher, key, public_keys):
    
    if debug == 1:
        print "Pulling cipher: "+ cipher
        print "With key: " + key

    ##Pull the file requested and corredponding signature from the server 
    os.system("scp  -q -P " + get_port() + " " + get_hostname() + ":~/kbox/"+cipher + ".enc  /tmp/ ")
    os.system("scp  -q -P " + get_port() + " " + get_hostname() + ":~/kbox/"+cipher + ".sig  /tmp/ ")

    ##Read the signature from its file
    signature_file_name = "/tmp/"+cipher+".sig"
    try:
        signature_file = open("/tmp/"+cipher+".sig", "r")
        signature = signature_file.read()
        signature_file.close()
        sig_file_exists=True
    except IOError as e:
        sig_file_exists=False

    ##Read the encrypted file contents
    encrypted_file_name = "/tmp/"+cipher+".enc"
    try:
        encrypted_file = open(encrypted_file_name, "r")
        encrypted_contents = encrypted_file.read()
        encrypted_file.close()
    except IOError as e:
        ## FILE DOES NOT EXIST                                                         
        if sig_file_exists:
            ##Check to see if the signature is the delete_token                        
            ##i.e. if the file was deleted by a user                                   
            file_deleted = False
            for pub_key_string in public_keys:
                pub_key = string_to_key(pub_key_string)
                if verify(delete_token + '\n' + cipher, signature, pub_key):
                    file_deleted = True
                    break
            if file_deleted:
                print "ERROR: The file you are attempting to pull has been deleted by \
a user"
                return ""
            else:
                ##The signature does not match the delete token for any users          
                print "ERROR: The file was deleted in a invalid manner."
                return ""
        else:
            print "ERROR: Both the file and signature do not exist."
            return ""

    ##Verify that the encrypted contents are signed by a valid user
    if sig_file_exists:
        verified = False
        for pub_key_string in public_keys:
            pub_key = string_to_key(pub_key_string.decode("hex"))
            if verify(encrypted_contents, signature, pub_key):
                verified = True
                break
            if not verified:
                print "Verification failed. This file or signature may have been corrupted"
    else:
        print "WARNING: Signature file does not exist! Verification process will be skipped."

    ##Decrypt the temp file     
    temp_file_name = "/tmp/"+cipher+".enc"
    try:
        decrypt(key,temp_file_name)
    except ValueError as e:
        print "ERROR: Decrpytion failed."
        return ""

    ##Read the decrypted contents
    #print temp_file_name[:-4]
    tempfile = open(temp_file_name[:-4],"r")    
    content = [line for line in tempfile] 
    tempfile.close()

    ##Remove the temp files
    os.remove(temp_file_name)
    os.remove(temp_file_name[:-4])
    if sig_file_exists:
        os.remove(temp_file_name[:-4]+".sig")
    
    return content

##Push a file to the server
##  cipher = the server-side filename
##  content = the contents of the file to be sent
##  key = the key under which the contents should be encrypted
##  challenge = a challenge to prove write-access
##  private_key_string = the private key of the user who is sending the file
##
def push(cipher, content, key, challenge, private_key_string):

    if debug == 1:
        print "Pushing cipher: "+ cipher
        print "With key: " + str(key)
        print "and  challenge: " + challenge
    
    ##Store the text in temp        
    temp_file_name = "/tmp/"+cipher
    tempfile = open(temp_file_name,"w") 
    tempfile.write(content)
    tempfile.close()
    
    ##Encrypt the file in temp
    encrypt(key,temp_file_name)

    ##Read the encrypted contents
    encrypted_file = open(temp_file_name + ".enc", "r")
    encrypted_contents = encrypted_file.read()
    encrypted_file.close()

    ##Sign the encrypted contents
    private_key = string_to_key(private_key_string)
    signature = sign(encrypted_contents, private_key)

    ##Store the signature in a temp file
    temp_sig_file_name = "/tmp/"+cipher+".sig"
    temp_sig_file = open(temp_sig_file_name,"w")
    temp_sig_file.write(signature)
    temp_sig_file.close()

    ##Send to server
    os.system("scp -q  -P " + get_port() + " " + temp_file_name + ".enc " + get_hostname() + ":~/kbox/ " )
    os.system("scp  -q -P " + get_port() + " " + temp_sig_file_name + " " + get_hostname() + ":~/kbox/ " )

    ## Delete temp files   
    os.remove(temp_file_name)
    os.remove(temp_file_name+".enc")
    os.remove(temp_sig_file_name)

##Remove a file from the server
##  cipher = the server-side name of the file to be removed
##
def remove(cipher, priv_key_string):
    if debug == 1:
        print "Removing " + cipher

    ##Prove write access
    ##### TODO

    ##Sign the delete token and put that in the temp signature file
    private_key = string_to_key(priv_key_string)
    signature = sign(delete_token + "\n"+ cipher, private_key)
    temp_sig_file_name = "/tmp/"+cipher+".sig"
    temp_sig_file = open(temp_sig_file_name,"w")
    temp_sig_file.write(signature)
    temp_sig_file.close()

    ##Send the new signature to the server
    os.system("scp -q -P " + get_port() + " " + temp_sig_file_name + " " + get_hostname() + ":~/kbox/ ")

    ##Delete the temp signature file
    os.remove(temp_sig_file_name)

    ##Remove the file from the server
    os.system("ssh -p " + get_port() + " " + get_hostname() + " 'rm ~/kbox/" + cipher + ".enc'")    
    
