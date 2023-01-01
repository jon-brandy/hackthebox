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
