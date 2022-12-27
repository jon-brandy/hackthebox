# You Cant C Me
> Write-up author: jon-brandy
## DESCRIPTION:
Can you see me?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209619917-ec81b5e1-dcd8-450a-903a-03f7ec442796.png)


2. Check the file type we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209619968-b1af84d3-e9f7-4a55-a112-6638e46b56e9.png)


3. It's a binary file and it's stripped. Means it's harder for us to debug the binary flow.
4. Let's decompile the binary and search for the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209620259-cbae9d30-3ebd-4fed-8f76-4dbcd7a1c863.png)


5. Notice here, if our input have the same strings as `Local_28` then the binary will print our output wrapped with HTB prefix.

> RESULT


6. Well i already tried to convert the hex into characters, but still got the wrong ans. which are weird.
7. Let's set the breakpoint at this offset using gdb

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209625646-f20c4f3e-8e20-4b39-a710-2809275aa390.png)


![image](https://user-images.githubusercontent.com/70703371/209625709-880d38f0-fc89-4b0e-b18a-45feddc23f4e.png)


![image](https://user-images.githubusercontent.com/70703371/209625748-394e3335-31f2-4452-9625-6dd36e1f1667.png)


8. Look at the RDI value.

![image](https://user-images.githubusercontent.com/70703371/209625797-686054be-30c0-47cb-998c-207334af96df.png)

9. Let's copy that and enter the strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209625891-dc089c0f-74a7-4ad0-bf85-5ea079c7309e.png)


10. Got the flag!

## FLAG

```
HTB{wh00ps!_y0u_d1d_c_m3}
```
