# Jingle Bell
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5971ad1c-2977-47e0-951e-2fc180541d05)


## Lessons Learned:
- Using sqlitebrowser to reviewing sqlite3.db file.
- Slack Application Forensic (.DB) file.

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


> 4TH QUESTION --> ANS: forela-secrets-leak

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3586d6c1-7331-49c9-8a2d-bdb7e1f5237a)


11. Still from the same row's data, we can see the channel's name based from the **hashtag** usage.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4631c112-1e99-4b76-8e58-7f1a6d54e850)



> 5TH QUESTION --> ANS: Tobdaf8Qip$re@1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/053d5052-f9cc-4983-9244-507c881c75fa)


12. Reviewing row 18th, **Torrin** seems Cyberjunkie spilled the password archive server and he confirmed the password again.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed6b02ac-03dd-4757-8502-39e16c2127e6)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ea55312-6018-4cdf-a12a-6c77feb8beb0)


> 6TH QUESTION --> ANS: `https://drive.google.com/drive/folders/1vW97VBmxDZUIEuEUG64g5DLZvFP-Pdll?usp=sharing`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc976d2f-5298-4698-865d-7ed624ced886)


13. Reviewing the next row, Cyberjunkie sent **Torrin** the google drive link.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cf51db83-18d8-46a8-b16b-52172b983b51)


> 7TH QUESTION --> ANS: `2023-04-20 10:34:49`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/50d25893-d2f4-4c5b-a09c-b4cb893b1a19)


14. To identify the timestamp of when **Torrin** sends the google drive link to Cyberjunkie, simply convert the Unix timestamp to UTC using [this](https://www.epochconverter.com/) online converter.

> UNIX TIMESTAMP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6bb06ed8-a135-456e-9194-f2a13ea8d706)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18991e57-3624-45b5-9d87-0b919c9a7623)


> 8TH QUESTION --> ANS: £10000

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/36becd05-8e17-4bbd-b8b3-1f3829756bcb)



15. Reviewing the 22nd row, we can identified the bank account number along with the money to be transferred.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/15e3abf4-3799-4222-ba10-44dc31b72ba7)


16. We've finished investigatd the case!

## IMPORTANT LINKS

```
https://www.epochconverter.com/
https://slack.com/help/articles/360017938993-What-is-a-channel
```
