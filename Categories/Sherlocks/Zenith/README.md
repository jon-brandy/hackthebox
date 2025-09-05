# Zenith
> Write-up author: jon-brandy

<img width="386" height="157" alt="image" src="https://github.com/user-attachments/assets/66817db9-68c5-40f5-978f-c5a997e25051" />


## Lessons Learned:
1. E-mail Forensics.
2. Parse event logs using `Hayabusa` and `EvtxEcmd`.
3. Using `Timeline Explorer` to review parsed event logs.
4. Static binary analysis using `pestudio`, `ghidra`, and manual detonation using `Flare-VM`.

## SCENARIO:
<p align="justify">We are contacting you with an urgent request concerning a potentially suspicious email that was recently received and unfortunately opened by one of our team members. As a construction company (Caymine builders), we regularly engage in project discussions with clients, and this email appeared to contain a project plan in PDF format. However, after further review, we have reason to believe this email and its attachment could be malicious. Despite our usual security protocols, the PDF was opened on one of our systems, which has raised significant concern regarding the security of our network.</p>

## STEPS:
1. In this case, we were tasked with investigating a phishing incident involving an email that contained a malicious PDF. Unfortunately, the PDF was opened, and the client is concerned about the security of their network.

> Artifacts given

<img width="1130" height="656" alt="image" src="https://github.com/user-attachments/assets/d9c4b8e7-1be5-48d9-9877-ebe224c9efd3" />

> 1ST QUESTION -> ANS: `2024-09-19 17:44:11`

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/79a50e11-370b-4033-92bc-ec4f7ea4ef8b" />

2. To identify the timestamp of the e-mail retrieval, we can review the available e-mail artifacts and analyze the message headers.

<img width="844" height="266" alt="image" src="https://github.com/user-attachments/assets/2e6345bf-34c3-4cdb-8990-581feaaa536a" />

> In VSCODE

<img width="2328" height="1097" alt="image" src="https://github.com/user-attachments/assets/161f8893-597b-426d-acf9-462b4407c528" />

3. The e-mail headers clearly show the message components and include the timestamp indicating when the Postfix MTA on `mail.caymine.htb` accepted and delivered the e-mail to the recipient’s mailbox (`felamos@caymine.htb`) at `Thu, 19 Sep 2024 17:44:11 UTC`.
4. Also, scrolling down below we can see the attached PDF file.

<img width="832" height="1000" alt="image" src="https://github.com/user-attachments/assets/d993dbc6-1faa-475c-94ac-62bdcdd1e4dd" />

5. To review the file, we can just decode the base64 using cyberchef then save it as PDF file.

<img width="1002" height="1189" alt="image" src="https://github.com/user-attachments/assets/089539fe-fcdb-4010-bd23-d6ef8cdd5fd6" />


> 2ND QUESTION -> ANS: `2024-09-18 13:57:04`

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/2faca0be-2c8f-4be1-a7c7-98a3729303e6" />

6. To identify the creation file timestamp, we can use `exiftool` in Linux to check for its metadata.



> 3RD QUESTION -> ANS: `downtown_construction_project_plan.pdf`

<img width="1275" height="196" alt="image" src="https://github.com/user-attachments/assets/1d4a3384-61ca-436d-a685-6b132970734f" />


> 4TH QUESTION -> ANS: `2024-09-18 21:19:18`

<img width="1282" height="196" alt="image" src="https://github.com/user-attachments/assets/7355cb64-0b3d-4d9c-8486-801efd42c871" />


> 5TH QUESTION -> ANS: `exit`

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/e4281f82-c4f2-4a02-9f1f-d8a4c58bd107" />


> 6TH QUESTION -> ANS: `C:\Users\Public\test.exe`

<img width="1282" height="200" alt="image" src="https://github.com/user-attachments/assets/0fa4daf4-4896-47fc-b2f8-fec035c3e668" />


> 7TH QUESTION -> ANS: `WindowsPooler`

<img width="1283" height="198" alt="image" src="https://github.com/user-attachments/assets/f75af8bd-3a83-4df1-9540-bf7c0529e5d0" />


> 8TH QUESTION -> ANS: `explorer.exe`

<img width="1280" height="200" alt="image" src="https://github.com/user-attachments/assets/ae4c3b09-b24c-4362-9cf2-002da21aef71" />


> 9TH QUESTION -> ANS: `Windows7`

<img width="1281" height="202" alt="image" src="https://github.com/user-attachments/assets/7e91a7bd-4236-476a-a6da-330b10165b9f" />


> 10TH QUESTION -> ANS: `Adobe Reader 9`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/1c6b31b2-6094-4b28-afe9-4ed52806e9e2" />


> 11TH QUESTION -> ANS: `2024-09-19 17:48:31`

<img width="1275" height="197" alt="image" src="https://github.com/user-attachments/assets/74c1dbb5-0fca-4b5a-b4cb-0ac4692ef9c8" />


> 12TH QUESTION -> ANS: `2024-09-19 17:50:17`

<img width="1283" height="198" alt="image" src="https://github.com/user-attachments/assets/aa2915e5-eaea-44b0-8d77-68741f8afb29" />


## REFERENCES:

```
https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32firstw
https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
```
