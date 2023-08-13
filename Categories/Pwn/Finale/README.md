# Finale
## DESCRIPTION:
It's the end of the season and we all know that the Spooktober Spirit will grant a souvenir to everyone and make their wish come true! Wish you the best for the upcoming year!
## HINT:
- NONE
## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_final/challenge]
└─$ file finale 
finale: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ac92ca00b198dcf7287937f5ce21c1123a5a549e, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_final/challenge]
└─$ pwn checksec finale                         
[*] '/home/brandy/Downloads/pwn_final/challenge/finale'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

2. After decompiled the binary, found a potential BOF at the finale() function (line 12).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc62844b-6743-4fad-a980-e7f31e7c2e28)


3. But notice there's a leaked stack address and based from the README.txt file, the problem setter told us not to do ret2libc because the remote server has a custom libc.
4. What comes to my mind we can do "seccomp-way", instead of spawn a shell, we grab the flag from the remote server.
5. Since it's not ret2shell challenge, hence don't need to worry about the flag.txt location.

### FLOW

```
Remembering there is leaked stack addres, hence we can use it to store the content of flag.txt.
Analyzing the source code, we can use open@plt, read@plt, and write@plt.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e7e9bc7c-0cd1-462a-bbbf-fa969c2acc1c)


> Things to know

```

```
