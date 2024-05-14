# TickTock
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c3aac728-10f3-4ffc-8344-fa0f7699be18)


## Lessons Learned:
- Reviewing TeamViewer logs (hunting C2 agent).

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


> 1ST QUESTION --> ANS: Merlin.exe

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a2a5b43-ad89-4a75-923c-6d1e79375e39)


4. Since the initial entry is from the **gladys** PC, where she allowed the attacker to do remote access to her PC. Let's check the log file inside her directory for any remote access application avail.

```
Navigating through --> /C/Users/gladys/AppData/Local/
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a68ffb92-4da2-4719-878c-cb70e147f6bc)


5. Seems we identified what remote access application gladys used, it's **TeamViewer**. Now let's review the log start by the **TeamViewer15_Logfile.log**

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/333fef0c-099b-49fc-b908-8fb14a3ff875)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb701865-a5b7-41ee-a783-b0f7c152e96b)


6. Long story short, upon reviewing the logs. Found an outbound connection at `11:21:34` from **Gladys** PC.
7. It downloaded a binary file named `Merlin.exe`. The binary stored at the desktop.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3c31f9f8-7ce4-45a1-8ba6-3156faed2ccb)

8. This could be the C2 Agent, but further checking is needed.
9. Upon reviewing the csv file which contains prefetch log, found that `Merlin.exe` is part of the prefetch. Meaning it's previously **Opened** or **Executed** on the PC.
10. It can be found at timestamp --> `11:51:15` row 63.
 
![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f31ceacb-cfcb-4ae6-9d73-3063d59d8cb2)


11. But again, we need more evidence whether it is indeed acts as a C2 agent.
12. Now let's review the Windows Event log.
13. The simplest way to identify whether the binary is malicious or not, we can start by reviewing the `Windows Defender` event log.
14. Long story short, found that `Merlin.exe` is logged inside the log.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a3652b77-7333-4e0f-84f2-054d3622a1df)


15. Reviewing the logs previous it, Windows Defender identified the malware's family name of `Merlin.exe` --> `VirTool:Win32/Myrddin.D`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1c90fbb4-21a1-4366-af91-6120837dc0ca)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27ea07dc-af5b-436b-b99e-b4217972de15)


16. So to summarize this up, `Merlin.exe` gets executed then quarantined by the Windows Defender, then it freed again.
17. Great! We hunted the C2 agent.

> 2ND QUESTION --> ANS: `-2102926010`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a66d9f4-a934-46dd-85fb-5ffb9c44b945)


18. Now, to identify the initial access's session ID, we need to review again the Team Viewer logfile.
19. Found that an initial connection started at `11:35:27` and the login attempt is at `11:35:27`, then it authenticated at `11:35:31`.
20. Which means the session ID is --> `-2102926010`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c2c6de0c-fc27-4ba0-a7c9-6e4e8e3f2c96)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/425adad3-1a78-4dbc-b39f-7b1339723ec4)


> 3RD QUESTION --> ANS: `reallylongpassword`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/77210ffa-b07a-46c3-8ef5-07722ed7e8d6)


21. To identify this event where the attacker attempted to set a bitlocked password on the C drive, we need to review Windows Powershell event log.
22. Found an interesting powershell execution at `18:14:33`, the contents are encoded with base64.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/98700fd8-d07d-4b8e-b30c-f7ead928857f)


23. Upon decoding it, it's indeed the command used by the attacker to mount the C drive. Also we identified the password used.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/240b9cf0-7016-4437-ab84-208ded626901)


> 4TH QUESTION --> ANS: `fritjof olfasson`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68f1a606-026e-4cba-84bf-055222807c00)


24. Next, to identify the name used by the attacker, again we need to review the TeamViewer logfile.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d9c3d1f7-be39-43fa-b929-1450ccd47407)


25. Based, from the evidence above, after the attacker authenticated. It saved the session and saved the local participant as `1764218403`.
26. Not long after it, around 4 seconds later, we can identified 2 participants inside the same session.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/efc8f4bb-8358-4df4-9665-f00a16fc5c22)


27. The first one, likely is Gladys PC's Hostname. The other one should be the attacker --> `fritjof olfasson`.

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
