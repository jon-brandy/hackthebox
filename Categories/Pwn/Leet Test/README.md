![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6042dc21-4df4-457f-99bc-7e062796326a)# Leet Test
> Write-up author: jon-brandy
## DESCRIPTION:
Are you 1337 enough?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ file leet_test 
leet_test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c6e69bc8fc90c94520adb2fc11a0d7d7b85326f6, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ pwn checksec leet_test                              
[*] '/home/brandy/Downloads/leet_test/leet_test'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```


2. After decompiled the binary, seems the concept here is overwriting stack variable using format strings vulnerability.
3. It's proven by no potential BOF but there is format strings vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6656022e-a408-4e6e-af3b-f7873e468318)


4. Analyzing the main functions, we know that we can overwrite 2 variables there, the `local_13c` which held the random values.
5. And `winner` variable which held the 0xcafebabe value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd203988-b454-4106-b115-ae41377c0d5c)


6. We can just overwrite them as 0, so it would be look like this:

```
0 * 0x1337c0de == 0
```

7. With this, when we run the binary, it will break out of the while loop then cat the flag for us.
8. Great! Here's what we need to do:

```
- Get the fmtstr offset.
- Calculate the exact address for the variable that held the random value.
- grab the address for winner.
```


9. 



