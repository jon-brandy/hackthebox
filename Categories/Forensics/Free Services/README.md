# Free Services
> Write-up author: jon-brandy
## DESCRIPTION:
Intergalactic Federation stated that it managed to prevent a large-scale phishing campaign that targeted all space personnel across the galaxy. 
The enemy's goal was to add as many spaceships to their space-botnet as possible so they can conduct distributed destruction of intergalactic services (DDOIS) using their fleet. 
Since such a campaign can be easily detected and prevented, malicious actors have changed their tactics. As stated by officials, a new spear phishing campaign is underway aiming high value targets. 
Now Klaus asks your opinion about a mail it received from "sales@unlockyourmind.gal", claiming that in their galaxy it is possible to recover it's memory back by following the steps contained in the attached file.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211980542-533c48b0-ff60-4a9d-a229-e0f00c11f5fb.png)


![image](https://user-images.githubusercontent.com/70703371/211980644-45faf4b6-d077-4bdf-b361-29fc28c97967.png)


![image](https://user-images.githubusercontent.com/70703371/211981425-cf0977a4-1779-4934-a280-49867f3b538c.png)


2. Well we can't view this file in kali linux, let's open it in windows.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212715812-12b7ed6a-5c31-42d9-9276-ac333d1d87f2.png)


3. At the other sheet, we got this:

![image](https://user-images.githubusercontent.com/70703371/212715911-e83a5e66-6e2f-4b2c-ad3e-c3a13bff949b.png)


4. Based from the macro formula we got at Macro1, we know that all the integer values in column E, F, and G are XORed with 24.

![image](https://user-images.githubusercontent.com/70703371/214282711-5a90ae43-aa07-48da-a0f3-cb1a705f9b96.png)


5. The logics of XOR, if we XOR it again, the original value shall returned.
6. First saved the macro sheet as `macroFile.csv`.

