#
# Author: Shankar, K
#   Demonstration of RSA in its Raw form
#   1. Asserting n = p1 * p2
#   2. 
#
from Crypto.PublicKey.RSA import *
import ast
import base64

f = open('/root/kp-adcaas-shankar.pem','r')
k = importKey(f.read())
print (' n = ', hex(k.n), 'd = ', hex(k.d),'e = ',hex(k.e))
print
#print(dir(k), k.__dict__)

p1 = long('bf59310903b36db3e3acb5d588d1e37b4a4a729e188b5f5289133ae7d513b0ee88e3849ac1dfcfadb30ad17404c81d91ede412befc9a3ae8f6c0fac8cbe8691cfdd9adcca25b1f5113ab9066791b9dae37cd840be3a3bb398c00e880111042b8113402a53dd2fde3ff671bb2896dd7f58e241616639f46dda89fe2a0dd3b870b',16)
p2 = long('bc795fb4eada46072b53a572c395e38edf4165242d63735ce736735cf7e3db05b1bfad7e265b6ef6041cfbd5afc673d67b5b123ea2778fbbf195e94ad1174199b1d8ac45c290cd979d31d71ec16e57b5b1c6704b009994c7f40b406ab607a503c7ad7e0c809d557393d51caaa7f2cb329d41d652ae416e205bdee8f445273243',16)
n = int('8ce038b41f6e0432e362ce49a093cafbfe3c6d28c50acf69a81cc5b5742a9d947c72388ce9fc952d9ea9a979af32e12cd0d9593a4048e21ad02017041311edeb8638ead8cd14cf7d11d8649879c3041d766faad3b2635b5f12f3196d284a34af1d1d649e98a0b48a16507467a2c769b5913d305292fe6aac579f0a6a5652f115867e4681910b47ca465adf98e82b1ddb1f71e5a2ec45784976d94fb8770b4830ab6a0f955747976d7a24ac6b7a8ac5ad6b639fc7141684b92467c81b4f923cd410c311b4f5c2fe86746bab4bf555fb7086a7b4813802416d733e05d65fcf416e40f25b623bbaf6c87fa396ca746ea4c1828a47920beb073411e7294310a17de1', 16)

assert(n == p1*p2)

e = long('10001', 16)
pubkey = construct((n, e))

data = 21598237325283972L
c = pubkey.encrypt(data,0)[0]
#c = pow(data, e, n)

print('encrypted data ' , c)

d=long('815152bc061df7bcbefef45ea209094c49152f1f3dc1aea44eae1acf76d3a7d3a6693380274ab5a62aff9393204094738f43f5a4835e643038dd3c43813df429400cff8804ba15bdb9a3eab40d11f7b514036dcce6f44debf8792fde041e1a3ea57b55e2403945817cfa5de0c48c497d62d5c88604698782acec51a34b9ad7b28e1911c18467c282354de2281cd433dd9ddc90e0a7d0e23381d25762d5bd480e337859d8e0177569c094603fa07ee37c757b073be72f6fa123825dd0b31bd9051f15397d01786bb366d031673c120d7b86b59ab1403489698ed536f70e39411d8469f4560ead755b33a7b0069c873ef0840ddba0c1e6b790e6bde740c272dc01',16)

pvtkey = construct((n,d))
pvtkey.d = d
pvtkey.e = e

#m = pvtkey.decrypt(c)
m = pow(c,d,n)
print('decrypted/original data ', m)

# Now lets do the opposite

c = pow(data, d, n)

print('encrypted with private exponent ', c)

m = pow(c, e, n)
print('decrypted/original data ', m)

"""
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAjOA4tB9uBDLjYs5JoJPK+/48bSjFCs9pqBzFtXQqnZR8cjiM6fyVLZ6pqXmv
MuEs0NlZOkBI4hrQIBcEExHt64Y46tjNFM99EdhkmHnDBB12b6rTsmNbXxLzGW0oSjSvHR1knpig
tIoWUHRnosdptZE9MFKS/mqsV58KalZS8RWGfkaBkQtHykZa35joKx3bH3HlouxFeEl22U+4dwtI
MKtqD5VXR5dteiSsa3qKxa1rY5/HFBaEuSRnyBtPkjzUEMMRtPXC/oZ0a6tL9VX7cIantIE4AkFt
cz4F1l/PQW5A8ltiO7r2yH+jlsp0bqTBgopHkgvrBzQR5ylDEKF94QIDAQABAoIBAQCBUVK8Bh33
vL7+9F6iCQlMSRUvHz3BrqROrhrPdtOn06ZpM4AnSrWmKv+TkyBAlHOPQ/Wkg15kMDjdPEOBPfQp
QAz/iAS6Fb25o+q0DRH3tRQDbczm9E3r+Hkv3gQeGj6le1XiQDlFgXz6XeDEjEl9YtXIhgRph4Ks
7FGjS5rXso4ZEcGEZ8KCNU3iKBzUM92d3JDgp9DiM4HSV2LVvUgOM3hZ2OAXdWnAlGA/oH7jfHV7
BzvnL2+hI4Jd0LMb2QUfFTl9AXhrs2bQMWc8Eg17hrWasUA0iWmO1Tb3DjlBHYRp9FYOrXVbM6ew
BpyHPvCEDdugwea3kOa950DCctwBAoGBAL9ZMQkDs22z46y11YjR43tKSnKeGItfUokTOufVE7Du
iOOEmsHfz62zCtF0BMgdke3kEr78mjro9sD6yMvoaRz92a3MolsfUROrkGZ5G52uN82EC+OjuzmM
AOiAERBCuBE0AqU90v3j/2cbsolt1/WOJBYWY59G3aif4qDdO4cLAoGBALx5X7Tq2kYHK1OlcsOV
447fQWUkLWNzXOc2c1z349sFsb+tfiZbbvYEHPvVr8Zz1ntbEj6id4+78ZXpStEXQZmx2KxFwpDN
l50x1x7Bble1scZwSwCZlMf0C0BqtgelA8etfgyAnVVzk9UcqqfyyzKdQdZSrkFuIFve6PRFJzJD
AoGANA1rTWx4Twt0j/MXF5UhMNTQ08U2IBPaO/fDOnW4WZVKH7pe7waXVEU0WC4bbuS8Yd59Sv8k
ZYoiNfUC0pVyorRblu/n6qnmQFeXfIjNfmN6Qqn9IfvUXp87UAQmoCnGMMfZQGJFF1QCkmXyd3gu
G1qDbo7Aov+AJPL5j5EfNGkCgYEApIekJ/BZCYbaqNOmotznYOK+WMfDI60irejXvpHcBGgtKjIP
DPcGn5cpoiKBptGaq+btv2Xez8f29rJIkM0nhD8/8euYFQaU0zIeJAgiBklj3uJKZ0SrH/6ID/zX
2UaRTS/D+LASKPWTWRgEVkbaYd3sCmf1HMNBVlH6tLrlo7cCgYBBXWjFTeCmf1XqlQOKiojsa6jq
T9ULM+jie/qO8GSaRm4g05iKcskTHlyNHEwqROucCFxA+iFbgEmdC/rYRzY7cnW5CsfXuJq4DARf
+DIEH/CRFr4YEi4TRWGKUQm4lNzgqQDQ4s1it9PnTW1aGOaHF1rM96UL3AMsrgOJEGnb1Q==
-----END RSA PRIVATE KEY-----
"""
