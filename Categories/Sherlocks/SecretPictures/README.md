# Secret Pictures
> Write-up author: jon-brandy

<img width="395" height="144" alt="image" src="https://github.com/user-attachments/assets/94daab7e-5b5d-4b5a-8ec6-b639c02e4e7a" />


## Lessons Learned:
1. Static Analysis using tools such as `IDA`, `PE Studio`, and `Detect It Easy (DiE)` to examine the PE file’s structure, metadata, and potential indicators of malicious behavior.
2. Dynamic Analysis using `Wireshark` to monitor network activity and observe the malware’s behavior during execution.

## SCENARIO:
<p align="justify">The university's IT team began receiving reports of strange activity on library computers. Students noticed hidden files appearing on their USB drives and disappearing moments later. An investigation revealed a single suspicious file named "SecretPictures." When opened, it vanished instantly without leaving a trace, and no antivirus tool could identify it. The IT team isolated the file and provided it for your analysis. As a cybersecurity analyst, your task is to determine what this malware does, how it spreads, and how to stop it before it affects more systems.</p>

## STEPS:
1. In this case, we were tasked with analyzing a PE file suspected of causing unusual activity on library computers, with no logs or operating system artifacts provided by the university’s IT team.

<img width="536" height="588" alt="image" src="https://github.com/user-attachments/assets/e9d876af-3259-461d-9652-946c457b6801" />


> 1ST QUESTION --> ANS: `FD46D178474F32F596641FF0F7BB337E`

<img width="1099" height="171" alt="image" src="https://github.com/user-attachments/assets/2f58fcfc-4df3-483e-9087-e3528e6485d9" />


2. To get the MD5 checksum, in powershell I ran this command:

```ps1
Get-Filehash .\secretPictures.exe -Algorithm MD5
```

<img width="833" height="102" alt="image" src="https://github.com/user-attachments/assets/78bd1c74-619e-4745-9a30-a3c0d75caf63" />


> 2ND QUESTION --> ANS: `GOLANG`

<img width="1098" height="170" alt="image" src="https://github.com/user-attachments/assets/24c7dc5d-88ac-4db1-a3dc-5805ed0b8c5d" />


3. A quick PE file analysis using PE Studio, DiE, or even a simple strings inspection is sufficient to determine the programming language used in the malware, compiled used,  identify any packers, and gain a broader understanding of potentially malicious import functions.

> RESULT FROM DIE

<img width="729" height="295" alt="image" src="https://github.com/user-attachments/assets/d286b809-c5f5-4145-abe9-75c992ea89ef" />


> 3RD QUESTION --> ANS: `Systemlogs`

<img width="1101" height="170" alt="image" src="https://github.com/user-attachments/assets/1df6ee08-62b4-4165-ab3f-c3b85d2472d4" />

4. To identify the name of the folder that the malware hides in by copying itself, we need to perform code review to the PE binary. In this writeup, I a using IDA.

<img width="1913" height="1011" alt="image" src="https://github.com/user-attachments/assets/b183cdb2-cdef-4751-80b1-36c32763ee52" />

5. Reviewing the `main.main()` function, found 4 functions that could be our interest.

<img width="664" height="590" alt="image" src="https://github.com/user-attachments/assets/279166fe-228e-482c-9c32-254a424ac72d" />


6. Inside the `main.hide()`, the binary performs a current working directory check using `main_getCurrentPath()`. 

<img width="800" height="529" alt="image" src="https://github.com/user-attachments/assets/c83260f3-716e-4000-8b7a-fefeff794475" />


7. Another functions that should be our interest are `main_lurk()` and `main_vanish()`, also `off_90D2F0` section, which stored the path to "C:\\Systemlogs".

<img width="1002" height="206" alt="image" src="https://github.com/user-attachments/assets/7f7fbc52-e7bd-44c7-b714-fb4592db1107" />

> OFF_90D2F0 section

<img width="1055" height="395" alt="image" src="https://github.com/user-attachments/assets/ed081e18-9ea0-495d-ba9a-861c928f5208" />

8. Afterwards, it called `runtime_concatstring2()` to copy the binary to `Systemlogs` directory.

<img width="921" height="474" alt="image" src="https://github.com/user-attachments/assets/13681c21-b51f-4043-a235-bdbbb888fcce" />

9. From reviewing the pseudocode, we can infer that a Systemlogs directory will be created, and the malware will copy itself there once its current location is identified by the program and before the execution flow is finished.
10. However, it is best to verify this behavior by debugging the binary.

> BEFORE

<img width="1706" height="786" alt="image" src="https://github.com/user-attachments/assets/68b1dcf7-17cd-47de-86c0-689238933b7b" />


> AFTER

<img width="1770" height="850" alt="image" src="https://github.com/user-attachments/assets/6a1efc86-6489-4b14-be79-a14322484ae4" />


11. As shown above, after `main_lurk()` completes, the program proceeds to `main_vanish()`. At this point, the Systemlogs directory has not yet been created, because the copying operation actually occurs inside the `main_vanish()` function.

