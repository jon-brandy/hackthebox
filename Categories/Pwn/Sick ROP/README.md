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


2. Since the binary is statically linked and after decompiled the binary, the pwn concept should be `ret2syscall` or `Sigreturn ROP`.
3. There's no main function, but we can still identify the first function called with --> `_start`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/122a3c96-f8e1-487c-90dc-5ea46e405122)


4. So it's calling **vuln()** function (infinite loop).
5. Checking the **vuln()** function, we have read and write syscall.
6. Next, I checked the available gadgets we have, turns out we don't have `mov rax, 0xf` or `pop rax`, and even no `pop rdi`.
7. Now, it's very clear that the pwn concept is SROP. The SROP method we need to use is using the **sys_mprotect()**.
8. Why **sys_mprotect()**?? Because it makes a memory segment with a fixed address for write & execute.

## FLOW

> The strat (in short)

```
1. Set the register value to call sys_mprotect().
2. Trigger the sys_rt_sigreturn. (at this point we should have a stack which is executeable).
3. Since we have an executeable stack, now inject our shellcode.
4. Control the RIP to the shellcode so we got RCE.
```


