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


7. To examine the parsed event log files, I used Timeline Explorer, another powerful tool developed by Eric Zimmerman.
8. By searching for the keyword "wmi", I identified three records related to Windows Management Instrumentation (WMI) activity, which provided valuable insight into the threat actor's behavior.

#### NOTE: VICTIM HOSTNAME -> DESKTOP-M3AKJSD

![image](https://github.com/user-attachments/assets/7ad9fd8a-55e9-4196-89f4-34b58ae4662a)

9. The first and second record clearly indicated that the threat actor utilized the **Win32_ComputerSystem** class to query the system’s model and manufacturer information, its commonly used for virtualization detection.

![image](https://github.com/user-attachments/assets/dedc0613-bc78-4d29-896f-41ccbaa8f7cd)


> 2ND QUESTION --> ANS: `SELECT * FROM MSAcpi_ThermalZoneTemperature`

![image](https://github.com/user-attachments/assets/3aea3779-33b0-4e20-b5c2-fa9e4ef95be3)


10. Following that, we observed the threat actor executing an SQL query to retrieve temperature data from the machine. This was done by dumping all entries from the MSAcpi_ThermalZoneTemperature class.
11. Very interesting!

![image](https://github.com/user-attachments/assets/29c1fb70-d510-4f5c-86c2-e3610c144cec)


> SQL QUERY:

```
SELECT * FROM MSAcpi_ThermalZoneTemperature
```

> 3RD QUESTION --> ANS: `Check-VM`

![image](https://github.com/user-attachments/assets/b2a0c8d7-82d8-45be-ba3b-6e2edc54d851)


12. Moving on, by examining activity near the timeline at `2025-04-09 16:20:11`, found a powershell script execution and a function named `Check-VM` is likely forged.

![image](https://github.com/user-attachments/assets/7479c178-b111-4da3-9bba-2a74d2aeed27)

![image](https://github.com/user-attachments/assets/9afbf512-e63b-4fb3-8f9e-31f53bef346b)

13. After tried to paste and did a quick check for it, indeed its very clear the **Check-VM** is a forged function to perform virtualization detection.

![image](https://github.com/user-attachments/assets/ddfcbd7b-2807-4651-9c87-4f697b064845)


> 4TH QUESTION --> ANS: `HKLM:\SYSTEM\ControlSet001\Services`

![image](https://github.com/user-attachments/assets/924bdd14-0dc6-4088-bd11-1a77552ad347)


14. Upon reviewing it, we identified a series of registry key queries occurring around the time of the virtualization check.
15. Notably, the threat actor specifically accessed the Services registry key, which is a common technique used to enumerate installed drivers and services—often leveraged for virtualization and sandbox detection.

![image](https://github.com/user-attachments/assets/85ef935e-4879-4de0-9b81-bc866e022c35)



> 5TH QUESTION --> ANS: `vboxservice.exe, vboxtray.exe`

![image](https://github.com/user-attachments/assets/41612f92-abf9-40a5-ad9a-fd1117fcb0a5)


16. Based on our previous findings, we can confidently conclude that the script is also capable of detecting VirtualBox environments.
17. To achieve this, the script performs a comparison check for the presence of two specific processes: vboxservice.exe and vboxtray.exe, both commonly associated with VirtualBox installations.


> 6TH QUESTION --> ANS: `Hyper-V, Vmware`

![image](https://github.com/user-attachments/assets/e5505f9c-9cb4-46e6-9f53-6dbc65bfca95)


18. To identify the output generated during execution, we examined the corresponding event logs using Event Viewer.
19. We observed a consistent pattern in the output messages. Each began with the phrase "This is a".
20. This pattern allowed us to efficiently locate the relevant detection events by simply searching for that specific string, which led us directly to the successful execution logs.

![image](https://github.com/user-attachments/assets/625a4249-1310-4ef1-8d5b-22b957745574)


21. Nice! We can tell the script detect two virtualizations platforms.
22. Those are Hyper-V and VMware.
23. Great! We've investigated a quick case and specific request!

## IMPORTANT LINKS:

```
https://github.com/Yamato-Security/hayabusa
```
