# Brainy's Cipher
> Write-up author: jon-brandy
## DESCRIPTION:
Brainy likes playing around with esoteric programming. 
He also likes math and has therefore encrypted his very secure password with a popular encryption algorithm. 
Claiming that his password cannot be retrieved now, he has sent the ciphertext to some of his friends. 
Can you prove to Brainy that his password can actually be recovered?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT - GOT A .TXT FILE

![image](https://user-images.githubusercontent.com/70703371/212460522-e825d181-9415-47cc-b90e-5a2e5a1e59be.png)


2. Well it's a brainfuck ciphertext. Let's decode it using [this](https://www.dcode.fr/brainfuck-language) website.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212460631-50d664d9-68f7-4841-b391-c84d8b9fe85b.png)


3. Since there's `pq` and `dq` it's a `weird-rsa`.
4. To decrypt this RSA, i used this script:

```py
import os
#from pwn import *
import binascii

os.system('clear')

#context.log_level = 'debug'

## STEPS:
'''
1. Get the qInv value.
2. Calculate the message.
3. Convert the message we got from (int) to str.
4. Print out the message.
'''

p = 7901324502264899236349230781143813838831920474669364339844939631481665770635584819958931021644265960578585153616742963330195946431321644921572803658406281
q =12802918451444044622583757703752066118180068668479378778928741088302355425977192996799623998720429594346778865275391307730988819243843851683079000293815051
dp = 5540655028622021934429306287937775291955623308965208384582009857376053583575510784169616065113641391169613969813652523507421157045377898542386933198269451
dq = 9066897320308834206952359399737747311983309062764178906269475847173966073567988170415839954996322314157438770225952491560052871464136163421892050057498651
c = 62078086677416686867183857957350338314446280912673392448065026850212685326551183962056495964579782325302082054393933682265772802750887293602432512967994805549965020916953644635965916607925335639027579187435180607475963322465417758959002385451863122106487834784688029167720175128082066670945625067803812970871

qInv = (1/q) % p
calcMessage = pow(c, dq, q)
plaintext = binascii.unhexlify(format(calcMessage,'x')).decode()
print(plaintext)

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/212460976-815d0ebf-ad2f-4330-8681-38c6153b46a3.png)


5. Wrap the output with `HTB{}`.
6. Got the flag!

## FLAG

```
HTB{ch1n3z_r3m4ind3r_the0rem_r0ck$$$_9792}
```

