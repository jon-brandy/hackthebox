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

![image](https://user-images.githubusercontent.com/70703371/209470626-1b8b301c-f33b-461e-9100-286baf84ad10.png)


9. It's 72 bytes.
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
16. I think the concept here is **ret2libc**, because there's not `system()` function, but only `reads()` and `write()`, both are come from the libc library.
17. Now we need to leak the `.got` address.
18. First, let's get the `pop_rdi` value from the binary using ropper.

```
ropper --file shooting_star --search "pop rdi"
```

> RESULT - 0x4012cb

![image](https://user-images.githubusercontent.com/70703371/209471808-e24d8024-2b4f-4d13-b242-36ba92a3b9bc.png)


19. Next, get the `pop_rsi` value.

```
ropper --file shooting_star --search "pop rsi"
```

> RESULT - 0x4012c9

![image](https://user-images.githubusercontent.com/70703371/209471877-bd6dc023-ec2d-4e90-ae9b-ac03deb64a3f.png)


20. 

