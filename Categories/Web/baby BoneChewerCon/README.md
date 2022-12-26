# baby BonChewerCon
> Write-up author: jon-brandy
## DESCRIPTION:
Due to heavy workload for the upcoming baby BoneChewerCon event, the website is under maintenance and it errors out, but the debugger is still enabled in production!! 
I think the devil is enticing us to go and check out the secret key.
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209569323-b5b56bc2-33b3-4b66-81e1-76c6273429ac.png)


2. Let's enter `HALLO` then register it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209569464-3a586034-89d3-4bfb-bcb6-d5102c92197f.png)


3. Turns out we can see the **http kernel**.
4. When i clicked this one:

![image](https://user-images.githubusercontent.com/70703371/209569516-1f79cafa-2123-462b-96a2-71260ef657a2.png)


5. Then scroll to the server/request data.

![image](https://user-images.githubusercontent.com/70703371/209569553-531b4990-f9ce-46b5-ac3a-af74afc69424.png)


![image](https://user-images.githubusercontent.com/70703371/209569575-b01d2f20-3352-445e-b9d6-5a35af54b1fd.png)


6. Got the flag

## FLAG

```
HTB{wh3n_th3_d3bugg3r_turns_4g41nst_th3_d3bugg33}
```
