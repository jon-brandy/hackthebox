# Subatomic
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/7619feaa-40d4-4b8d-8cd5-5fe71e5a31d1)


## Lesson(s) Learned:
1. sda

## SCENARIO:

<p align="justify">Forela is in need of your assistance. They were informed by an employee that their Discord account had been used to send a message with a link to a file they suspect is malware. The message read: "Hi! I've been working on a new game I think you may be interested in it. It combines a number of games we like to play together, check it out!". The Forela user has tried to secure their Discord account, but somehow the messages keep being sent and they need your help to understand this malware and regain control of their account! Warning: This is a warning that this Sherlock includes software that is going to interact with your computer and files. This software has been intentionally included for educational purposes and is NOT intended to be executed or used otherwise. Always handle such files in isolated, controlled, and secure environments. One the Sherlock zip has been unzipped, you will find a DANGER.txt file. Please read this to proceed.</p>

## STEPS:
1. A Discord account has been compromised and is being used to send messages containing a link to a suspected malicious file. Despite the owner's efforts to secure the account, the messages continue to be sent.
2. As forensic analysts, our task is to investigate the incident and analyze the malware to understand its behavior and regain control of the account.
3. Unzipping the zip file shall resulting to 2 files. Those are **.txt** file and the zipped malware binary.

![image](https://github.com/user-attachments/assets/a4859d6d-4738-4fcb-a8df-9ae2ea0505c8)

> Danger.txt

![image](https://github.com/user-attachments/assets/15b5fe39-d4d5-4e41-bf8f-37fe7b691e37)


4. Unzipping the **malware.zip** file using the provided password, shall resulting to a binary named **nsis-installer.exe**.

![image](https://github.com/user-attachments/assets/3d5ea2ad-681b-409a-b80f-928fc65a8c20)


> 1ST QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/410dbded-ea3d-4810-85a7-f1ab96265ef3)


5. To identify the **imphash** of this malware installer, we can simply grab the checksum and load it at virus total.
6. In **Window Powershell** terminal, we can use this command:

```
Get-Filehash .\nsis-installer.exe -Algorithm <checksum_you_want>
```

![image](https://github.com/user-attachments/assets/2eb19355-bad4-4fcb-8960-62a2b7bba0eb)


> RESULT AT VIRUS TOTAL

![image](https://github.com/user-attachments/assets/2dd3e64c-1db4-400b-ac31-7c80f88e1bbd)



> 2ND QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/5de05f00-3bc8-4a96-a66f-3a1673754327)


> 3RD QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/4131d86e-5199-45b8-920c-396c49305b96)


> 4TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/87cfee9b-69f2-4243-900f-3397b8f18397)


> 5TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/32b38bf1-d4cf-48a4-b8ee-5d51248508ce)


> 6TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/4fb2fde3-b386-4402-8d00-fa3e71bfd8f4)


> 7TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/8d3f126d-7893-4c2c-bad0-0701b26ee91d)


> 8TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/9191e24b-562f-490a-b4a9-c6fa306cf94a)


> 9TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/cad17c45-bb9a-4d48-a6ed-a3034d6eb855)


> 10TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/7893cb57-ef91-43d4-b3df-5a79a0c81e45)


> 11TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/254bb4b9-423d-4069-a2c8-3c3faa0ca93c)


> 12TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/b8921284-21c9-413f-a332-78432de9550e)


> 13TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/54ed6588-8c39-422f-b6d8-466d6ba9fdc3)



## IMPORTANT LINK(S):

```

```
