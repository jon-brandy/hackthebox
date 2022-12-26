# Baby RE
> Write-up author: jon-brandy
## DESCRIPTION:
Show us your basic skills! (P.S. There are 4 ways to solve this, are you willing to try them all?)
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209570996-118b083a-2463-48a3-a4e3-be98ac027f28.png)


2. Let's use `7z` then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571029-bc4440d0-960f-4235-801b-c7e4c5cfcd79.png)


![image](https://user-images.githubusercontent.com/70703371/209571044-4863c371-8913-46a1-88dd-924f2aa194a8.png)


3. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571070-a35363e4-50c9-4eca-b7d4-b9302963ddd4.png)


4. Since it's a binary file, let's make it executeable by run `chmod`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571219-f84bc7c0-8af2-4a59-9804-61cc3b3f9c75.png)


5. Let's input any strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571239-884b609b-764f-4e15-8f40-8d9122e099ba.png)


6. Now let's decompile the binary using ghidra, then check the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571330-78e15e52-7635-4c9b-9f55-e9ab5552c813.png)


![image](https://user-images.githubusercontent.com/70703371/209571365-ac0d8c94-c240-4070-a7c8-b3863361b123.png)


7. Notice we can see the correct input. Let's run the file again and input the strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571389-1367229e-d66a-40f0-bce4-c59c08e6aba9.png)


8. Got the flag!

## FLAG

```
HTB{B4BY_R3V_TH4TS_EZ}
```
