# Operation Blackout 2025: Phantom Check
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/fe403e78-3986-488e-8b3d-9013333fbb80)


## Lessons Learned:
1. Using Hayabusa for efficient parsing and triage of Windows event logs.
2. Utilized Timeline Explorer to examine and correlate events within CSV-based timeline data.
3. Using Event Viewer to analyze windows event logs.

## SCENARIO:

<p align="justify">Talion suspects that the threat actor carried out anti-virtualization checks to avoid detection in sandboxed environments. Your task is to analyze the event logs and identify the specific techniques used for virtualization detection. Byte Doctor requires evidence of the registry checks or processes the attacker executed to perform these checks.</p>


## STEPS:
1. In this case, we were tasked with investigating and analyzing Windows event logs to identify the techniques used by the threat actor for virtualization detection, as well as the specific registry keys accessed during the execution of the detection process.
2. Unzipping the evidence we're only given 2 windows event log files:

![image](https://github.com/user-attachments/assets/1769ddce-d418-47fc-90c5-bfcb56269969)

3. Since our objective was highly specific, we accelerated the investigation by using an open-source tool called Hayabusa, developed by the Yamato Security team.

 ![image](https://github.com/user-attachments/assets/a3bf7b87-4cf5-41cc-a238-7a80e5925ef6)


> COMMAND EXECUTED:

```
hayabusa-3.3.0-win-x64.exe csv-timeline -d C:\HTB-SHERLOCKS\ -o results.csv -p super-verbose
```

4. Using the command above, my objective was to parse all event logs located in the HTB-SHERLOCKS directory, which contained the forensic evidence. I utilized the `--csv-timeline` flag to instruct Hayabusa to convert the parsed data into a CSV timeline format, and the `-o` flag to specify the output file name as results.csv.
5. Additionally, I enabled the `--super-verbose` flag to ensure Hayabusa provided detailed output regarding its scanning findings, which helped in identifying relevant artifacts more efficiently. 

![image](https://github.com/user-attachments/assets/c683c4b8-b232-4d3b-8aa7-a315de47a935)


6. Hayabusa returned several medium-severity detections, which warranted further analysis to determine their relevance to the threat actor's activity.

![image](https://github.com/user-attachments/assets/1f7eb425-5e68-4717-92a1-d92c95f8d83c)


> 1ST QUESTION --> ANS: `Win32_ComputerSystem`

![image](https://github.com/user-attachments/assets/4b91cf43-bc23-4f50-976c-b0205aa90c7c)


7. To examine the parsed event log files, I used Timeline Expolorer which again another tool developed by Eric Zimmerman.
8. Searching for specific keyword -> `wmi`, returned us 3 records related to WMI. 

#### NOTE: VICTIM HOSTNAME -> DESKTOP-M3AKJSD

![image](https://github.com/user-attachments/assets/7ad9fd8a-55e9-4196-89f4-34b58ae4662a)


> 2ND QUESTION --> ANS: `SELECT * FROM MSAcpi_ThermalZoneTemperature`

![image](https://github.com/user-attachments/assets/3aea3779-33b0-4e20-b5c2-fa9e4ef95be3)


> 3RD QUESTION --> ANS: `Check-VM`

![image](https://github.com/user-attachments/assets/b2a0c8d7-82d8-45be-ba3b-6e2edc54d851)


> 4TH QUESTION --> ANS: `HKLM:\SYSTEM\ControlSet001\Services`

![image](https://github.com/user-attachments/assets/924bdd14-0dc6-4088-bd11-1a77552ad347)

> 5TH QUESTION --> ANS: `vboxservice.exe, vboxtray.exe`

![image](https://github.com/user-attachments/assets/41612f92-abf9-40a5-ad9a-fd1117fcb0a5)


> 6TH QUESTION --> ANS: `Hyper-V, Vmware`

![image](https://github.com/user-attachments/assets/e5505f9c-9cb4-46e6-9f53-6dbc65bfca95)


## IMPORTANT LINKS:

```
https://github.com/Yamato-Security/hayabusa
```
