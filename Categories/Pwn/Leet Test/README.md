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


7. The program opens `/dev/urandom`, then read 4 bytes from that file into `local_13c`. Next the program do `AND` operation on those random bytes that we got with `0xffff`.


![image](https://user-images.githubusercontent.com/70703371/211010008-1ffc912d-9ca6-4074-b12a-868e0a9bd9cd.png)



> NOTES

```
/dev/random and /dev/urandom are special files that serve as cryptographically secure pseudorandom number generators in linux. They allow access to environmental noise collected from device drivers and other sources.

EXAMPLE OF "AND" OPERATION BASED ON THE CODE:

Assume the random bytes is 77 77 77 77, then:

77 77 77 77
00 00 ff ff
-------------- AND
00 00 77 77

Hence, we only have 2 random bytes left.
```

8. So at the end of the while loop, we have 2 random bytes.
9. The "while loop" will always be active, we need to hit the `break` statements to stop it.

![image](https://user-images.githubusercontent.com/70703371/211010771-888a07b1-0506-44d7-b000-a815497f7ac9.png)


10. Based from the "while loop", we want to pass the if condition so we can get the `flag.txt` file, the problem here is we can do bufferoverflow because the input we can do is only the "name". Not only that the `local_128` variable (name) is not used in the if condition.
11. But we can pass that by utilize the format string vulnerability.
12. Since our input is stored in the stack, by utilize this vuln, we can see our own input stored in hex values from stack.

> EXAMPLE

![image](https://user-images.githubusercontent.com/70703371/211011990-3db0fb2e-997b-4938-b6ba-7e59d54ddb79.png)


13. Notice there's `0x4141..` (A) in hex at the 10th element.


![image](https://user-images.githubusercontent.com/70703371/211012209-55a92e81-abb0-4f73-a178-43a8b369026b.png)


14. Based from this concept, we can utilize it to overwrite the `winner` interger stored in stack, hence we can pass the condition and get the flag.
15. To test out our concept, i made this python script:

```py
from pwn import *
import os

os.system('clear')

def start(argv=[], *a, **kw):
    if args.REMOTE: 
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else: 
        return process([exe] + argv, *a, **kw)


exe = './leet_test'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

sh = start()

winOffset = 0x404078 # win offset
p = flat([
    winOffset,
    b'%10$p' # Overwrite the 10th element
])

sh.sendlineafter(':', p)
sh.interactive()

```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211013764-621edb34-e17f-46eb-a67f-818b1cce7362.png)




16. Great! We proved it right.
17. 
