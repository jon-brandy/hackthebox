# Noted
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9567cfe5-4323-4624-9df5-6caef66b4635)


## Lessons Learned:
1. SAD

## SCENARIO:

Simon, a developer working at Forela, notified the CERT team about a note that appeared on his desktop. 
The note claimed that his system had been compromised and that sensitive data from Simon's workstation had been collected. 
The perpetrators performed data extortion on his workstation and are now threatening to release the data on the dark web 
unless their demands are met. Simon's workstation contained multiple sensitive files, including planned software projects, 
internal development plans, and application codebases. The threat intelligence team believes that the threat actor made some mistakes, 
but they have not found any way to contact the threat actors. The company's stakeholders are insisting that this incident be resolved 
and all sensitive data be recovered. They demand that under no circumstances should the data be leaked. As our junior security analyst, 
you have been assigned a specific type of DFIR (Digital Forensics and Incident Response) investigation in this case. 
The CERT lead, after triaging the workstation, has provided you with only the Notepad++ artifacts, suspecting that the attacker 
created the extortion note and conducted other activities with hands-on keyboard access. Your duty is to determine how the 
attack occurred and find a way to contact the threat actors, as they accidentally locked out their own contact information.



## STEPS:
1. In this challenge, we're given 5 files.

> 1ST QUESTION --> ANS: C:\Users\Simon.stark\Documents\Dev_Ops\AWS_objects migration.pl

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0dd42171-8e8f-4eb3-98d8-e1620b706532)


2. To identify the full path of the script used by Simon for AWS operations, we just need to review the config file --> `config.xml`.
3. Inside the history tag, we can see the full path of it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/920fdfe5-31e3-42f2-8e86-045b0cd1ed88)


> 2ND QUESTION --> ANS: C:\Users\Simon.stark\Desktop\LootAndPurge.java

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6e72cd7b-af06-46c8-8aee-6e8cf5cfad00)


4. To identify which source file is duplicated by the attacker, we can check the session.xml file.
5. Reviewing the code, we can identify that .java is the only source file available there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b1463f7c-eff1-4872-bc53-4ed9d4668853)


6. To make sure that it is indeed our interest file, we can review the source file by following the criteria listed from the chall's description --> `This code gathered sensitive data and prepared it for exfiltration`.
7. Upon reviewing the code, we can identify 2 core functions called namely `collectFiles` and `createZipArchive` which used for preparation for data exfil.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/16999e12-e3f3-4066-b1d4-380efb3e8da2)

8. It's clear now that the .java source is the duplicated source.

> 3RD QUESTION --> ANS: Forela-Dev-Data.zip

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/76baed27-5a96-4eb6-8093-ad24d3619087)


9. Again, reviewing the .java source we can identified that the attacker stored all the data to a zip file named `Forela-Dev-Data.zip`.

> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bd00c2c7-e6b0-4f78-a74b-4c199619ae05)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31c92200-39fa-4364-9b93-cc2e26475e9f)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9d21e480-8f5e-478d-973c-d5dcfd2ba636)


