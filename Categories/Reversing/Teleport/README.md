# Teleport
> Write-up author: jon-brandy
## DESCRIPTION:
You've been sent to a strange planet, inhabited by a species with the natural ability to teleport. 
If you're able to capture one, you may be able to synthesise lightweight teleportation technology. 
However, they don't want to be caught, and disappear out of your grasp - can you get the drop on them?
## HINT:
- NONE
## STEPS
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214474090-4b909fdc-99f3-466a-9863-dc2bf75d6362.png)


![image](https://user-images.githubusercontent.com/70703371/214474116-830570e8-2d0c-4f2e-827f-f40f7c326e1b.png)


![image](https://user-images.githubusercontent.com/70703371/214474147-fb76e23d-5e77-4aae-9544-3b826275d0bb.png)


2. Since it's a binary file, let's decompile the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214475267-0f5a9f16-0078-43be-a905-1c40ba460b70.png)


![image](https://user-images.githubusercontent.com/70703371/214475412-35ce0dce-4378-40ac-bd2c-5eb52ea2fd9b.png)


![image](https://user-images.githubusercontent.com/70703371/214475434-7eabd128-1992-431d-be3a-c989a71f15cf.png)


3. Looks like the functions contains the flag's character. But it's position is randomized.
4. Actually we can ordered the characters with the number they have, example:

![image](https://user-images.githubusercontent.com/70703371/214475636-b07d0ae7-d063-40bc-a4e0-affe87b4c238.png)


5. The `H` -> 1, means it stands for the first character.
6. Doing the same approach at the end we got the flag!

## FLAG

```
HTB{jump1ng_thru_th3_sp4c3_t1m3_c0nt1nuum!}
```
