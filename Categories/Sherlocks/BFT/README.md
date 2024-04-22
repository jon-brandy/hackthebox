# BFT
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bfaf309d-3852-4098-ba7f-fe722f04cb51)


## Lessons Learned:
- Parsing Master File Table (MFT) raw file using MFT Explorer.
- Using MFTECmD to convert MFT raw file to csv.
- Identify downloaded malicious file.

## SCENARIO:

In this Sherlock, you will become acquainted with MFT (Master File Table) forensics. You will be introduced to well-known tools 
and methodologies for analyzing MFT artifacts to identify malicious activity. During our analysis, you will utilize the MFTECmd 
tool to parse the provided MFT file, TimeLine Explorer to open and analyze the results from the parsed MFT, and a Hex editor 
to recover file contents from the MFT.


## STEPS:
1. In this task we're given a MFT file which we can analyze using MFT Explorer. But I prefer to analyze it by converting the raw MFT file to a .csv format.
2. Then analyze the CSV file using Timeline Explorer.
3. To convert the raw MFT file to .csv format, you can either use `analyzeMFT` or `MFTECmD.exe`. Both also can be used for the same purpose.

> 1ST QUESTION --> ANS: Stage-20240213T093324Z-001.zip

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


8. However, found another zip file that resides in the Download directory. Interesting!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2edaf7cc-e593-4b47-ab45-e932e82fc40b)


9. To improve the visibility, I sorted the parent path then custom the filter for only `Downloads` directory of user Simon.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/97f3315b-4b05-4a83-abab-48ce65dcea44)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9715566-3d7b-430b-840f-1bc6bb5df538)



10. Great! Based from the results above, seems there are only 2 .zip files inside Simon `Downloads` directory at 13th February 2024.
11. Further analysis, found that `Stage-20240213T093324Z-001.zip` is unzipped and has another .zip file inside it named `invoices.zip`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9631bebb-c611-461e-9ebf-399e505e1e2e)


12. Then found out a .bat file inside invoice.zip. This is absolutely indicating a malicious file.

#### Notes

```
A .bat file is a batch file in Windows, which is essentially a script containing a series of commands that are
executed in sequence. These files are often used to automate tasks or run multiple commands at once.
```

13. Noticed the file size is only 286 bytes. Hence it should be stored directly at the MFT entry.

#### Notes

```
When a file is small enough to be stored entirely within the MFT record, it can improve access times because the file
data can be read directly from the MFT without the need to access additional disk sectors. This technique is often used
for system files and other small files that are frequently accessed.
```


14. Knowing this, then let's analyze invoice.bat's content by uploading raw MFT file using `MFT Explorer`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bae66771-6510-4e1d-a827-553cc186c664)


15. Based from the result above, we can see there is a C2 IP and it's port which are as the web server to download a file.
16. Great! We hunted the malicious file then.

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
