# racecar

> Write-up author: jon-brandy

## DESCRIPTION:
Did you know that racecar spelled backwards is racecar? Well, now that you know everything about racing, win this race and get the flag!

## HINT:
- NONE

## STEPS:
1. First, unzip the file given and enter `hackthebox` as the password.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557130-3fe9ba23-8bcb-4e88-aa13-5268f073a7c5.png)


2. Next, check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557218-d4234e3c-3953-4400-bbcc-41b7e95cbfd9.png)


3. It's an ELF 32 bit file, dynamically linked and luckily not stripped.
4. Now check the file's protector.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557439-109f1672-662f-4626-99f8-f1332be2609f.png)


5. Hmm.. Looks like there's no vuln we can utilize here.
6. Anyway, let's run the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207557828-d7de0ace-f121-41d7-87c4-4cf18ad7482d.png)


![image](https://user-images.githubusercontent.com/70703371/207557903-9ccaf724-8926-497e-8e6c-f0c44893a15f.png)


![image](https://user-images.githubusercontent.com/70703371/207557945-a8cc3667-034d-47d1-a182-f6ee9c8e4b70.png)


![image](https://user-images.githubusercontent.com/70703371/207557993-c0842a28-250f-4334-8404-0a60ed55e99d.png)



![image](https://user-images.githubusercontent.com/70703371/207558779-ab2e8e92-5f67-4ce2-9c3e-3ff392f6c954.png)



![image](https://user-images.githubusercontent.com/70703371/207558766-204d621a-4ad0-432d-a2f5-5ee2961621b6.png)


7. Let's run the remote server.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207558976-9a6ad069-a3a0-4934-82c9-3b4872ec777e.png)


8. Follow the same steps as before.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207559114-b0da1ce8-c96f-48ac-853a-4efcc5066a68.png)


9. Let's decompile the file using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207559895-986815be-edeb-4683-9478-e3d36c911d04.png)


10. 


