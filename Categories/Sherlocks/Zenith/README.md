# Zenith
> Write-up author: jon-brandy

<img width="386" height="157" alt="image" src="https://github.com/user-attachments/assets/66817db9-68c5-40f5-978f-c5a997e25051" />


## Lessons Learned:
1. Business e-mail compromise.
2. Parse PDF objects using `peepdf`.
3. Parse event logs using `Hayabusa` and `EvtxeCmd`.
4. Using `Timeline Explorer` to review parsed event logs.
5. Static binary analysis using `pestudio`, `ghidra`, and manual detonation using `Flare-VM`.

## SCENARIO:
<p align="justify">We are contacting you with an urgent request concerning a potentially suspicious email that was recently received and unfortunately opened by one of our team members. As a construction company (Caymine builders), we regularly engage in project discussions with clients, and this email appeared to contain a project plan in PDF format. However, after further review, we have reason to believe this email and its attachment could be malicious. Despite our usual security protocols, the PDF was opened on one of our systems, which has raised significant concern regarding the security of our network.</p>

## STEPS:
1. In this case, we were tasked with investigating a phishing incident involving an email that contained a malicious PDF. Unfortunately, the PDF was opened, and the client is concerned about the security of their network.

> Artifacts given

<img width="1130" height="656" alt="image" src="https://github.com/user-attachments/assets/d9c4b8e7-1be5-48d9-9877-ebe224c9efd3" />

> 1ST QUESTION -> ANS: `2024-09-19 17:44:11`

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/79a50e11-370b-4033-92bc-ec4f7ea4ef8b" />

2. To identify the timestamp of the e-mail retrieval, we can review the available e-mail artifacts and analyze the message headers.

<img width="844" height="266" alt="image" src="https://github.com/user-attachments/assets/2e6345bf-34c3-4cdb-8990-581feaaa536a" />

> In VSCODE

<img width="2328" height="1097" alt="image" src="https://github.com/user-attachments/assets/161f8893-597b-426d-acf9-462b4407c528" />

3. The e-mail headers clearly show the message components and include the timestamp indicating when the Postfix MTA on `mail.caymine.htb` accepted and delivered the e-mail to the recipient’s mailbox (`felamos@caymine.htb`) at `Thu, 19 Sep 2024 17:44:11 UTC`.
4. Also, scrolling down below we can see the attached PDF file.

<img width="832" height="1000" alt="image" src="https://github.com/user-attachments/assets/d993dbc6-1faa-475c-94ac-62bdcdd1e4dd" />

5. To review the file, we can just decode the base64 using cyberchef then save it as PDF file.

<img width="1002" height="1189" alt="image" src="https://github.com/user-attachments/assets/089539fe-fcdb-4010-bd23-d6ef8cdd5fd6" />


> 2ND QUESTION -> ANS: `2024-09-18 13:57:04`

<img width="1280" height="198" alt="image" src="https://github.com/user-attachments/assets/2faca0be-2c8f-4be1-a7c7-98a3729303e6" />

6. To identify the file creation timestamp, we used **exiftool** in Linux to examine the PDF metadata. During the review, we observed that the Producer field was set to pyFPDF. The use of a non-standard PDF generation tool is noteworthy and raises a potential concern.

<img width="937" height="506" alt="image" src="https://github.com/user-attachments/assets/3eca2467-9599-4f0e-870b-39ee54abea6c" />


> 3RD QUESTION -> ANS: `downtown_construction_project_plan.pdf`

<img width="1275" height="196" alt="image" src="https://github.com/user-attachments/assets/1d4a3384-61ca-436d-a685-6b132970734f" />

7. Next, to identify what is the embedded file name, we can start by parse the PDF's Objects using `peepdf`.

<img width="740" height="986" alt="image" src="https://github.com/user-attachments/assets/9afbfe57-c4a7-475f-8a80-184bf1c087c9" />

8. We identified several suspicious elements during the analysis. Starting with objects 11 and 12, we found a reference to object 13, which appears to contain the file extension of the displayed filename. Upon reviewing object 13, we can clearly conclude that the filename and its extension are `downtown_construction_project_plan.pdf`.

<img width="894" height="361" alt="image" src="https://github.com/user-attachments/assets/d03a1666-853b-4c2d-8ddf-95fde083f825" />

#### NOTE:

```console
In a PDF, an indirect object reference has this format:
<object number> <generation number> R
```

