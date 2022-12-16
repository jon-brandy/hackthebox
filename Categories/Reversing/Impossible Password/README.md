# Impossible Password
> Write-up author: jon-brandy
## DESCRIPTION:
Are you able to cheat me and get the flag?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208129090-784d9df3-a66f-404c-bb37-3276d2fc4474.png)


2. Now, check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208129195-3604916d-566c-4438-a97b-a3debcb68a18.png)


3. Now we know it's a binary file and stripped, means we can't see the function's name. Since it's a binary file, let's make it executeable by run chmod, then run the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208129406-d09f7b90-0781-4e39-8b73-e2c78feb6ecf.png)


4. Hmm.. let's decompile the file using ghidra.
5. Find a clue here.

![image](https://user-images.githubusercontent.com/70703371/208130523-59086866-395b-4b45-948e-773b1a8dee01.png)


6. The program will compare our input with the `local_10` value.
7. Then the program will prompt us an input again, and it will compare our input with `__s2` value.

![image](https://user-images.githubusercontent.com/70703371/208130909-4d17f40b-6018-4c31-aa6b-7add255f0fbc.png)


8. Let's analyze this function.

![image](https://user-images.githubusercontent.com/70703371/208131063-56205631-7b75-4128-b1ae-1ac97370cee6.png)


![image](https://user-images.githubusercontent.com/70703371/208131171-bc4830da-22e0-470c-af4c-f0eab1a7bb69.png)


9. However, better than wasting time analyze the stripped code, in reverse engineering we may **patch the binary instruction**.
10. 
