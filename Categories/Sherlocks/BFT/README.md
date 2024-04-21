# BFT
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bfaf309d-3852-4098-ba7f-fe722f04cb51)


## Lessons Learned:
- Parsing Master File Table (MFT) raw file using MFT Explorer.
- Using analyzeMFT to convert MFT raw file to csv.

## SCENARIO:

In this Sherlock, you will become acquainted with MFT (Master File Table) forensics. You will be introduced to well-known tools 
and methodologies for analyzing MFT artifacts to identify malicious activity. During our analysis, you will utilize the MFTECmd 
tool to parse the provided MFT file, TimeLine Explorer to open and analyze the results from the parsed MFT, and a Hex editor 
to recover file contents from the MFT.


## STEPS:
1. In this task we're given a MFT file which we can analyze using MFT Explorer. 

> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6838e00-5a77-458f-ab52-7d544a525ebe)


2. Now let's convert the mft.raw file to a csv file using `analyzeMFT` python script.
3. Next, we can use it to the MFT Explorer.

> Converting mft.raw file to .csv file.




> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/67acd946-ad3b-464d-8721-009130d27a14)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4bfc30b-fbfc-4c8d-aff7-f625a576de33)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/832cd8ff-b6c5-46a6-b1fe-e295b84ae818)



> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/082f4e7c-4f96-4172-b568-ac812da368b1)



> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/47ac6334-4072-46e0-ba7d-e5be553442f4)
