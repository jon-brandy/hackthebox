# Rebuilding
> Write-up author: jon-brandy
## DESCRIPTION:
You arrive on a barren planet, searching for the hideout of a scientist involved in the Longhir resistance movement. 
You touch down at the mouth of a vast cavern, your sensors picking up strange noises far below. 
All around you, ancient machinery whirrs and spins as strange sigils appear and change on the walls. 
You can tell that this machine has been running since long before you arrived, and will continue long after you're gone. Can you hope to understand its workings?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/214468857-70a7ec42-2108-4192-ba02-63ee77a56f28.png)


![image](https://user-images.githubusercontent.com/70703371/214469939-7d7e11b9-2b82-44bd-8b55-872937df0cc0.png)


![image](https://user-images.githubusercontent.com/70703371/214469306-8a4701fd-ef5b-4169-b595-e58d5ed51d63.png)


3. Since it's a binary file let's decompile it.
4. When analyzing the `main()` function, this operations caught my attention.

![image](https://user-images.githubusercontent.com/70703371/214470632-3acceebf-3933-4d6c-87d8-ef41680f28b3.png)


5. Let's check the encrypted values.

![image](https://user-images.githubusercontent.com/70703371/214470690-2a45cb93-e073-41fc-a6ba-d07e2574876c.png)


6. Looks like a hexadecimal values. Notice the hex is XORed with a key named -> `humans`.


![image](https://user-images.githubusercontent.com/70703371/214470861-9e5282f2-b043-4233-a861-e22dbea6e1ce.png)


7. But i found another key at the `_INIT_1()` function named `aliens`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214470968-f51d8579-8eb1-402f-97ce-0d23d305f0f0.png)


8. I'm guessing `aliens` is the correct key. Let's copy the hex values and XORed it with `aliens` at cyberchef

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214471352-c4d36d5d-14df-47a6-8ece-1060c85f606e.png)


9. Got the flag!

## FLAG

```
HTB{h1d1ng_c0d3s_1n_c0nstruct0r5}
```
