# SalineBreeze-2
> Write-up author: jon-brandy

<img width="460" height="166" alt="image" src="https://github.com/user-attachments/assets/94dc13b0-5e69-4506-b708-f633138b92d6" />


## Lessons Learned:
1. Demodex TTPs (associated with Demodex, Salt Typhoon / Earth Estries & Ghost Emperor)
2. PowerShell deobfuscation and reverse engineering
3. Dynamic malware analysis using FLARE-VM and Procmon
4. Static malware analysis using PEStudio and Ghidra

## SCENARIO:
<p align="justify">Your boss was so impressed with your research skills that you've been "rewarded" with a new task: malware analysis. Your mission is to investigate a piece of malware linked to the infamous cyber espionage group, Salt Typhoon. They've been targeting critical infrastructure, and it's up to you to uncover their tactics and techniques.</p>

## STEPS:
1. In this case, we are tasked with performing a malware analysis on a .ps1 file that is suspected to be linked to an infamous cyber-espionage group known as Salt Typhoon.
2. Upon a quick review of the provided PowerShell script, we can clearly identify encrypted strings and an AES-based decrypt-and-execute loader logic.

> ONEDRIVED.PS1

<img width="1076" height="707" alt="image" src="https://github.com/user-attachments/assets/74f24f95-80b8-4024-aaa9-4a3136724299" />


> 1ST QUESTION --> ANS: `Demodex`

<img width="1414" height="216" alt="image" src="https://github.com/user-attachments/assets/51072693-dabd-493d-bbe7-90fdf570d03a" />


3. While reviewing online articles about Salt Typhoon, one article curated by [Trend Micro](https://www.trendmicro.com/en_us/research/24/k/earth-estries.html) describes a DEMODEX rootkit infection chain that used the same PowerShell script name as the one we have now.

<img width="1480" height="776" alt="image" src="https://github.com/user-attachments/assets/c1c970bc-dfc4-4089-9ae1-4c24e8701095" />


4. The article also states that, based on Trend Micro telemetry, they identified specific commands used by the threat actor to make the script functional.
5. Let's just tried that on our sandbox.

<img width="927" height="348" alt="image" src="https://github.com/user-attachments/assets/7847d7be-1b60-4ff7-a9f4-b8597d33a499" />


> 2ND QUESTION --> ANS: `System.Security.Cryptography.AesManaged`

<img width="1413" height="214" alt="image" src="https://github.com/user-attachments/assets/7f5ab020-64fe-4141-9ad7-bc8fc202989e" />


> 3RD QUESTION --> ANS: `$k`

<img width="1413" height="213" alt="image" src="https://github.com/user-attachments/assets/f681489d-69b6-4c31-ae28-e563b8193fc9" />


> 4TH QUESTION --> ANS: `password@123`

<img width="1413" height="219" alt="image" src="https://github.com/user-attachments/assets/22fa89d4-95a7-4408-81d1-eeeeebd1ead0" />


> 5TH QUESTION --> ANS: `midihelp`

<img width="1416" height="215" alt="image" src="https://github.com/user-attachments/assets/43aa3efb-ae9d-438a-a608-d99d5cc357a7" />


> 6TH QUESTION --> ANS: `3b1c251b0b37b57b755d4545a7dbbe4c29c15baeca4fc2841f82bc80ea877b66`

<img width="1414" height="215" alt="image" src="https://github.com/user-attachments/assets/e5a51a57-a916-46e6-aa8b-6ad54e5b53a6" />


> 7TH QUESTION --> ANS: `MsMp4Hw`

<img width="1415" height="214" alt="image" src="https://github.com/user-attachments/assets/b9111235-9749-49b8-94b7-fb64e91a842e" />


> 8TH QUESTION --> ANS: `C:\Windows\System32\msmp4dec.dll`

<img width="1415" height="218" alt="image" src="https://github.com/user-attachments/assets/37adc5e6-62d9-48d1-8b1c-496c98a7a1f0" />


> 9TH QUESTION --> ANS: `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SvcHost`

<img width="1416" height="214" alt="image" src="https://github.com/user-attachments/assets/7fd53a92-f782-4b65-9a0d-2329530ac7cc" />


> 10TH QUESTION --> ANS: `Start-Service -name $svcname;`

<img width="1414" height="217" alt="image" src="https://github.com/user-attachments/assets/553c9d92-013a-411d-afea-fb7909d284a7" />


> 11TH QUESTION --> ANS: `GetComputerNameA`

<img width="1415" height="215" alt="image" src="https://github.com/user-attachments/assets/697d9ac8-2044-4b91-89c6-0b663728353e" />


> 12TH QUESTION --> ANS: `ServiceMain`

<img width="1416" height="216" alt="image" src="https://github.com/user-attachments/assets/bc5a3d16-bfd9-4b35-82f8-3e3a1ff4d098" />


> 13TH QUESTION --> ANS: `10000`

<img width="1415" height="242" alt="image" src="https://github.com/user-attachments/assets/c2d2f5ce-23bd-4839-aa27-6076143ad90a" />

 
## REFERENCE:

```
https://www.trendmicro.com/en_us/research/24/k/earth-estries.html
```
