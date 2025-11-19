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


6. Inside the `main.hide()`, the binary performs a current working directory check using `main_getCurrentPath`. also `off_90D2F0` section stored the path to "C:\\Systemlogs". 

<img width="800" height="529" alt="image" src="https://github.com/user-attachments/assets/c83260f3-716e-4000-8b7a-fefeff794475" />


> 4TH QUESTION --> ANS: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\HealthCheck`

<img width="1099" height="170" alt="image" src="https://github.com/user-attachments/assets/c4cc06bf-78b8-4809-9ecf-1cfcb1db66ff" />


> 5TH QUESTION --> ANS: `malware.invalid.com`

<img width="1099" height="171" alt="image" src="https://github.com/user-attachments/assets/7eaccc6e-5294-49d9-b7d3-eb9136e8a84a" />


> 6TH QUESTION --> ANS: `GetDriveType`

<img width="1097" height="169" alt="image" src="https://github.com/user-attachments/assets/d96bc92d-1aa2-40a0-8bf1-07ddcf17b089" />



> 7TH QUESTION --> ANS: `NewTicker`

<img width="1099" height="170" alt="image" src="https://github.com/user-attachments/assets/897b8960-8f6f-4a47-893d-1bee7ab9fd60" />


> 8TH QUESTION --> ANS: `Base64`

<img width="1098" height="171" alt="image" src="https://github.com/user-attachments/assets/4c2a44f1-f384-4c43-b543-51340d67f178" />


> 9TH QUESTION --> ANS: `name,version`

<img width="1097" height="190" alt="image" src="https://github.com/user-attachments/assets/1d9d4ec1-56a5-4825-ac3f-45008acae3cd" />

## REFERENCES:
```
```
