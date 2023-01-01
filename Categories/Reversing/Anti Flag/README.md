# Anti Flag
> Write-up author: jon-brandy
## DESCRIPTION:
Flag? What's a flag?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Now run the binary file we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210162405-611e1d11-17da-42f4-913a-48e3926c8c3e.png)


3. Let's decompile the binary in cutter.

> RESULT - MAIN

![image](https://user-images.githubusercontent.com/70703371/210162626-75716976-2f86-4e13-a189-52bbd096f17f.png)


4. It looks like the program comparing the values of `const char *s`.

![image](https://user-images.githubusercontent.com/70703371/210162650-66733faf-d6d3-49a1-9643-a42bdbda7585.png)


5. Let's patch this instruction pointer to `je`.

![image](https://user-images.githubusercontent.com/70703371/210162668-57594f04-1188-4816-af98-36fabe1d281a.png)



