# Hyperfiletable
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/210fd377-ebdc-42a1-8304-4300f8b7e0fc)


## Lessons Learned:
- Parsing raw mft data using analyzedMFT.py
- 

## SCENARIO:
There has been a new joiner in Forela, they have downloaded their onboarding documentation, however someone has managed to phish the user with a malicious attachment. 
We have only managed to pull the MFT record for the new user, are you able to triage this information?

## STEPS:
1. In this challenge we're given a raw data file of MFT record for the new user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9e4f3b11-5442-4fde-b8aa-403bb4a309fa)


2. To analyze this file, we need to parse it first.
3. To parse the file I used **analyzeMFT** and convert the output to .csv file.

```
python3 'C:\CTF\TOOLS-FOREN\analyzeMFT\analyzeMFT.py' -f .\mft.raw -o analyzed_mft.csv
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d20d5f3b-5563-4df5-aa7e-0da650204c47)

> 1ST QUESTION --> ANS: 3730c2fedcdc3ecd9b83cbea08373226

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/05226cef-3ce0-4714-b307-bf26447616ae)


4. To get the MD5 hash of the MFT, we can use md5sum command in Linux.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9e6b248c-048e-40ae-a406-9feb5b82f9dc)


> 2ND QUESTION --> ANS: Randy Savage

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5a89a8df-a628-4d3b-86b1-73462c5387fe)


5. To identify the user's name on the system, we can filter our search with this --> `/Users/`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5240e0df-0e42-4961-b259-09ca63176ffd)


6. **Randy Savage** stands out as the only user we can see here.

> 3RD QUESTION --> ANS: Onboarding.hta

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6434cc11-abfb-46ad-9a85-7d596254a627)


7. To get the malicious filename, I start by searching .hta and it resulting to only 1 filename namely --> Onboarding.hta.
8. This concludes that it is indeed the malicious file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9d7d23e-5ffb-4ca8-b2b2-47129948f14b)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/afb69561-172b-42ee-9e00-0d1adec8b87f)


9. To identify the ZoneIdentifier of the download for the malicious HTA file, we can lookfor 

> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d2855386-f550-4511-8db9-af380a4461cf)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e2059637-730a-41dc-af25-be9af334a015)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c664039a-81b4-49aa-84db-543e4e9788cc)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd9609be-f7b0-4a44-b610-a9324b0c59ce)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3b042188-9781-41d1-9007-8a6310b09d33)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d5a5b2b4-6e13-46c6-9888-5ddee4659e54)




## IMPORTANT LINKS

```
https://andreafortuna.org/2017/07/18/how-to-extract-data-and-timeline-from-master-file-table-on-ntfs-filesystem/
https://github.com/dkovar/analyzeMFT
```
