# Campfire-1
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c42e376-ab7d-4d72-8fb9-6a690165a992)


## Lessons Learned:
1. Using **EventViewer** to analyze DC's security logs.
2. Kerberoasting Attack Analysis.
3. Using PECmd.exe to convert prefetch file to csv format.
4. Using Timeline Explorer to review the csv formatted prefetch file.
5. Identifying common kerberoasting tools.

## SCENARIO:
<p align="justify">Alonzo Spotted Weird files on his computer and informed the newly assembled SOC Team. Assessing the situation it is believed a Kerberoasting attack may have occurred in the network. It is your job to confirm the findings by analyzing the provided evidence. You are provided with: 1- Security Logs from the Domain Controller 2- PowerShell-Operational Logs from the affected workstation 3- Prefetch Files from the affected workstation</p>

## STEPS:
1. In this case, we're tasked to investigate a kerberoasting attack on Alonzo's computer. It is known that he spotted few weird files on hits computer.
2. Later on, SOC team is informed and asked to assess the situation.
3. SOC team found the situation is a result of kerberoasting attack in the network and we're asked to confirm their findings by analyzing the provided evidence.
4. We're provided with security logs from Domain Controller, Powershell-Operational Logs, and Prefetch files from the affected workstation.



> 1ST QUESTION --> ANS: `2024-05-21 03:18:09`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/56e304d5-e71a-4426-99fc-24238f2d20da)


5. The easiest way to identify the initial kerberoasting attempt, we need to filter for EventID **4769 (A Kerberos service ticket was requested)**.
6. Next, check for the service name that is not **krbtgt** or ends with **$** sign (it indicates a workstation).
7. Also note that the ticket type should be 0x17 along with the failure code must be 0x0.
8. Upon reviewing every logs, found one log which met our requirements.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bfa58c24-0e76-4deb-abd1-45d621515b59)


> 2ND QUESTION --> ANS: MSSQLService

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ea80688-a40a-4ebf-915f-153769ef6ba6)


9. Based from the log, seems **MSSQLService** is the targeted service name.
10. Upon reviewing the previous log, we can identify that the workstation used for this kerberoasting attack is **FORELA-WKSTN001**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b86d7f9-457f-4680-b413-5614b48eea07)


> 3RD QUESTION --> ANS: `172.17.79.129`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/14c102a9-b21a-46bd-ace4-398a62d95ac0)


11. The IP address of the workstation is also shown at the initial kerberoasting attempt and it's previous log.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df4d9acd-c589-427b-8fc8-417f2d7c4976)


> 4TH QUESTION --> ANS: powerview.ps1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5cdef3c-0f59-4bf7-bb16-cc4945de9920)


12. Moving on to the powershell event logs. We can identify which powershell script used by the threat actor to enumerate AD objects and hunt for kerberoastable accounts in the network.
13. Upon further review to the script and searching for variables naming related to AD and it's logic. We can confirm that it is indeed the used script.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4588cca4-33a8-4b6f-bf6e-c0fedecd93d9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d5669947-b188-4383-84a7-97e7d35f248b)


> 5TH QUESTION --> ANS: `2024-05-21 03:16:32`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c67fe84-19b6-497d-939e-a450b13f2315)


14. Based from our previous identification, the initial execution of the script is at `2024-05-21 03:16:32`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8cfaf4b4-1a38-424d-ad65-69a58266380d)


> 6TH QUESTION --> ANS: `C:\Users\Alonzo.spire\Downloads\Rubeus.exe`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2e9d6138-f941-4ee0-bc86-f1396c46ae81)


15. After identified which account is kerberoastable, the threat actor continue it's attack scheme by executing a specific tool for kerberoasting.
16. Upon reviewing the prefetch file given, a tool named `RUBEUS` caught my attention.
17. Things to note, **RUBEUS**, **IMPACKET**, **GetUserSPN.py**, and **POWERSPLOIT (Invoke-Kerberoast)** are common tools used for kerberoasting.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/af9afc3a-980f-49ec-a939-b99bd81fc239)


18. Now let's convert the prefetch file to a csv file then review it using **Timeline Explorer** to gain more info about the tool properties.

> USING PECmd.exe to convert .pf file to csv.

```
.\PECmd.exe -f 'pathfile.pf' --csv . --csvf result.csv
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f8084f27-c5a3-48d9-8d4d-4cd3efb72e22)


> RESULT IN TIMELINE EXPLORER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34bad86b-6c7c-4b35-9fd3-801e73639a33)


19. To identify it's path, simply check the `Files Loaded` column.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb984d0e-e3e5-4e98-8996-202cc2afeaba)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2e2af728-8fad-4b3c-9fb8-ad51c72ecb76)

20. Nice! We've identified the full path.

> 7TH QUESTION --> ANS: `2024-05-21 03:18:08`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8d1ba2d-15fb-47d9-9a4f-fa1320a3bf7d)


21. Next to identify the execution timestamp, simply check the `Last Run` column.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/859a7b00-88e6-4e27-bcb1-dd1f780a67c9)


22. Great! We've investigated the case!

## IMPORTANT LINKS

```
https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4769
https://www.cybertriage.com/blog/dfir-breakdown-kerberoasting/
```
