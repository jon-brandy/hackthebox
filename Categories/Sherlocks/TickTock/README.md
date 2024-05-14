# TickTock
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c3aac728-10f3-4ffc-8344-fa0f7699be18)


## Lessons Learned:
- sadasd

## SCENARIO:

<p align="justify">
Gladys is a new joiner in the company, she has recieved an email informing her that the IT department is due to do some work on her PC, she is guided to call the IT team where they will inform her on how to allow them remote access. The IT team however are actually a group of hackers that are attempting to attack Forela.
</p>

## STEPS:
1. In this case, we're tasked to investigate a malicious remote access connection through the logs given.
2. Based from the scenario and the questions, we can conclude that a new employee gets a call from the attacker to allow them remote access to her PC. After they get a TeamViewer connection, they also launch a C2 agent. 

> ARTIFACTS GIVEN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5decd5b4-7c6b-4a00-a791-7ecc902d4e30)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0a3a50b3-026c-41d4-9135-e51ad91b7bbb)


3. It seems we're gonna dealing with parsing **Master File Table** and reviewing Windows Event Logs if needed.


> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a2a5b43-ad89-4a75-923c-6d1e79375e39)


4. Since the initial entry is from the **gladys** PC, where she allowed the attacker to do remote access to her PC. Let's check the log file inside her directory for any remote access application avail.

```
Navigating through --> /C/Users/gladys/AppData/Local/
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a68ffb92-4da2-4719-878c-cb70e147f6bc)


5. Seems we identified what remote access application gladys used, it's **TeamViewer**. Now let's review the log start by the **TeamViewer15_Logfile.log**

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/333fef0c-099b-49fc-b908-8fb14a3ff875)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb701865-a5b7-41ee-a783-b0f7c152e96b)







> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a66d9f4-a934-46dd-85fb-5ffb9c44b945)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/77210ffa-b07a-46c3-8ef5-07722ed7e8d6)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68f1a606-026e-4cba-84bf-055222807c00)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f77df07-0fb5-4a38-9916-c908b9c46c14)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4ce8c9b4-139f-421a-bbc9-12dfdaf58093)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54560c19-0fbb-4d51-8556-138a3bcca3b3)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/508aad12-731d-437d-83c7-c81c1dcb18e3)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/077adf97-e116-4fa7-aa0b-6c891ade17ae)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a67891d5-2989-4f21-92c0-1f2878b4d3df)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d53a6817-f667-44b3-9f74-acd9422cb6e6)
