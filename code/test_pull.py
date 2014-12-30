from crypto_sign import *
from KNode import *
from inflate import *

(pub_key,priv_key) =  import_key("/home/gueltro/kbox/.key/giulio") 

inflate('zero',priv_key)


