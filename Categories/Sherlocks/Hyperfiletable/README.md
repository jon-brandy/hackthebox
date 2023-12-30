# Hyperfiletable
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/210fd377-ebdc-42a1-8304-4300f8b7e0fc)


## Lessons Learned:
- sdasd

## SCENARIO:
There has been a new joiner in Forela, they have downloaded their onboarding documentation, however someone has managed to phish the user with a malicious attachment. 
We have only managed to pull the MFT record for the new user, are you able to triage this information?

## STEPS:
1. In this challenge we're given a raw data file of MFT record for the new user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9e4f3b11-5442-4fde-b8aa-403bb4a309fa)


2. To analyze this file, we need to parse it first.
3. To parse the file I used **analyzeMFT**.


## IMPORTANT LINKS

```
https://andreafortuna.org/2017/07/18/how-to-extract-data-and-timeline-from-master-file-table-on-ntfs-filesystem/
https://github.com/dkovar/analyzeMFT
```