9. Reviewing object 14 revealed the content of the embedded file. However, the declared MIME type is inconsistent with the actual file data. Analysis of the raw bytes indicates that the embedded content is a PE binary.

<img width="3278" height="961" alt="image" src="https://github.com/user-attachments/assets/332a89c0-8459-48c9-9715-b0d112057d7a" />

10. To make sure of it, after extract the pdf using **binwalk** and performs a basic file check, it confirms LINUX identified the file nto as PDF but as 32 bit PE binary.

<img width="879" height="218" alt="image" src="https://github.com/user-attachments/assets/1ce418c5-a866-4bdf-a028-6eb708519c3d" />


> 4TH QUESTION -> ANS: `2024-09-18 21:19:18`

<img width="1282" height="196" alt="image" src="https://github.com/user-attachments/assets/7355cb64-0b3d-4d9c-8486-801efd42c871" />

11. The compilation timestamp for the PE binary, can be easily identified again by simply running **exiftool** to check the binary's metadata.

<img width="885" height="687" alt="image" src="https://github.com/user-attachments/assets/df36e1d4-af36-484d-b9c2-2c85471456f0" />


> 5TH QUESTION -> ANS: `exit`

<img width="1280" height="199" alt="image" src="https://github.com/user-attachments/assets/e4281f82-c4f2-4a02-9f1f-d8a4c58bd107" />

12. Since the question asks for the original project name, this can be verified by examining the debug information embedded in the binary. A static analysis in Ghidra can be performed with the objective of locating the Program Database (PDB) file path, which often reveals the original project name assigned by the developer.

<img width="1324" height="850" alt="image" src="https://github.com/user-attachments/assets/6c0556d0-e906-4f49-9129-1161f63779ff" />

> Or you may use PESTUDIO

<img width="941" height="575" alt="image" src="https://github.com/user-attachments/assets/0d5c41ad-61ec-49d6-9330-135cecf15651" />


> 6TH QUESTION -> ANS: `C:\Users\Public\test.exe`

<img width="1282" height="200" alt="image" src="https://github.com/user-attachments/assets/0fa4daf4-4896-47fc-b2f8-fec035c3e668" />


13. To identify this, I began by detonating the malware in a controlled sandboxed environment (FLARE-VM) and examined the Users subdirectories. During this review, I found a newly created binary named `test.exe` inside the Public directory.

<img width="653" height="254" alt="image" src="https://github.com/user-attachments/assets/9875683b-5f80-4fe3-95d4-377c5d628813" />

14. Since the malware copies itself, we can verify its legitimacy by checking the file hash, a straightforward method. The analysis confirmed that the newly created file is identical to the original binary.

<img width="831" height="238" alt="image" src="https://github.com/user-attachments/assets/7b055244-4743-46b6-8ecb-a7610b298428" />


> 7TH QUESTION -> ANS: `WindowsPooler`

<img width="1283" height="198" alt="image" src="https://github.com/user-attachments/assets/f75af8bd-3a83-4df1-9540-bf7c0529e5d0" />


15. Since the detonation was performed manually, we can also review the `SOFTWARE` or `NTUSER.dat` registry hive to identify anomalous registry key values under the `Run` key. However, because the binary is stored in the Public directory, the focus should be on reviewing `HKEY_CURRENT_USER` (NTUSER.dat).

<img width="963" height="695" alt="image" src="https://github.com/user-attachments/assets/a7f40453-b066-4ce9-b53e-45659d3925dd" />


#### NOTE:
To identify persistence mechanism as **Run** or **RunOnce** manually, you may check from these:
- **HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run** (SOFTWARE)
- **HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce** (SOFTWARE)
- **HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run** (NTUSER.dat)
- **HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce** (NTUSER.dat)


16. Interestingly, a new Windows service named WindowsPooler was found installed on the system, and it references the malicious binary.
17. Actually all of these findings can be confirmed by reviewing the code at function `FUN_140001070`

<img width="1513" height="730" alt="image" src="https://github.com/user-attachments/assets/9476aea9-2722-4b44-a0d6-a2b2e9163f01" />


> 8TH QUESTION -> ANS: `explorer.exe`

<img width="1280" height="200" alt="image" src="https://github.com/user-attachments/assets/ae4c3b09-b24c-4362-9cf2-002da21aef71" />

