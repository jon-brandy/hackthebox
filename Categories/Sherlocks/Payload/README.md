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
11. Inside parsed header section, we can identify the address of the binary's entrypoint.

<img width="803" height="831" alt="image" src="https://github.com/user-attachments/assets/8538ace5-5622-437d-9c53-b81a81353f9e" />

> 7TH QUESTION -> ANS: `8d098d59a01f830a`

<img width="1279" height="198" alt="image" src="https://github.com/user-attachments/assets/b19cacb0-a646-41e9-8885-be4b60b12e4e" />

12. To speed up the triage, I began by searching for code that attempts to obtain a handle to a DLL and store the address of its functions. This is so could quick reveals the intent of the binary.
13. This search led to the identification of the function `FUN_140001d97`.

<img width="1669" height="897" alt="image" src="https://github.com/user-attachments/assets/7a5c7022-2c4e-4f1c-9d50-c40c18067ec3" />

14. Long story short, after reviewing each nested functions, identified `FUN_1400017d0` as the function of primary interest.

<img width="1622" height="288" alt="image" src="https://github.com/user-attachments/assets/4cce5022-044e-458a-b647-c883272d140b" />

15. Inside, it performs a simple bitwise operations actually. It's just a textbook XOR-based encryption / decryption.

<img width="759" height="908" alt="image" src="https://github.com/user-attachments/assets/1378b5b2-5c1a-481d-8638-17fdccb2c0a9" />

16. However, the analysis revealed suspicious behavior when `param3` was identified as a string buffer. Upon inspecting its contents, we observed the presence of encrypted strings. This indicates that, prior to obtaining the handle of a DLL and resolving its functions, the binary performs a payload decryption routine.

<img width="821" height="392" alt="image" src="https://github.com/user-attachments/assets/98e6d6c9-1c8f-4750-a07e-38fa5aed39de" />

> PAYLOAD LOCATION

<img width="778" height="144" alt="image" src="https://github.com/user-attachments/assets/a3a66306-52cd-4367-9c9e-a18ba91b9112" />

> PAYLOAD CONTENT

<img width="830" height="785" alt="image" src="https://github.com/user-attachments/assets/fe818b72-8924-4979-8e3c-5e4ada82b7d3" />

17. At this stage, we were able to clearly identify the first 8 bytes of the payload. In addition, another useful tool for static binary analysis is `PE-Bear`, which provides greater visibility into the encrypted payload structure and its characteristics.

> PAYLOAD IS STORED AT .DATA SECTION (Global Initialized Variable)

<img width="2089" height="1224" alt="image" src="https://github.com/user-attachments/assets/6f801202-d001-404c-9a8f-0f0dcd0722bc" />

> 8TH QUESTION -> ANS: `0x5555555555555555`

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/7467689d-d3c4-46d3-9048-7cd5c7a35c43" />

18. Reviewing the previously identified decrypt function for the payloads. Notice `param1` is treated as a pointer to a buffer of bytes, `param2` iiis used as a modulus, means the function keeps wrappoing around inside that buffer.
19. It means `param1` is a key material buffer, which is indexed repeatedly to generate the keystream `local_1d` that XORs against `param3`.

<img width="763" height="898" alt="image" src="https://github.com/user-attachments/assets/2115c734-2de7-473a-aebc-7388963aa512" />

> KEY BUFFER LOCATION

<img width="1818" height="235" alt="image" src="https://github.com/user-attachments/assets/b457c547-05bf-4601-bdb5-81a18f0e4f91" />

> KEY BUFFER CONTENT

<img width="813" height="210" alt="image" src="https://github.com/user-attachments/assets/632ad58a-f2e5-48ea-a370-e8a8e5a3c7ec" />


20. Great! Now we also identified the key buffer used (in hex).

> 9TH QUESTION -> ANS: `0x5FFC40`

<img width="1279" height="201" alt="image" src="https://github.com/user-attachments/assets/053f7e62-d1c5-4a7a-b538-01ef68213a94" />

