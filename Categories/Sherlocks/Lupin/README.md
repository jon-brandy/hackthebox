# Lupin
> Write-up author: jon-brandy

<img width="342" height="150" alt="image" src="https://github.com/user-attachments/assets/5ec03859-e0d1-471d-b62a-1bb381515ef6" />

## Lessons Learned:
1. Phorpiex malware family analysis, focusing on behavior and execution flow.
2. Reverse engineering clipboard hijacking techniques, identifying how address replacement logic works.
3. Static analysis using IDA, Ghidra, and Detect It Easy (DiE) for code navigation, function tracing, and basic binary inspection.

## SCENARIO:

<p align="justify">After a security incident, unusual activity on Samira’s workstation led to the discovery of a suspicious binary operating stealthily in the background. The executable evades standard detection while maintaining persistence and network communication. Your mission is to reverse the binary and extract the attacker’s TTPs for the endpoint security team.
</p>

## STEPS:
1. saad

> 1ST QUESTION -> ANS: `6.41450`

<img width="1330" height="239" alt="image" src="https://github.com/user-attachments/assets/f1a213ee-53b5-4e49-8b1a-d720d86a7dc9" />

> 2ND QUESTION -> ANS: `syscrondvr.exe`

<img width="1326" height="238" alt="image" src="https://github.com/user-attachments/assets/9e9ad593-6523-4425-a392-d2b795f7d01a" />

> 3RD QUESTION -> ANS: `GetLocaleInfoA`

<img width="1328" height="241" alt="image" src="https://github.com/user-attachments/assets/75bacf4f-704b-4e2c-bd60-08921be2850b" />


> 4TH QUESTION -> ANS: `DeleteUrlCacheEntry`

<img width="1325" height="270" alt="image" src="https://github.com/user-attachments/assets/3b281fd2-1a70-4fb6-8f68-9004ec67b97e" />


> 5TH QUESTION -> ANS: `0x405B90`

<img width="1327" height="269" alt="image" src="https://github.com/user-attachments/assets/4bf683db-20ab-4bb4-a02f-4d8ab7d56831" />


> 6TH QUESTION -> ANS: `WM_DRAWCLIPBOARD`

<img width="1329" height="240" alt="image" src="https://github.com/user-attachments/assets/614d91c3-5eaf-42c2-a573-9adba7409e23" />


> 7TH QUESTION -> ANS: `0x404A60`

<img width="1325" height="240" alt="image" src="https://github.com/user-attachments/assets/568c855b-693e-4774-95a7-ae5354621ff5" />


> 8TH QUESTION -> ANS: `0xab2d474dad344da1e3b7ece6e7022c3295c52b176978337be82288a59e5a2a40`

<img width="1326" height="239" alt="image" src="https://github.com/user-attachments/assets/2b633240-f4dc-480a-81d8-0c99ad257bfe" />


> 9TH QUESTION -> ANS: `239.255.255.250`

<img width="1327" height="240" alt="image" src="https://github.com/user-attachments/assets/10b6bb6e-df64-4c7c-b5eb-fbf511737d88" />


> 10TH QUESTION -> ANS: `1900`

<img width="1330" height="242" alt="image" src="https://github.com/user-attachments/assets/a6a467d2-5640-4ed4-8c66-f080c612320b" />


> 11TH QUESTION -> ANS: `phorpiex`

<img width="1331" height="244" alt="image" src="https://github.com/user-attachments/assets/2d6d1f00-2885-4357-8652-4cffb943a8ed" />

## REFERENCES:

```
https://etherscan.io/name-lookup-search?id=jamilaaidos.eth
https://ethplorer.io/address/0x75d4a4b37177c92b26d7563fbb7ef4758fe9aa03#
```
