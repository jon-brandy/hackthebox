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


> 13TH QUESTION --> ANS: ``

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
https://www.acunetix.com/blog/articles/dns-zone-transfers-axfr/
https://github.com/ly4k/PwnKit
https://blog.qualys.com/vulnerabilities-threat-research/2022/01/25/pwnkit-local-privilege-escalation-vulnerability-discovered-in-polkits-pkexec-cve-2021-4034
```
