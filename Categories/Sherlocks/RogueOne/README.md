# RogueOne
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8a7c34cc-784b-4e1c-b9d4-baf9d3433187)


## Lessons Learned:
- Using volatility3 to do memory forensics.

## SCENARIO:

Your SIEM system generated multiple alerts in less than a minute, indicating potential C2 communication from Simon Stark's workstation. 
Despite Simon not noticing anything unusual, the IT team had him share screenshots of his task manager to check for any unusual processes. 
No suspicious processes were found, yet alerts about C2 communications persisted. The SOC manager then directed the immediate containment 
of the workstation and a memory dump for analysis. As a memory forensics expert, you are tasked with assisting the SOC team at Forela 
to investigate and resolve this urgent incident.

## STEPS:
1. In this challenge we're given a memory dump which we can analyze using volatility.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9bf2516-20ec-429e-9b5c-8a25f2fcad23)


