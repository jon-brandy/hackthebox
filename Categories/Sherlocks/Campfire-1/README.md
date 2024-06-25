# Campfire-1
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c42e376-ab7d-4d72-8fb9-6a690165a992)


## Lessons Learned:
1. Using **EventViewer** to analyze DC's security logs.
2. Kerberoasting Attack Analysis.

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
10. Let's review the previous log, to identify at which workstation this activity occured.

> 3RD QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/14c102a9-b21a-46bd-ace4-398a62d95ac0)


> 4TH QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5cdef3c-0f59-4bf7-bb16-cc4945de9920)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c67fe84-19b6-497d-939e-a450b13f2315)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2e9d6138-f941-4ee0-bc86-f1396c46ae81)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8d1ba2d-15fb-47d9-9a4f-fa1320a3bf7d)


## IMPORTANT LINKS

```
https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4769
```
