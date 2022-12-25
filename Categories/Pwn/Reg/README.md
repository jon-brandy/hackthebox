# Reg
> Write-up author: jon-brandy
## DESCRIPTION:
This is a basic buffer flow exploit. Try to get the flag.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next, check the file type we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469022-868db7be-e8d4-4678-a528-9f0bd0b2a919.png)


3. It's a 64 bit binary file, dynamically linked and **not stripped**. Since it's not stripped, hence it's easier for us debug or identify the function.
4. Now, check the binary's protection.

> RESULT 

```
No canary Found (means we can do bufferoverflow concept).
No PIE (means a binary and all of it's dependencies are loaded not in random locations within virtual memory each time the application executed).
Partial RELRO (some sections of the binary are read only, preventing them from being modified).
```

![image](https://user-images.githubusercontent.com/70703371/209469053-3655c77c-d080-476a-97e9-3b6bbe2ff4b4.png)


5. Now run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469202-3e2f98a8-6865-4bcf-95b2-6b3bfc7e5907.png)


6. Let's enter 1024 cyclic pattern.

> RESULT - GOT SEGMENTATION FAULT

![image](https://user-images.githubusercontent.com/70703371/209469249-07d78d45-4722-47cf-a3bc-ba148c4871d3.png)


7. To find the correct bytes to overflow the buffer, copy all the RBP characters.

![image](https://user-images.githubusercontent.com/70703371/209469266-359f4ef1-28d3-46fb-87d8-20e696c0e3a3.png)


8. Then run this command -> `cyclic -l gaaaaaaa`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469282-1faa70d6-4614-499f-aa8f-b27c342306c7.png)


9. 48 Bytes.
10. Let's decompile the file with ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469351-4d3d9e29-06ec-4204-9fdd-75d9879d3b34.png)


11. Check the `run()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469384-032f4017-bd9d-4755-bff2-4e60b5265c84.png)


12. Based from the decompiled binary we got, the vuln is at the `gets()` function.
13. Notice there's a function named `winner()`.

![image](https://user-images.githubusercontent.com/70703371/209469428-a99621bc-4522-4f3c-9b18-65a419ea11c4.png)


14. The concept here is ret2win, we can control the return address to the `winner()` function by overflow the buffer.
15. Now get the `winner()` address.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209469477-2d32a529-e4c5-4779-89d1-5c81ea270f00.png)


16. Convert that to decimal.
17. Here's our script so far.

> THE SCRIPT

```py

```