18. To verify this, I continued the code review at function `FUN_140001070` and identified several Windows API calls and code snippets consistent with process injection behavior. Specifically, the code performs process enumeration and targeting, opens the target process, allocates memory within the remote process, writes the payload into the allocated memory, and finally executes the injected code.

<img width="774" height="892" alt="image" src="https://github.com/user-attachments/assets/becd2638-a6b9-4c90-9c07-4380e2032f03" />

19. Now, it is confirmed that **explorer.exe** indeed the targeted process for payload injection by the malware.

> 9TH QUESTION -> ANS: `Windows7`

<img width="1281" height="202" alt="image" src="https://github.com/user-attachments/assets/7e91a7bd-4236-476a-a6da-330b10165b9f" />

20. To identify the client’s OS version, we reviewed the `System` event logs. These logs were first parsed using `EvtxECmd` (by Eric Zimmerman) and then examined with `Timeline Explorer`.

> COMMAND

```
.\EvtxECmd.exe -f "path_to_file.evtx" --csv . --csvf filename_xxx.csv
```

<img width="1391" height="442" alt="image" src="https://github.com/user-attachments/assets/fd8e5e6f-3561-4e3b-8354-4b476cf5f257" />

21. Afterwards, in `Timeline Explorer`, we can check for Event ID `2004` or search for the keyword "Build" to identify the OS build information.

<img width="2682" height="622" alt="image" src="https://github.com/user-attachments/assets/10444848-fa0e-4ee9-a7e6-633a7b82c425" />

22. Review the Event ID `2004` details, it shows us information related to the client OS.

<img width="1030" height="185" alt="image" src="https://github.com/user-attachments/assets/a48c52bf-8e9e-43d7-9059-5bea2521fcf6" />


> 10TH QUESTION -> ANS: `Adobe Reader 9`

<img width="1279" height="196" alt="image" src="https://github.com/user-attachments/assets/1c6b31b2-6094-4b28-afe9-4ed52806e9e2" />

23. To identify the adobe program used, we should review the `Application` event log file and check for Event ID `11707` for completed installation operation.

<img width="1565" height="325" alt="image" src="https://github.com/user-attachments/assets/c5e29612-860a-4dd8-897e-74dd1d23f285" />


> 11TH QUESTION -> ANS: `2024-09-19 17:48:31`

<img width="1275" height="197" alt="image" src="https://github.com/user-attachments/assets/74c1dbb5-0fca-4b5a-b4cb-0ac4692ef9c8" />

24. Activity related to service installation can be identified in `system` event log. However, to give us better scope or horizon related to suspicious activity, we may also triage all event logs using evtx analyzer tool -> Hayabusa.

> Command using Hayabus

```
hayabusa-3.3.0-win-x64.exe csv-timeline -d dir_to_evtx -o htb-zenith-hayabusa.csv -p super-verbose
```

<img width="1816" height="578" alt="image" src="https://github.com/user-attachments/assets/8ae0ee71-be7d-4368-9bfd-f599ac3c743c" />

25. Notice, that `Hayabusa` flagged a high alert named "Meterpreter or Cobalt Strike Getsystem Service Installation - System". This should be related to our interest.

<img width="2934" height="501" alt="image" src="https://github.com/user-attachments/assets/df21276b-622b-4125-b260-285305d15c3b" />

26. On felamos-PC (the client host), the threat actor performed privilege escalation by creating a service named **ismzjo** that executes command prompt as SYSTEM. Don't forget to conver the timestamp to UTC+0.

> 12TH QUESTION -> ANS: `2024-09-19 17:50:17`

<img width="1283" height="198" alt="image" src="https://github.com/user-attachments/assets/aa2915e5-eaea-44b0-8d77-68741f8afb29" />

27. At `System` windows event log, we can clearly identify the timestamp of WindowsPooler service exection for persistence. Check for event ID **7045** and triage specific for new installation service WindowsPooler.

<img width="1922" height="105" alt="image" src="https://github.com/user-attachments/assets/763e978f-1b9f-482c-a956-d7a09cc42396" />

<img width="904" height="190" alt="image" src="https://github.com/user-attachments/assets/f8b617ee-d80e-4ba7-92f1-dc176dab3721" />

28. Great! We've investigated the case briefly.

## REFERENCES:

```
https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-process32firstw
https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot
https://github.com/jesparza/peepdf
https://github.com/Yamato-Security/hayabusa
```
