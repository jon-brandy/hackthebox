# BabyEncryption
> Write-up author: jon-brandy
## DESCRIPTION:
You are after an organised crime group which is responsible for the illegal weapon market in your country. 
As a secret agent, you have infiltrated the group enough to be included in meetings with clients. 
During the last negotiation, you found one of the confidential messages for the customer. 
It contains crucial information about the delivery. Do you think you can decrypt it?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208054222-33318282-9be4-4ffa-a16b-e819e647f073.png)


2. Let's see what's inside the python script

> THE SCRIPT

```py
import string
from secret import MSG

def encryption(msg):
    ct = []
    for char in msg:
        ct.append((123 * char + 18) % 256)
    return bytes(ct)

ct = encryption(MSG)
f = open('./msg.enc','w')
f.write(ct.hex())
f.close()
```

3. Based from the script, we know that every character is multiplied by 123 and added by 18. Lastly modulus 256 to make sure that the character remains in the ASCII range.
4. Since there's a modulus and we know it that the flag is within the ASCII range, then we can bruteforce characters within a range of 33 to 126.

> ASCII TABLE

![image](https://user-images.githubusercontent.com/70703371/208057803-d6deed17-7706-416d-990b-56f025b12276.png)


5. Here is the modified script.

> Modified script

```py
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
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/208061213-a1749144-c608-4937-b77a-31c3f03de666.png)

6. Got the flag!

## FLAG

```
HTB{l00k_47_y0u_r3v3rs1ng_3qu4710n5_c0ngr475}
```


