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


> Turns out it's a bash command, which encode the input to base64.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4b56bbd-ba23-4865-bf9a-a6320d07dced)


3. Might be the clue here, interesting. Also great helper, we have system().

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8352888-9bc3-4083-be29-144c2d356355)


