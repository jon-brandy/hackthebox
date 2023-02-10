# Restaurant
> Write-up author: vreshco
## DESCRIPTION:
Welcome to our Restaurant. Here, you can eat and drink as much as you want! Just don't overdo it..
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218115116-506eedf0-2fd5-4456-821b-2e840a5b4910.png)


2. Let's check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218115265-0417d28f-2401-4961-a53b-0b84149e075c.png)


3. Now we know, the **restaurant** is a 64 bit binary file and it's not stripped, let's check the binary's protections.

> VULN - NO CANARY FOUND, NO PIE.

![image](https://user-images.githubusercontent.com/70703371/218116059-7fc94767-9177-42f5-b2cd-66e4deba8b90.png)


4. Now let's decompile the binary using ghidra.
5. At the `fill()` function, looks like there's a bufferoverflow.

![image](https://user-images.githubusercontent.com/70703371/218119145-7fe380f3-fbfb-44a0-9c7f-876f5c90b093.png)


6. Let's get the offset of RIP first by get a segmentation fault with running the binary in gdb.
7. Enter 1024 bytes.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/218121772-d33483b6-d7ee-4d9e-90b6-9216d265edc1.png)


8. Since there's no value leaked at the RIP, we can use the RSP offset.

> RESULT - 40

![image](https://user-images.githubusercontent.com/70703371/218122089-5186b81e-be34-4433-8d53-9745341c834d.png)





