# Malevolent ModMaker
> Write-up author: jon-brandy

<img width="486" height="148" alt="image" src="https://github.com/user-attachments/assets/27faddcc-836d-40c6-84fd-0520317e57ff" />


## Lessons Learned:
1. Dynamic binary analysis using `x64dbg`.
2. Static binary analysis using `ghidra`, `pestudio`, and `CFFExplorer`.

## SCENARIO:
<p align="justify">Bob, a senior software engineer at Acme Inc., was taking a break from correcting AI code to check in with his favorite gaming community. One of the newer members shared a new program that can make mods for a popular game. Eager to try new things, when he ran it as administrator (as instructed), all of his files were deleted and replaced! He immediately called the help desk, so they locked his machine and an incident response was called!</p>

## STEPS:
1. In this case, we were tasked with investigating an incident where, after a senior software engineer downloaded and executed a program advertised as a modding tool for popular games, it instead encrypted all of his files and deleted the originals.
2. The scope of the investigation is relatively small. We were specifically asked to analyze the malware based on a set of defined questions. The provided artifacts for analysis are shown in the red box below:

<img width="585" height="337" alt="image" src="https://github.com/user-attachments/assets/2bf15621-a10f-49a6-8902-0194aeeae5d9" />


> 1ST QUESTION -> ANS: `ransomware`

<img width="1281" height="205" alt="image" src="https://github.com/user-attachments/assets/1ed8b46b-5c62-4352-9bcb-ffe51e3d04e9" />

3. Based on the incident scenario and the provided artifacts, we can clearly attribute this malware infection to ransomware.

<img width="816" height="287" alt="image" src="https://github.com/user-attachments/assets/6a2cceb5-6d0e-469c-bc90-83fb39a91251" />


> 2ND QUESTION -> ANS: `webhook`

<img width="1279" height="198" alt="image" src="https://github.com/user-attachments/assets/c14514c3-6446-4e2e-9958-6da3b47ebdaf" />

4. Instead of manually reviewing the source code, I chose to detonate the binary and observe what happens to the sandbox environment.
5. After detonating the malware (MCModMaker-v1.4.exe), a terminal window appeared showing a failed outbound POST request to Discord (its C2 server), which was attempted via a webhook.

<img width="989" height="267" alt="image" src="https://github.com/user-attachments/assets/b482edb0-77b8-493d-bfdc-ab6e0c60470f" />


> 3RD QUESTION -> ANS: `powershell -ep bypass`

<img width="1279" height="197" alt="image" src="https://github.com/user-attachments/assets/7c3a00d2-832a-43b5-afd9-553baa6bec64" />

6. To identify which commands were used to execute binaries and scripts, I manually debugged the sample in xDbg, pausing execution just before the webhook was called.
7. The simplest approach is to search for error strings or any other strings of interest. In this case, I focused on debugging-related terms, since earlier the malware printed error messages to the terminal when its outbound connection to the Discord webhook failed.
8. Filtering for the string `discord` in xDbg produced several hits. The bottom four entries are likely the most relevant to our analysis.

<img width="889" height="709" alt="image" src="https://github.com/user-attachments/assets/1990a958-c58f-4063-bb5d-9578e8fe794c" />

9. Inspect the offset then scrolled-up we can identify `powerhsell -ep bypass` is used to perform request with curl to several domains.

<img width="1287" height="903" alt="image" src="https://github.com/user-attachments/assets/b8630e6f-8ba2-48bb-9888-d70372bbbaa8" />


> 4TH QUESTION -> ANS: `ZVBOKX3P8H7`

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/bcd9bd8f-7338-4f50-b719-182dc1a2522f" />

10. Based on our previous findings, we can clearly identify that hunnid[.]htb is the API used to perform geolocation enumeration, as it makes use of several parameters directly related to geolocation.

<img width="1236" height="194" alt="image" src="https://github.com/user-attachments/assets/f587e602-cfff-4c24-a0b6-53b446345d92" />

11. The API key is also presented in cleartext -> `ZVBOKX3P8H7`.

> 5TH QUESTION -> ANS: `goteem.htb`

<img width="1284" height="198" alt="image" src="https://github.com/user-attachments/assets/f70cc14b-65a1-431f-916f-2d01c17b5a06" />


> 6TH QUESTION -> ANS: `application/json`

<img width="1284" height="202" alt="image" src="https://github.com/user-attachments/assets/bfb6e326-6127-43c2-912f-8abbf855a754" />


> 7TH QUESTION -> ANS: `TXT`

<img width="1279" height="197" alt="image" src="https://github.com/user-attachments/assets/d7606584-0ca8-4e12-9fbc-b87fe80a707b" />


> 8TH QUESTION -> ANS: `Skipping directory: %s (access denied)`

<img width="1279" height="197" alt="image" src="https://github.com/user-attachments/assets/15f6cb6f-3397-4eaa-8c10-6597cd5a3537" />


> 9TH QUESTION -> ANS: `crypto_aes_NewCipher`

<img width="1281" height="196" alt="image" src="https://github.com/user-attachments/assets/24c339f8-da86-4345-824c-73eff5f1eed9" />


> 10TH QUESTION -> ANS: `6368616e676520746869732070617373`

<img width="1278" height="196" alt="image" src="https://github.com/user-attachments/assets/f6d40ea4-ff10-4f7f-8448-45ab3ab8da98" />


> 11TH QUESTION -> ANS: `AI Coding Chatbot`

<img width="1280" height="196" alt="image" src="https://github.com/user-attachments/assets/261e879f-bd54-4c7a-a3ce-04a4fcb7f518" />


## REFERENCES:

```
```
