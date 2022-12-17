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

![image](https://user-images.githubusercontent.com/70703371/208225388-d469c922-0647-43d9-b821-9ac1fba01212.png)


9. Now check the functiosn
