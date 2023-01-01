# Android-in-the-Middle
> Write-up author: jon-brandy
## DESCRIPTION:
Years have passed since Miyuki rescued you from the graveyard. 
When Virgil tells you that he needs your help with something he found there, 
desperate thoughts about your father and the disabilities you developed due to the disposal process come to mind. 
The device looks like an advanced GPS with AI capabilities. 
Riddled with questions about the past, you are pessimistic that you could be of any value. 
After hours of fiddling and observing the power traces of this strange device, 
you and Virgil manage to connect to the debugging interface and write an interpreter to control the signals. 
The protocol looks familiar to you. Your father always talked about implementing this scheme in devices for security reasons. Could it have been him?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/210165812-83747862-195a-4536-ac48-ff4e4c5f52be.png)


> THE SCRIPT

```
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib
import random
import socketserver
import signal


FLAG = "HTB{--REDACTED--}"
DEBUG_MSG = "DEBUG MSG - "
p = 0x509efab16c5e2772fa00fc180766b6e62c09bdbd65637793c70b6094f6a7bb8189172685d2bddf87564fe2a6bc596ce28867fd7bbc300fd241b8e3348df6a0b076a0b438824517e0a87c38946fa69511f4201505fca11bc08f257e7a4bb009b4f16b34b3c15ec63c55a9dac306f4daa6f4e8b31ae700eba47766d0d907e2b9633a957f19398151111a879563cbe719ddb4a4078dd4ba42ebbf15203d75a4ed3dcd126cb86937222d2ee8bddc973df44435f3f9335f062b7b68c3da300e88bf1013847af1203402a3147b6f7ddab422d29d56fc7dcb8ad7297b04ccc52f7bc5fdd90bf9e36d01902e0e16aa4c387294c1605c6859b40dad12ae28fdfd3250a2e9
g = 2


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(0)
        main(self.request)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def sendMessage(s, msg):
    s.send(msg.encode())


def recieveMessage(s, msg):
    sendMessage(s, msg)
    return s.recv(4096).decode().strip()


def decrypt(encrypted, shared_secret):
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.decrypt(encrypted)
    return message


def main(s):
    sendMessage(s, DEBUG_MSG + "Generating The Global DH Parameters\n")
    sendMessage(s, DEBUG_MSG + f"g = {g}, p = {p}\n")
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n\n")

    sendMessage(s, DEBUG_MSG + "Generating The Public Key of CPU...\n")
    c = random.randrange(2, p - 1)
    C = pow(g, c, p)
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n")
    sendMessage(s, DEBUG_MSG + "Public Key is: ???\n\n")

    M = recieveMessage(s, "Enter The Public Key of The Memory: ")

    try:
        M = int(M)
    except:
        sendMessage(s, DEBUG_MSG + "Unexpected Error Occured\n")
        exit()

    sendMessage(s, "\n" + DEBUG_MSG + "The CPU Calculates The Shared Secret\n")
    shared_secret = pow(M, c, p)
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n\n")

    encrypted_sequence = recieveMessage(
        s, "Enter The Encrypted Initialization Sequence: ")

    try:
        encrypted_sequence = bytes.fromhex(encrypted_sequence)
        assert len(encrypted_sequence) % 16 == 0
    except:
        sendMessage(s, DEBUG_MSG + "Unexpected Error Occured\n")
        exit()

    sequence = decrypt(encrypted_sequence, shared_secret)

    if sequence == b"Initialization Sequence - Code 0":
        sendMessage(s, "\n" + DEBUG_MSG +
                    "Reseting The Protocol With The New Shared Key\n")
        sendMessage(s, DEBUG_MSG + f"{FLAG}")
    else:
        exit()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), Handler)
    server.serve_forever()

```

2. Since i'm new to cryptography, so i did a small outsource about the script. Found out that the script is making use fo the **Diffie-Hellman Key Exchange**.
3. This argument supported by the availability of variables p and g.
4. Well to find the secret message (flag) we can assume that out public key is 1. 1 to any power is 1, so we can utilize this concept to bootstrap out AES encryption shown in the challenge.
5. So here is the modified script:

```py
from pwn import *
import os
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
import hashlib

os.system('clear')
context.log_level = 'debug'

sh = remote('167.172.55.94',32595)

p = 0x509efab16c5e2772fa00fc180766b6e62c09bdbd65637793c70b6094f6a7bb8189172685d2bddf87564fe2a6bc596ce28867fd7bbc300fd241b8e3348df6a0b076a0b438824517e0a87c38946fa69511f4201505fca11bc08f257e7a4bb009b4f16b34b3c15ec63c55a9dac306f4daa6f4e8b31ae700eba47766d0d907e2b9633a957f19398151111a879563cbe719ddb4a4078dd4ba42ebbf15203d75a4ed3dcd126cb86937222d2ee8bddc973df44435f3f9335f062b7b68c3da300e88bf1013847af1203402a3147b6f7ddab422d29d56fc7dcb8ad7297b04ccc52f7bc5fdd90bf9e36d01902e0e16aa4c387294c1605c6859b40dad12ae28fdfd3250a2e9
g = 2

mes = b'Initialization Sequence - Code 0'

def enc(mes, pubkey):
    key = hashlib.md5(long_to_bytes(pubkey)).digest()
    cipherText = AES.new(key, AES.MODE_ECB)
    result = cipherText.encrypt(mes)
    return result

sh.recvuntil(b':')
sh.sendline(b'1')
sh.recvuntil(':')
sh.sendline(enc(mes,1).hex())

getFlag = sh.recvall()
success(getFlag)

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210166171-00e3014d-944e-47c4-85e4-8286c90b19c0.png)


6. Got the flag!

## FLAG

```
HTB{7h15_15_cr3@t3d_by_Danb3er_@nd_h@s_c0pyr1gh7_1aws!_!}
```

