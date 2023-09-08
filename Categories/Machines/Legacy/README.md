# Legacy
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c3613dba-80e2-4531-8062-67c543733ab8)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.4 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 19:02 PDT
Nmap scan report for 10.10.10.4
Host is up (0.025s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
|_clock-skew: mean: 5d00h27m38s, deviation: 2h07m16s, median: 4d22h57m38s
|_smb2-time: Protocol negotiation failed (SMB2)
|_nbstat: NetBIOS name: LEGACY, NetBIOS user: <unknown>, NetBIOS MAC: 005056b9bf11 (VMware)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2023-09-13T07:00:44+03:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.08 seconds
```

1. Based from the nmap results, the machine runs SMB service. This should be our interest since there's no web application or any service that is interesting other than that.
2. Luckily nmap has a flag which makes us easier to identify the vuln.
3. Simply run --> `nmap -p 139,445 --script smb-vuln* 10.10.10.4 --min-rate 1000`.

> RESULT

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p 139,445 --script smb-vuln* 10.10.10.4 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 19:10 PDT
Nmap scan report for 10.10.10.4
Host is up (0.038s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Host script results:
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|_      https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_smb-vuln-ms10-054: false

Nmap done: 1 IP address (1 host up) scanned in 5.38 seconds
```

4. Turns out there is 2 CVE found.
5. I did a small research and turns out the correct CVE for this challenge is module --> **smb-vuln-ms08-067**.
6. This arg is supported by the server service for this CVE.
7. Since we already have the CVE number, let's use metasploit straight away.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58392440-cafc-41f1-9bc5-5bed0c4afa94)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/12a09306-442e-46e4-a1fe-9afb0c02c58a)


## USER FLAG

```
e69af0e4f443de7e36876fda4ec7644f
```


> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a273338e-a0c2-40fd-9f31-501c64d8b0fd)


## ROOT FLAG

```
993442d258b0e0ec917cae9e695d5713
```
