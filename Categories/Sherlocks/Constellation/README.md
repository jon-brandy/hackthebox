# Constellation
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ba2e1093-d5e6-4c40-8216-af5076a4b300)


## Lessons Learned:
- sadasd

## SCENARIO:
<p align="justify">
  The SOC team has recently been alerted to the potential existence of an insider threat. The suspect employee's workstation has been secured and examined. During the memory analysis, the Senior DFIR Analyst succeeded in extracting several intriguing URLs from the memory. These are now provided to you for further analysis to uncover any evidence, such as indications of data exfiltration or contact with malicious entities. Should you discover any information regarding the attacking group or individuals involved, you will collaborate closely with the threat intelligence team. Additionally, you will assist the Forensics team in creating a timeline. Warning : This Sherlock will require an element of OSINT and some answers can be found outside of the provided artifacts to complete fully.
</p>

## STEPS:
1. In this challenge we're tasked to do further analysis of artifacts which extracted by the IR team. Based from the artifacts, we're told to do information gathering regarding all individuals involved in this incident and collaborate with the Threat Intelligence team.
2. We've recieved 2 artifacts:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/84ca4c81-048a-4bf1-9a6a-d8256b9b35fc)


> PDF CONTENT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/87e56423-34db-4808-a3e9-28939f905be7)


> IOC CONTENT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc75456f-33c8-478b-811e-06d00f1e8698)


> 1ST QUESTION --> ANS: `2023-09-16 16:03:37`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eff7f229-5af5-4c46-901e-5ee441911711)


3. Based from the scenario and the IOC's link, we can speculate that the communication between the suspect and the actor group are done by discord.
4. Hence the PDF file timestamp can be used to identify the initial communication between the suspect and the attacker group.
5. To find the timestamp I used [this](https://dfir.blog/unfurl/) online threat intelligence tool named `unfurl`.
6. Copy the discord link from the IOC file and paste it to the tool.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a503a2f0-4290-4949-b60c-6f6606452d85)

7. The correct initial timestamp is at the first index.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a3e5ba02-1608-4db1-b444-4049f62f8060)


> 2ND QUESTION --> ANS: NDA_Instructions.pdf

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3d6a642-19f6-449d-99dc-8c8cf11d4852)


8. It's clear, that the attack group sent the `NDA_Instructions.pdf` through discord.

> 3RD QUESTION --> ANS: `2023-09-27 05:27:02`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ee7bf1b0-8c12-4b1e-8272-6af79567b41d)


9. Again, still using the same online tool, we can identified the initial timestamp of when the attack group sent the pdf file to the suspect.
10. Simply check for `File ID` branch.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8fefcff-db22-4f86-89e7-ddbb9fd1a63a)


> 4TH QUESTION --> ANS: `How to zip a folder using tar in linux`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/09061d1d-9028-4acd-b060-274a335cb535)


11. Now, reviewing the other link inside the IOC file, seems the attack group query `how to zip a folder using tar in linux` with google. Again, based from this condition and previous IOC, we can speculate that the attack group want the suspect to exfiltrates all the internal information to a folder then zip it using tar in linux.

> 5TH QUESTION --> ANS: `how to archive a folder using tar i`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ebdb8cf6-487e-41f3-88d0-11e8777e29d9)


12. However, if we reviewed it carefully, it seems the attack group queried another thing --> `how to archive a folder using tar i`. 

> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37743e99-d015-4dff-b7e4-c59fcbc30d70)



> 7TH QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/336a8237-90a3-4af9-94e2-e54b5e79fe49)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b2b6906-fc91-4468-be70-62c26ee96610)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c78303be-9c2a-4f36-a789-2e60bcfe418d)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ea88256-3146-4c41-8720-2e9ab8226055)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/00d6f74d-7377-4838-9dc2-46c948d6e3bc)

