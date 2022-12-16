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

> GHIDRA

