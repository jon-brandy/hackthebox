#mport string
#from secret import MSG
import os
os.system('clear')

f = open('./msg.enc', 'r')
'''
def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * char + 18) % 256)
    return bytes(ct)
'''

plaintext = ""

secret = f.read()
cipher = bytes.fromhex(secret)

for i in cipher: # for every char in cipher
    for brute in range(33, 126):
        if((123 * brute + 18) % 256) == i: # if it's a char
            plaintext += chr(brute)
            break
                
print(plaintext)
'''
ct = encryption(MSG)
f = open('./msg.enc','w')
f.write(ct.hex())
f.close()
'''