<img width="1225" height="789" alt="image" src="https://github.com/user-attachments/assets/2df20334-064d-475e-afcb-19da284900b7" />

> SYSTEMLOGS DIRECTORY AND INSIDE IT

<img width="851" height="474" alt="image" src="https://github.com/user-attachments/assets/8273a036-699c-4acb-8f32-c19d8aee7e13" />

<img width="1025" height="189" alt="image" src="https://github.com/user-attachments/assets/01082fed-748e-4f9e-ad22-45df21c2a70c" />


12. Noticed that the copied filename is changed to `logcheck.exe` and the original binary is removed.

<img width="425" height="139" alt="image" src="https://github.com/user-attachments/assets/18823df9-bf2e-44d2-9e1b-99f67fbec065" />


> 4TH QUESTION --> ANS: `malware.invalid.com`

<img width="1099" height="170" alt="image" src="https://github.com/user-attachments/assets/c4cc06bf-78b8-4809-9ecf-1cfcb1db66ff" />

13. To identify its FQDN, I created a sandbox environment with fake network capability. For this purpose, I used REMnux configured with INetSim.
14. On my Windows machine (FLARE-VM), I captured the network traffic using Wireshark and executed the malware again to observe and extract its FQDN.

<img width="1314" height="527" alt="image" src="https://github.com/user-attachments/assets/2e7470da-3c6a-4115-ba41-0fddd4647c57" />


15. As seen above, flare performed an outbound connection to `malware.invalid[.]com`.


> 5TH QUESTION --> ANS: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\HealthCheck`

<img width="1099" height="171" alt="image" src="https://github.com/user-attachments/assets/7eaccc6e-5294-49d9-b7d3-eb9136e8a84a" />

16. Upon reviewing the main_lurk() function, it becomes evident that the binary attempts to open a registry key under the Run location and create a new value inside it. This behavior indicates a persistence mechanism, typically used to ensure execution after reboot. Although the sample also uses scheduled task–related functionality elsewhere, the logic here directly targets Run key–based persistence.

<img width="1576" height="941" alt="image" src="https://github.com/user-attachments/assets/573fe80b-46f3-4e74-9cd1-19a2278fa8e2" />

17. The registry root handle is not stored in cleartext. Instead, the malware passes a decimal constant to the golang_org_x_sys_windows_registry_OpenKey function. To identify which predefined HKEY it corresponds to, this decimal value must be translated to hexadecimal.
18. This conversion can be validated using [any](https://www.rapidtables.com/convert/number/decimal-to-hex.html?x=-2147483647) standard decimal-to-hex utility.

```
v43 = golang_org_x_sys_windows_registry_OpenKey(
        -2147483647,
        (unsigned int)"Software\\Microsoft\\Windows\\CurrentVersion\\RUN",
        45,
        3,
        a5,
        a6,
        a7,
        a8,
        a9);
```

<img width="593" height="680" alt="image" src="https://github.com/user-attachments/assets/2b9157bb-cb42-4bbe-8297-e071c8faed82" />


18. After obtaining the hex form, we correlate the value with documented Windows predefined registry handles, such as those listed in the Windows SDK (winreg.h) or in public [mirrors](https://doxygen.reactos.org/d0/d77/winreg_8h.html).

<img width="694" height="163" alt="image" src="https://github.com/user-attachments/assets/2c2584e8-82d0-4117-9155-0472ac808c42" />

19. Great! Based on this mapping, we can conclusively determine that the malware attempts to open and write to:

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

20. This confirms that the malware establishes persistence by placing an entry under the HKCU Run key, ensuring the malicious program executes automatically for the current user during system startup.

> 6TH QUESTION --> ANS: `GetDriveType`

<img width="1097" height="169" alt="image" src="https://github.com/user-attachments/assets/d96bc92d-1aa2-40a0-8bf1-07ddcf17b089" />



> 7TH QUESTION --> ANS: `NewTicker`

<img width="1099" height="170" alt="image" src="https://github.com/user-attachments/assets/897b8960-8f6f-4a47-893d-1bee7ab9fd60" />


> 8TH QUESTION --> ANS: `Base64`

<img width="1098" height="171" alt="image" src="https://github.com/user-attachments/assets/4c2a44f1-f384-4c43-b543-51340d67f178" />


<img width="1298" height="309" alt="image" src="https://github.com/user-attachments/assets/e91a9068-582c-4c15-b869-c0c3b0138968" />


> 9TH QUESTION --> ANS: `name,version`

<img width="1097" height="190" alt="image" src="https://github.com/user-attachments/assets/1d9d4ec1-56a5-4825-ac3f-45008acae3cd" />

<img width="1300" height="488" alt="image" src="https://github.com/user-attachments/assets/b8b56ccf-7a0b-4db8-a5fe-650e4076c7c2" />



## REFERENCES:
```
https://learn.microsoft.com/en-us/windows/win32/sysinfo/predefined-keys?
https://doxygen.reactos.org/d0/d77/winreg_8h.html
https://www.rapidtables.com/convert/number/decimal-to-hex.html?x=-2147483647
```
