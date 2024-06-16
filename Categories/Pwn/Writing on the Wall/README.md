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

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f7df9ca-e75c-44bc-9f79-d2d1de4fb592)


2. Upon reviewing the decompiled code in ghidra, we can clearly spot the vuln at the read() usage. It introduced a OOB vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb41ecaf-6ff5-44d2-95a3-a917fc690d96)


3. It's quite straightforward then.
4. Reviewing the stack, seems the position of **password** is adjacent below **buffer**. Hence, hitting RBP shall overwrite **password**.
5. Remember about read() vuln, it reads data until it meet a NULL byte.
6. So then, utilizing the OOB could overwrite the **password** value entirely.
