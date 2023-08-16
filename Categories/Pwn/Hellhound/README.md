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

```console
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


4. Although there's no potential overflow, we still can do ret2win here. The heap exploit we're gonna do is called **House of Spirit**.

### FLOW

```
We're gonna do a fake chunk then overwrites a pointer to point to it.
```

First we need to grab the leaked stack address at option 1, then we add it with our padding. 

> Padding is calculated from

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1c3c714c-515a-446a-b17d-0b8457fd14eb)


```
choice (8 bytes) + canary (8 bytes) + input (64 bytes).
```

Why do we need canary?? No need to explain this in detail I guess, already learned heap, I'm guessing you already familiar with canary.
So our return address is consist of --> leaked stack address + padding.
