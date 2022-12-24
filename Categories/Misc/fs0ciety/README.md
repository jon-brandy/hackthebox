# fs0ciety
> Write-up author: jon-brandy
## DESCRIPTION:
We believe that there is an SSH Password inside password protected 'ZIP' folder. 
Can you crack the 'ZIP' folder and get the SSH password?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209438954-516a1c8a-5fc1-42a0-953f-831724a4b31a.png)


2. Unzip the `.zip` file we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209438977-d7a4d85a-ac56-4161-8733-ab1ebed75bc8.png)


3. Since we didn't know the password, let's use **fcrackzip**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209439141-3ee39975-8b91-4442-98a4-159f2ab10bc7.png)


4. Got the pass, let's unzip it with the pass we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209439164-71456fd0-eb73-4291-8342-0e26ee4dd135.png)


5. Strings the `.txt` file.

![image](https://user-images.githubusercontent.com/70703371/209439192-2b776c77-d073-44d0-844f-13d09811d33d.png)


6. 
