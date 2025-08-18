# Payload
> Write-up author: jon-brandy

<img width="366" height="145" alt="image" src="https://github.com/user-attachments/assets/9bc5a89c-86c0-49cf-adad-b11d71ba6594" />


## Lessons Learned:
1. Malware Analysis
2. Using `PEStudio`, `DIE`, `Ghidra`, `CFF Explorer`, `PE Bear`, and `radare2` to conduct static windows binary analysis.
3. Using `x64dbg` and `capa` to conduct dynamic binary analysis.

## SCENARIO:

<p align="justify">You’ve completed Training Day — congrats, rookie. Now the real game begins. An unmarked binary just landed on your desk. It’s acting shady, tripping a few alarms, but no one's sure what it really is. Malware? Or just a misunderstood piece of code? Your mission: reverse-engineer the program, trace its behavior, and uncover the truth. Every line of code could be a clue—or a trap. Welcome to your first real case.</p>

## STEPS:
1. asda

<img width="514" height="294" alt="image" src="https://github.com/user-attachments/assets/21be1a37-0609-45a1-baf8-187d42cb3900" />


> 1ST QUESTION -> ANS: `EDD41B4A819F917F81203424730AAF0C24CC95E40ACFC0F1BD90B11DADF58015`

<img width="1282" height="200" alt="image" src="https://github.com/user-attachments/assets/efa2000a-a035-4616-bbb7-ff7f44ec751f" />

<img width="1472" height="166" alt="image" src="https://github.com/user-attachments/assets/17a1b2bf-ed0d-404d-8d19-f116e002d1e5" />


> 2ND QUESTION -> ANS: MingW

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/5db6c7c9-93e4-40e4-a5cd-d5bd9947e20a" />

<img width="1804" height="1303" alt="image" src="https://github.com/user-attachments/assets/4595e90e-1b3d-43a0-8721-41e02b46cd29" />


> 3RD QUESTION -> ANS: `2023-04-06 15:21:17`

<img width="1283" height="197" alt="image" src="https://github.com/user-attachments/assets/bf90cb0f-6159-4715-bb77-42702624d34e" />

<img width="806" height="658" alt="image" src="https://github.com/user-attachments/assets/a292f283-9e81-4b17-8d9b-ad7808ebd910" />


> 4TH QUESTION -> ANS: `False`

<img width="1281" height="198" alt="image" src="https://github.com/user-attachments/assets/f8fbf1bc-72b1-41a4-a2c8-eaad1fb15e8c" />

<img width="583" height="635" alt="image" src="https://github.com/user-attachments/assets/c51d7208-1a01-4fb1-9276-55f16c9fdeba" />


> 5TH QUESTION -> ANS: `0x140000000`

<img width="1279" height="201" alt="image" src="https://github.com/user-attachments/assets/7daf7a0e-b437-4da8-a361-6c1c5a442867" />

<img width="843" height="642" alt="image" src="https://github.com/user-attachments/assets/cf231646-db83-4ee5-8546-4bde01280105" />


> 6TH QUESTION -> ANS: `0x00001125`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/c80996c0-55a4-4b1b-b8ee-2562feed8cf6" />


> 7TH QUESTION -> ANS: `8d098d59a01f830a`

<img width="1279" height="198" alt="image" src="https://github.com/user-attachments/assets/b19cacb0-a646-41e9-8885-be4b60b12e4e" />

<img width="1055" height="1065" alt="image" src="https://github.com/user-attachments/assets/8306ea12-4b7b-4763-86b0-1fafebff32ed" />

<img width="2073" height="931" alt="image" src="https://github.com/user-attachments/assets/7457af5e-c047-4468-b07e-84ca4f8f067a" />

<img width="1914" height="1067" alt="image" src="https://github.com/user-attachments/assets/d519bf5b-c386-4e99-8819-0ff233c9b8da" />


> 8TH QUESTION -> ANS:

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/7467689d-d3c4-46d3-9048-7cd5c7a35c43" />


> 9TH QUESTION -> ANS:

<img width="1279" height="201" alt="image" src="https://github.com/user-attachments/assets/053f7e62-d1c5-4a7a-b538-01ef68213a94" />


> 10TH QUESTION -> ANS:

<img width="1280" height="197" alt="image" src="https://github.com/user-attachments/assets/fc1c6c3c-ce4e-46d4-a07f-c33de35e997b" />


> 11TH QUESTION -> ANS: `VirtualAllocEx`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/23d38c47-8834-4e8b-acfa-42911d4d4255" />


## REFERENCES:
```
https://github.com/radareorg/radare2/releases
https://github.com/horsicq/DIE-engine/releases
```
