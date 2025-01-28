# No Gadgets
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/a14e6d6a-7b1f-4913-84a2-e243c47c8bfc)

## Lessons Learned:
1. Bypass **strelen()** check.
2. Perform partial GOT overwrite using controlled **RBP**.
3. Passing **/bin/sh** strings to drop shell.

## DESCRIPTION:
<p align="justify">In a world of mass shortages, even gadgets have gone missing. The remaining ones are protected by the gloating MEGAMIND, a once-sentient AI trapped in what remains of the NSA's nuclear bunker. Retrieving these gadgets is a top priority, but by no means easy. Much rests on what you can get done here, hacker. One could say too much.</p>

## STEPS:
1. In this challenge, we're given a full setup for the pwn challenge.

![image](https://github.com/user-attachments/assets/9e332a80-dbe8-47a1-b08c-9eb5dc26b4ca)

2. The binary itself is 64 bit, dynamically linked, and not stripped.

![image](https://github.com/user-attachments/assets/5110b458-6cf1-4c40-b017-50c269bc2957)

> BINARY PROTECTIONS

![image](https://github.com/user-attachments/assets/3eccc84b-f954-4f3a-86a3-7ee37243602c)

3. Since we're given the source code, hence we won't need to decompile the binary **to analyze the source**.
4. Upon reviewing it, the bug is very straightforward. Big buffer overflow at the user input, however a buffer check is mitigating our further exploitation.

![image](https://github.com/user-attachments/assets/c1e74311-9cbc-460e-a420-f22b09b17ff6)

5. If the buffer length is bigger than the allocated buffer, hence the binary shall terminated.


