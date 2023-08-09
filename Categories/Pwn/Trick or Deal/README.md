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


4. The pwn concept here is ret2win with UAF, but the problem is the PIE enabled. There are no way we can leaj 

