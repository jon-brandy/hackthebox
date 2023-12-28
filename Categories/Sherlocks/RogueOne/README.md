# RogueOne
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8a7c34cc-784b-4e1c-b9d4-baf9d3433187)


## Lessons Learned:
- Using volatility3 to conduct memory forensics.

## SCENARIO:

Your SIEM system generated multiple alerts in less than a minute, indicating potential C2 communication from Simon Stark's workstation. 
Despite Simon not noticing anything unusual, the IT team had him share screenshots of his task manager to check for any unusual processes. 
No suspicious processes were found, yet alerts about C2 communications persisted. The SOC manager then directed the immediate containment 
of the workstation and a memory dump for analysis. As a memory forensics expert, you are tasked with assisting the SOC team at Forela 
to investigate and resolve this urgent incident.

## STEPS:
1. In this challenge we're given a memory dump which we can analyze using volatility.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9bf2516-20ec-429e-9b5c-8a25f2fcad23)


> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/989f7f08-c3a9-499f-9f74-af9304baa108)


> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78eb4957-6a6e-4e01-83c5-52ce7faf7f90)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a46b2bd6-153c-4281-94b4-16ce0a8f128d)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59721088-9c05-4618-919a-b7e727afdee4)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/535cab90-f0d1-4ace-93f3-b767bac4c701)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/49f0b387-c048-40f2-88a3-23b2ab8c4e44)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/baf4d3cd-0517-43f9-a0e7-7d8c6416d516)

