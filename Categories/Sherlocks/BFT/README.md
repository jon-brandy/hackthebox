# BFT
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bfaf309d-3852-4098-ba7f-fe722f04cb51)


## Lessons Learned:
- Parsing Master File Table (MFT) raw file using MFT Explorer.
- Using MFTECmD to convert MFT raw file to csv.

## SCENARIO:

In this Sherlock, you will become acquainted with MFT (Master File Table) forensics. You will be introduced to well-known tools 
and methodologies for analyzing MFT artifacts to identify malicious activity. During our analysis, you will utilize the MFTECmd 
tool to parse the provided MFT file, TimeLine Explorer to open and analyze the results from the parsed MFT, and a Hex editor 
to recover file contents from the MFT.


## STEPS:
1. In this task we're given a MFT file which we can analyze using MFT Explorer. But I prefer to analyze it by converting the raw MFT file to a .csv format.
2. Then analyze the CSV file with MFT Explorer or Timeline Explorer (both can be used to analyze the .csv file).
3. To convert the raw MFT file to .csv format, you can either use `analyzeMFT` or `MFTECmD.exe`. Both also can be used for the same purpose.

> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6838e00-5a77-458f-ab52-7d544a525ebe)


4. For this writeup, I used `MFTECmD.exe` to convert the raw MFT to .csv file.

> Converting mft.raw file to .csv file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a5a79e2f-1029-4a2c-9df4-ed1ea2968957)


5. Now let's upload it to `Timeline Explorer`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/39d7836a-1b65-4c79-93c4-f8381a708ac6)


6. The easiest way to identify the zip filename which Simon downloaded at 13th February, we just have to search for `.zip` and correlate the timestamp.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/86a998d8-397d-4c1a-9303-8ed5fb95a88e)


7. Found one zip file that looks convincing based on it's timestamp and it's file path.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e1bf4356-751f-4e34-99f2-12aee2bb2dd3)


8. However, found another zip file that downloaded at the same date. Interesting.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2edaf7cc-e593-4b47-ab45-e932e82fc40b)


9. Now 

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
