# Payload
> Write-up author: jon-brandy

<img width="366" height="145" alt="image" src="https://github.com/user-attachments/assets/9bc5a89c-86c0-49cf-adad-b11d71ba6594" />


## Lessons Learned:
1. Using `PEStudio`, `DIE`, `Ghidra`, `CFF Explorer`, `PE Bear`, and `radare2` to conduct static windows binary analysis and triage.
2. Using `x64dbg` to conduct dynamic binary analysis.

## SCENARIO:

<p align="justify">You’ve completed Training Day — congrats, rookie. Now the real game begins. An unmarked binary just landed on your desk. It’s acting shady, tripping a few alarms, but no one's sure what it really is. Malware? Or just a misunderstood piece of code? Your mission: reverse-engineer the program, trace its behavior, and uncover the truth. Every line of code could be a clue—or a trap. Welcome to your first real case.</p>

## STEPS:
1. In this case, we were tasked with investigating a suspicious binary that triggered multiple alarms upon execution. Extracting the malware archive revealed a single file named **func_pointer.exe**.

<img width="1024" height="549" alt="image" src="https://github.com/user-attachments/assets/bfee7d95-622f-4875-a91e-9940e3e0ca70" />

2. When the binary was executed, it only displayed a simple dialog box stating **HTB pwned us** No other immediate modifications were visibly observed. This behavior is interesting, as it suggests that the malware may be designed to execute post-exploitation activities in a stealthy manner.

<img width="179" height="144" alt="image" src="https://github.com/user-attachments/assets/c47b8ac0-ed02-4418-befa-83281fccbf7c" />


> 1ST QUESTION -> ANS: `EDD41B4A819F917F81203424730AAF0C24CC95E40ACFC0F1BD90B11DADF58015`

<img width="1282" height="200" alt="image" src="https://github.com/user-attachments/assets/efa2000a-a035-4616-bbb7-ff7f44ec751f" />

3. Loading the binary into PEstudio allowed us to identify its hash, as well as review the imported and exported functions that could raise suspicion. In addition, analyzing the embedded strings provided further context, which may assist in attribution efforts or serve as a quick triage step to infer the potential objectives of the binary.
4. We also identified that the binary is 64-bit, and two imports, VirtualProtect and VirtualQuery were flagged as malicious. It is important to note, however, that not all imports marked as malicious should be considered inherently suspicious. Many Windows APIs are legitimate but frequently abused by malware, which often leads automated tools or triage utilities to flag them as potentially malicious.

<img width="1129" height="568" alt="image" src="https://github.com/user-attachments/assets/afe1300a-6185-4cda-adf2-3a615d9f4598" />


> 2ND QUESTION -> ANS: MingW

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/5db6c7c9-93e4-40e4-a5cd-d5bd9947e20a" />

4. Upon reviewing the strings in PEstudio, we were able to clearly identify the compiler used for the binary, which is **MinGW**. Numerous compiler-related strings referencing **MinGW** were present throughout the binary.

<img width="1213" height="806" alt="image" src="https://github.com/user-attachments/assets/04c5a580-f102-41ae-b4f3-0617b1c2f434" />


> 3RD QUESTION -> ANS: `2023-04-06 15:21:17`

<img width="1283" height="197" alt="image" src="https://github.com/user-attachments/assets/bf90cb0f-6159-4715-bb77-42702624d34e" />


5. To identify information related to compilation datetime, I used `radare2` with flag `-I` to shows for binary info (including its protections).

<img width="1304" height="863" alt="image" src="https://github.com/user-attachments/assets/e35e9f11-aab0-4aad-8fc0-91922c7912b4" />

6. This binary was compiled as a 64-bit Windows console application. It has stack canaries enabled and NX/DEP protection, which prevent straightforward stack buffer overflows and execution of injected shellcode from data pages. However, **it lacks ASLR support** (no relocations, not PIC), meaning the memory layout is mostly predictable.

> 4TH QUESTION -> ANS: `False`

<img width="1281" height="198" alt="image" src="https://github.com/user-attachments/assets/f8fbf1bc-72b1-41a4-a2c8-eaad1fb15e8c" />

7. Based on our previous findings, the binary was compiled with **ASLR (Address Space Layout Randomization) disabled**.

<img width="583" height="635" alt="image" src="https://github.com/user-attachments/assets/c51d7208-1a01-4fb1-9276-55f16c9fdeba" />


> 5TH QUESTION -> ANS: `0x140000000`

<img width="1279" height="201" alt="image" src="https://github.com/user-attachments/assets/7daf7a0e-b437-4da8-a361-6c1c5a442867" />

8. There are many ways to identify the image base address, you may use decompiler or debugger. However, in this case I will use `Detect-it-Easy (DIE)` which commonly used to identify a file type along with heuristic analysis.
9. At the top right, we can see the image base address of the binary along with its entry point address.

<img width="723" height="527" alt="image" src="https://github.com/user-attachments/assets/feae4977-5444-4447-983f-0c46a22b4812" />

> 6TH QUESTION -> ANS: `0x00001125`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/c80996c0-55a4-4b1b-b8ee-2562feed8cf6" />

10. Another useful tool to highlight is CFF Explorer, which is widely used for binary triage and analysis.
11. Inside parsed header, we can identify the address of the binary's entrypoint.

<img width="803" height="831" alt="image" src="https://github.com/user-attachments/assets/8538ace5-5622-437d-9c53-b81a81353f9e" />

> 7TH QUESTION -> ANS: `8d098d59a01f830a`

<img width="1279" height="198" alt="image" src="https://github.com/user-attachments/assets/b19cacb0-a646-41e9-8885-be4b60b12e4e" />



<img width="1055" height="1065" alt="image" src="https://github.com/user-attachments/assets/8306ea12-4b7b-4763-86b0-1fafebff32ed" />

<img width="2073" height="931" alt="image" src="https://github.com/user-attachments/assets/7457af5e-c047-4468-b07e-84ca4f8f067a" />

<img width="1914" height="1067" alt="image" src="https://github.com/user-attachments/assets/d519bf5b-c386-4e99-8819-0ff233c9b8da" />


> 8TH QUESTION -> ANS: `0x5555555555555555`

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/7467689d-d3c4-46d3-9048-7cd5c7a35c43" />

<img width="992" height="1151" alt="image" src="https://github.com/user-attachments/assets/6abdf47b-475e-4475-9f6f-e619b91fa4e1" />

<img width="1897" height="441" alt="image" src="https://github.com/user-attachments/assets/335147fb-c2bc-466c-a2cc-77f5f94a8f52" />


> 9TH QUESTION -> ANS: `0x5FFC40`

<img width="1279" height="201" alt="image" src="https://github.com/user-attachments/assets/053f7e62-d1c5-4a7a-b538-01ef68213a94" />

<img width="1066" height="948" alt="Pasted image 20250902194404" src="https://github.com/user-attachments/assets/0e3aeaf2-8adf-462e-bf86-7f981d2d84fc" />

> 10TH QUESTION -> ANS: `fc4881e4f0ffffff`

<img width="1280" height="197" alt="image" src="https://github.com/user-attachments/assets/fc1c6c3c-ce4e-46d4-a07f-c33de35e997b" />


> 11TH QUESTION -> ANS: `VirtualAllocEx`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/23d38c47-8834-4e8b-acfa-42911d4d4255" />


## REFERENCES:
```
https://github.com/radareorg/radare2/releases
https://github.com/horsicq/DIE-engine/releases
```
