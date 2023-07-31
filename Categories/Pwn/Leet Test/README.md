# Leet Test
> Write-up author: jon-brandy
## DESCRIPTION:
Are you 1337 enough?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ file leet_test 
leet_test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c6e69bc8fc90c94520adb2fc11a0d7d7b85326f6, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ pwn checksec leet_test                              
[*] '/home/brandy/Downloads/leet_test/leet_test'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

