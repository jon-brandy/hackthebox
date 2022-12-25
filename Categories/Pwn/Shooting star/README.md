# Shooting star
> Write-up author: jon-brandy
## DESCRIPTION:
Tired of exploring the never-ending world, you lie down and enjoy the crystal clear sky. 
Over a million stars above your head! Enjoy the silence and the glorious stars while you rest.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next, check the type of file we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470016-ecc03170-c28c-4e53-bf5f-7954c723f673.png)


3. It's a 64 bit binary file, dynamically linked, and **not stripped**, hence it's easier for us to debug and identify the functions.
4. Now check the binary's protection.

> RESULT - No canary found - No PIE - Partial RELRO

![image](https://user-images.githubusercontent.com/70703371/209470051-2c078c05-cfe6-47b0-ba3d-ff0626419729.png)


5. Let's make the file executeable by run chmod, then run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470142-0ec0daea-11cf-4ab3-9875-905c305b56a9.png)


6. Let's choose option 1.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470148-90c8c2cc-9c1f-4608-89b3-8940c00a8808.png)


7. Let's paste 1024 cyclic pattern.

> RESULT - GOT SEGMENTATION FAULT

![image](https://user-images.githubusercontent.com/70703371/209470163-8f6a6d8c-6a27-4a81-8395-db5e1b42b01f.png)


8. Find the correct bytes to overflow the buffer.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470185-9bda701e-ed75-446c-905c-e5eead82c801.png)


9. It's 64 bytes.
10. Now let's check all the functions available.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470211-70694e0a-25d6-40d8-9610-46ec70b36c73.png)


11. A function caught my attention -> `setup()` func.
12. Let's decompile the binary using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470231-01786e09-00cc-4eeb-b8c6-0e1268e8a54b.png)


13. Check the `star()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209470246-7146969e-960a-4835-9265-4b72c221ae7b.png)


14. Notice the program reads more buffer from `local_48`.

![image](https://user-images.githubusercontent.com/70703371/209470294-3e462513-66b2-4fe4-a821-920ac6ae8d66.png)


15. We found the vuln there.
16. 
