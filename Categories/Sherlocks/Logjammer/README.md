# Logjammer
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7f39ebc6-1bf6-4352-8165-e19d86fb2006)

## Lesson learned:
- Windows event log analysis.

## Sherlock Scenario:
You have been presented the opportunity to work as a junior DFIR consultant for a big consultancy, however they have provided a technical assessment for you to complete. 
The consultancy Forela-Security would like to gauge your knowledge on Windows Event Log Analysis. Please analyse and report back on the questions they have asked.

## STEPS:
1. In this challenge we're given several windows event logs. 

> 1ST QUESTION --> ANS: `27/03/2023 14:37:09`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5a0b7dda-6ffa-4234-a8dc-d606ffca3564)


2. To identify the timestamp, we need to analyze the **Security** or **Security_1** log.
3. Long story short, after sorted the timestamp from the oldest to newest, found a logon attempt with explicit credentials (eventID -> 4648) and **cyberjunkie** as it's username.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2d1e7efa-7b4f-4036-a646-53c5b9f7d08e)


4. However, it does not explain whether the login attempt is succesfull or not. It can be successfully or it can't be.
5. But it concludes that this is the 1st attempt.
6. Hence let's convert the timestamp tp UTC using this online tool --> `https://dateful.com/convert/utc`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/86b45242-3f52-4ed0-a1b9-f831f87cddf6)


> 2ND QUESTION --> ANS: Metasploit C2 Bypass

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/333779a9-2bff-4554-84c7-f79130644319)

7. Analyzing the **Windows Firewall-Firewall** shall let us identify the name of the firewall rule added. 


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0a9605c0-f6e1-46a8-acdc-f26ddd521d37)



Upon an

> 3RD QUESTION --> ANS: Outbound

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f880250-44d7-4ad9-aa5f-0838a36845e9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/036c6743-c20e-427d-9d64-c697ca9015d5)


> 4TH QUESTION --> ANS: Other Object Access Events

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/20348858-350d-47ed-89c5-136bf96addd3)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1887ca59-a2df-4c18-bdd5-1b270ae92c5e)



> 5TH QUESTION --> ANS: HTB-AUTOMATION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1836c8d0-253d-4b9c-9a54-ae9d1e7310e2)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5864036-b3ca-421d-8c64-0ee0ef2d9e6c)



> 6TH QUESTION --> ANS: C:\Users\CyberJunkie\Desktop\Automation-HTB.ps1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b24fc2a-c67f-4529-afff-5285417adac1)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68c9003f-7ab3-4ef8-9024-1ec4945450b4)



> 7TH QUESTION --> ANS: -A cyberjunkie@hackthebox.eu

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/777a9b04-329f-4bcf-87e1-7eb3ec9b14b7)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1b09f60e-6ac5-4590-ac7c-98a9366a5e28)



> 8TH QUESTION --> ANS: SharpHound

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f34e9494-c82f-4b26-b30d-f77509fcf6cd)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9bc7137d-a956-4d7d-8971-9e1d68b33af1)


> 9TH QUESTION --> ANS: C:\Users\CyberJunkie\Downloads\SharpHound-v1.1.0.zip

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4c35cd98-c37f-4468-bb96-56af437cc905)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/48b1f3c6-dd95-48db-921d-e96fd5d95a8a)



> 10TH QUESTION --> ANS: Quarantine

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9099a991-0742-41d0-8fb5-dbc976592f53)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/43cf2235-70e8-489e-9c24-8de4c57154bf)


> 11TH QUESTION --> ANS: Get-FileHash -Algorithm md5 .\Desktop\Automation-HTB.ps1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1335058a-1e50-4c29-82cc-2063b6c148b2)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2a109bd6-36aa-4f74-a968-a1ba5a81f81f)


> 12TH QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/45be88e2-405b-4c2f-8713-210b7b492559)


