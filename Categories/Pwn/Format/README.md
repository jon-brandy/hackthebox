# Format
## DESCRIPTION:
Can you hear the echo?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/format_htb]
└─$ file format
format: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5d38e04d29b4aae722164869f3151cea776ce91c, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/format_htb]
└─$ pwn checksec format                                     
[*] '/home/brandy/Downloads/format_htb/format'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

2. After decompiled the binary, it seems we can leak - calculate the piebase and libc base using the format strings vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e3f2da2-36ef-481e-b471-b432a1dafa77)


3. But there is no BOF, hence we can't do ret2libc here. Also we can't overwrite the Global Offset Table, because RELRO is full.
4. So how to get the shell? We still can utilize `__malloc_hook`.

#### MALLOC HOOK

- **__malloc_hook** is a hook function which is called whenever malloc is called.
- We can use one_gadget and we can trigger them by sending big buffer.
- printf() will use malloc to allocate memory after we sent big buffer.


5. Let's grab the piebase and potential libc.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd8097b8-44e8-4e63-8058-8765319f4a73)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f41313c3-13fb-4455-8ceb-aa392f095f1f)

