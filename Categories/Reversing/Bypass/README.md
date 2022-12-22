# Bypass
> Write-up author: jon-brandy
## DESCRIPTION:
The Client is in full control. Bypass the authentication and read the key to get the Flag.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208224177-c9cf72c6-296f-489c-abe4-4192527d99ed.png)


2. Got an `exe` file.
3. Let's run it on windows.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208224228-53c2ba05-acfb-4af9-97eb-2e8c3fa468ca.png)


4. Let's decompile it with ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208224452-d5f2d63a-abf0-4e32-9b77-2450a7b0d4b7.png)


5. Surprisingly we got no clue.
6. Then i tried to strings the file to see if there are any hints.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208224494-3115f639-5c79-4742-adf9-aa34b135fe18.png)


7. Now we know that the codebase was written in .NET.
8. To decompile .NET binaries we need to use dnSpy.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209152786-d178c14d-f037-478b-ac64-1dcf40f6b935.png)


9. Now check this function.

![image](https://user-images.githubusercontent.com/70703371/209146033-7899f12c-5760-4a2f-9162-1338e1997db9.png)


![image](https://user-images.githubusercontent.com/70703371/209146076-31a10430-0dbb-4092-9be1-3514120af42f.png)


10. Based from it we know that the boolean values of flag and flag2 is the same.

![image](https://user-images.githubusercontent.com/70703371/209150407-feb1744f-65dd-4d86-b317-efd391ed1d50.png)


11. Now set breakpoints at flag2 and flag.

![image](https://user-images.githubusercontent.com/70703371/209153013-03b0df56-b33f-44dd-8e2e-1032329284e2.png)


![image](https://user-images.githubusercontent.com/70703371/209153302-878a9699-1c1a-423a-a8cd-d9082c7b1d56.png)


12. 



