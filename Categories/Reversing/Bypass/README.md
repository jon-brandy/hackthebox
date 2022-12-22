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


12. Run the program.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209154204-2f0b4a48-8298-4b09-a5d5-bda0ba9ee7d0.png)


13. Hmm.. When i checked the `1()` function.

![image](https://user-images.githubusercontent.com/70703371/209156879-8bc2c5d9-3686-4185-b489-3c70ce5d42f0.png)


14. The bool always return false.
15. Anyway let's change bool value of flag2 to true then click the `continue` button.

![image](https://user-images.githubusercontent.com/70703371/209162824-966da772-0082-48a9-bb6b-1505480d6a05.png)

![image](https://user-images.githubusercontent.com/70703371/209162848-502d4474-8720-475d-8126-acb89d9fa593.png)


> RESULT ON THE CMD

![image](https://user-images.githubusercontent.com/70703371/209159071-39c58b94-20f6-4da1-a212-08eaa78d3dec.png)


16. Now enter any strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209159192-070c0eb8-3d31-4209-90d3-88a9577053a2.png)


17. Notice we got this value for the secret key.

![image](https://user-images.githubusercontent.com/70703371/209159249-0c7f47d0-43a1-47ad-bb10-284353c8c391.png)


18. Copy that.

> SECRET KEY

```
ThisIsAReallyReallySecureKeyButYouCanReadItFromSourceSoItSucks
```

19. Now run the program again at **dnspy** and use the same step.
20. When prompted the secret key, paste the strings we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209163165-ba24f8ff-0440-4f48-abec-4e5ea6d26566.png)


21. Nice, but don't click the continue button, press f10 at **dnspy** to step over execution.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209163431-f4cf3cc7-ea97-4428-ab0d-914da7b17fa6.png)


22. Got the flag!


## FLAG

```
HTB{SuP3rC00lFL4g}
```