21. To identify the address of the decrypted payload, we should debug the binary. To debug it I used `x64Dbg`.
22. At first, load the binary there and press `run to user code` so we jumped to the binary's entrypoint.

<img width="3128" height="1210" alt="image" src="https://github.com/user-attachments/assets/9307cbc3-8222-452a-9e35-3ba1098ae730" />


23. Next, right-click and follow the steps below. Since our objective is to begin debugging at the payload decoding phase, we should first locate the key buffer offset and set breakpoints there. Additional breakpoints can also be placed throughout the debugging process, as this may help us identify more accurate offsets for analysis.

<img width="1774" height="905" alt="image" src="https://github.com/user-attachments/assets/9ee7992c-1466-4962-a679-48c84e9b5745" />

> RESULT AFTER JUMPED TO KEY BUFFER

<img width="1346" height="715" alt="image" src="https://github.com/user-attachments/assets/9372c3e9-85c7-4a0d-996a-38a42c6abdf3" />

24. After set breakpoint(s), just click the run button to jump there (it act like continue in GDB).

<img width="1435" height="439" alt="image" src="https://github.com/user-attachments/assets/3b25cdb6-9ae8-4862-8fba-7ea7cabc7e73" />

25. To identify the content, we can follow the dump by right click and follow these steps:

<img width="1189" height="737" alt="image" src="https://github.com/user-attachments/assets/40fe5390-251b-4eb1-91b8-3478159d65d2" />

26. The full debugging steps are not shown here, as they would be too lengthy. The main objective is to identify where the decrypted value is stored.
27. Once this location is identified, another breakpoint can be set to track that section or register, and the dump can then be followed again in xDbg.
28. I recommend always comparing the logic with the assembly view in Ghidra, as this provides better context for identifying which instructions should be prioritized during debugging.

<img width="1882" height="723" alt="image" src="https://github.com/user-attachments/assets/860af134-2207-4cce-bb0b-541a933aff0a" />

29. In short, we identified the actual offset where the decrypted payload is stored. Based on our findings, the encrypted payload resides in the .DATA section. Therefore, the debugging focus should be narrowed to mov instructions that interact with the data segment (ds).

<img width="1373" height="604" alt="image" src="https://github.com/user-attachments/assets/d71685e8-ab9e-470a-bdf3-09c76dc61d2c" />

30. To examine the content value and its address, it is best to begin the review at the cmp instruction. For this purpose, we set a breakpoint at offset `0x1400019A4` and then followed the dumps starting at offset `0x14000199B`. Now we can see that the address of the decrypted payload is stored at `0x5FFC40`, as `ds:[RDX]` is used to hold each decrypted payload buffer index and, in turn, points to this address.

<img width="1503" height="1135" alt="image" src="https://github.com/user-attachments/assets/bbc25bc5-138d-4f8b-a05c-11069d2940f3" />

31. At this stage, we can skip the previous breakpoint and set a new one at `0x1400019B4`, then follow the dumps at `0x1400019AF`. From there, by examining offset `0xFFC40` and the subsequent addresses, we can identify the entirety of the decrypted payload.

<img width="843" height="899" alt="image" src="https://github.com/user-attachments/assets/f55bc4c4-574d-4ad5-a2a6-fe7c7a7cdbb7" />


> 10TH QUESTION -> ANS: `fc4881e4f0ffffff`

<img width="1280" height="197" alt="image" src="https://github.com/user-attachments/assets/fc1c6c3c-ce4e-46d4-a07f-c33de35e997b" />


32. Based on our previous findings, we can clearly identify in the dump that the first 8 bytes of the payload reside at `0x5FFC38 + 0x8`, spanning up to offset `0x5FFC48`.

<img width="623" height="477" alt="image" src="https://github.com/user-attachments/assets/8cec8585-47e7-435d-8d81-9807ebf0f6ee" />


> 11TH QUESTION -> ANS: `VirtualAllocEx`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/23d38c47-8834-4e8b-acfa-42911d4d4255" />


## REFERENCES:
```
https://github.com/radareorg/radare2/releases
https://github.com/horsicq/DIE-engine/releases
```
