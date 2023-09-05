# Sick ROP
> Write-up author: jon-brandy
## DESRIPTION:
You might need some syscalls.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, statically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6e25e36a-812d-4462-b990-ca0508a23e15)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0381a559-7551-4ce3-b19e-360aed87559a)


2. Since the binary is statically linked and after decompiled the binary, it's very clear the pwn concept here is `Sigreturn ROP / SROP`.
3. There's no main function, but we can still identify the first function called with --> `_start`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/122a3c96-f8e1-487c-90dc-5ea46e405122)


4. So it's calling **vuln()** function (infinite loop).
5. Checking the **vuln()** function, we have read and write syscall.
6. Next, I checked the available gadgets we have, turns out we don't have `mov rax, 0xf` or `pop rax`.
7. Until now, it's still clear, the SROP concept we need to use is using the **mprotect**.
8. 
