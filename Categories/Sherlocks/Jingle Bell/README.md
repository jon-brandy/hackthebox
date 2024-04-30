# Jingle Bell
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5971ad1c-2977-47e0-951e-2fc180541d05)


## Lessons Learned:
- Using sqlitebrowser to reviewing sqlite3.db file.

## SCENARIO:

<p align="justify">
Torrin is suspected to be an insider threat in Forela. He is believed to have leaked some data and removed certain applications from their workstation. They managed to bypass some controls and installed unauthorised software. Despite the forensic team's efforts, no evidence of data leakage was found. As a senior incident responder, you have been tasked with investigating the incident to determine the conversation between the two parties involved.
</p>

## STEPS:
1. As a senior incident responder, we're tasked to investigate an incident in Forela. It is believed that **Torrin** leaked some data and removed certain applications from Forela workstation.
2. We're given these files:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0e09cc43-806e-4d73-82c4-f38a62aea066)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eee76dfd-2fe2-4c9d-b8c0-4eab7ef2eb55)


> 1ST QUESTION --> ANS: Slack

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c2ce1b8d-616c-4ca1-b896-388c9c43bad5)


3. Upon reviewing the DB file given, we can identify the tool used by Torrin to leak Forela's data by reviewing the `notification` table.
4. Noticed an application seems to be our interest among all 23 rows.
5. It's `slack` application.

#### NOTES:

```
Slack is a cloud-based communication platform primarily used for workplace collaboration. It allows teams tocommunicate
in real-time through channels organized by topic, as well as through direct messaging. Users can share files, integrate
with other tools and services, and search through conversations and files easily.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/466a299c-d761-4ec5-8d74-fc7bf63305c5)


6. Further checking, we identified a conversation between `PrimeTech Innovations` company, especially the Dev team.
7. It asked **Torrin** whether he managed to find the files related to Forela Oil Extraction Plan in Angola.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e28cd9e1-c98b-44e7-9ba0-ec3258100d79)


8. It's clear then, that **Torrin** using `slack` to leak Forela's secret.

> 2ND QUESTION --> ANS: PrimeTech Innovations

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/758d8d97-0806-4537-9084-09e2d2e2ba29)


9. Based from our previous finding, it's clear that **Torrin** tried to leak Forela's data to `PrimeTech Innovations` company.


> 3RD QUESTION --> ANS: Cyberjunkie-PrimeTechDev

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6afcb584-942c-42e5-9bf5-e85b4f60f55b)


10. Again, based from our previous finding, **Torrin** communicated with user `Cyberjunkie-PrimeTechDev`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0a1fcba4-307d-443e-bfd9-593af1a988b2)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3586d6c1-7331-49c9-8a2d-bdb7e1f5237a)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/053d5052-f9cc-4983-9244-507c881c75fa)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc976d2f-5298-4698-865d-7ed624ced886)


> 7TH QUESTION --> ANS:



> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/36becd05-8e17-4bbd-b8b3-1f3829756bcb)


