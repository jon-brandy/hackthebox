# APTNightmare

> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/73392552-cbb7-450d-947d-f045e0be264e)


## Lessons Learned:
1. Analyzed packet capture file using `wireshark`.
2. Reviewing nmap activities and identified open ports. (using small `wireshark` foo).
3. Identifying DNS Zone Transfer Activity and compromised subdomain along with credentials used by the threat actor.
4. Using `volatility` to analyze memory dump from a web server (using ubuntu profile).
5. Using `wireshark` and `volatility` to identify command used by the attacker to gain initial access to the web server and what binary is used for privilege escalation.
6. Correlated the technique used with MITRE framework.
7. Using `regripper` to parse common registry hives.
8. Identifying and review program execution artifacts.
9. Using `LECmd.exe` to analyze **.lnk** files.
10. Using `Registry Explorer` to review registry hives, identify dirty log, and create clean hive from transaction logs.
11. Using `FTK Imager` to review acquisitioned disk.
12. Conducted small e-mail forensic for phishing mail.
13. Using `EvtxEcmd.exe` to parse windows powershell and powershell operational event logs to csv.
14. Using `Timeline Explorer` to review csv file.
15. Using `cyberchef` to decode encoded powershell command (formula used --> from base64 and gunzip). Afterwards using formula (from base64 and xor 35 decimal with null preserving).
16. Identifying threat label using virus total.
17. Analyzing cobalt strike beacon using `1768.py` script.
18. Identifying new tasks created by the threat actor (persistence artifacts).
   
## SCENARIO:

<p align="justify">We neglected to prioritize the robust security of our network and servers, and as a result, both our organization and our customers have fallen victim to a cyber attack. The origin and methods of this breach remain unknown. Numerous suspicious emails have been detected. In our pursuit of resolution, As an expert forensics investigator, you must be able to help us.</p>

## STEPS:
1. In this case, we are tasked with investigating a cybersecurity breach, the origin and methods of which are still unknown. However, it is known that numerous suspicious emails have been detected.In this case, we are tasked with investigating a cybersecurity breach, the origin and methods of which are still unknown. However, it is known that numerous suspicious emails have been detected.
2. As a forensic investigator we are given 4 files which we need to analyze. There are 2 acquisitioned data (disk and RAM), a captured network file, and an ubuntu profile. 

![image](https://github.com/user-attachments/assets/f62c048e-d09c-4a9b-9d8a-831c62632bc6)


3. Based from the file naming, we can indicate the infected device is the CEO's and the captured RAM is from the web server.

> 1ST QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/b9b4dc1d-29c7-4ca7-9f54-403e7cca76ce)


> 2ND QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/e47b56d0-f619-42c4-bab1-977d75b13d12)


> 3RD QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/d1af8af5-47ee-47a4-a4ea-951a69d446c3)


> 4TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/97cf7841-c653-4443-9024-8c0e7e333969)


> 5TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/f3184f83-beba-41ac-b0a5-361520d9114c)


> 6TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/7ea00737-7d18-4ef0-97ff-74c3e97c2b4f)


> 7TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/72b71a83-cf42-4cc9-b82c-c038753ea294)


> 8TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/8ccab98f-94b0-49ef-84a6-9f478c1db49f)


> 9TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/a36ebc73-d9da-49f7-9045-a3d4aa352df6)


> 10TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/d7178191-3ed0-454c-b735-8dcd1969fcc6)


> 11TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/c1cfa667-dbea-46a1-bfb7-a75a8284d5f4)


> 12TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/f42f9999-8f00-4894-a4d3-1648b6e51612)


> 13TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/8b7fe429-49b7-4edc-8eac-600c7e855a0d)


> 14TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/f8bb72f2-a79d-41f4-9f25-53a027dd8a21)


> 15TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/01cc74a3-9c67-46a4-bb5d-e951f055057f)


> 16TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/96e7114c-f2a0-4f85-bbeb-7b3df5826fb4)


> 17TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/4748107b-0a8e-4faf-9a50-a0188a15d1d1)


> 18TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/35922d0f-1aa8-4964-a917-2b5d6921fed8)


> 19TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/07ba599e-943b-4ebf-b682-ac31cf0f0623)


> 20TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/76c9edc4-6c82-41fe-9af1-1ad69081318a)


> 21ST QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/22e67f89-e4fa-48e2-9511-96c105bc6efc)


> 22ND QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/a09f7537-4060-4c40-8680-8c4071229499)


> 23RD QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/b360d8f3-01a6-433e-a51b-df1380e705bb)


## IMPORTANT LINKS:

```

```
