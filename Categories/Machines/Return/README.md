# Return
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bb7929a7-5a9e-434c-a534-346742066b3d)


## Lessons Learned:
- Enumerating SMB Services using **smbclient** and **enum4linux**.
- Abusing network printer.
- Using evil-winrm to login as svc-printer.
- Enumerating group memberships for user svc-printer.
- Checking user's privilege.
- Abusing Active Directory (AD) security groups.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ nmap -p- -sV -sC 10.10.11.108 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-23 08:15 PST
Stats: 0:00:47 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 61.24% done; ETC: 08:16 (0:00:30 remaining)
Nmap scan report for 10.10.11.108
Host is up (0.018s latency).
Not shown: 65501 closed tcp ports (conn-refused)
PORT      STATE    SERVICE       VERSION
53/tcp    open     domain        Simple DNS Plus
80/tcp    open     http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: HTB Printer Admin Panel
88/tcp    open     kerberos-sec  Microsoft Windows Kerberos (server time: 2023-12-23 16:35:21Z)
135/tcp   open     msrpc         Microsoft Windows RPC
139/tcp   open     netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open     ldap          Microsoft Windows Active Directory LDAP (Domain: return.local0., Site: Default-First-Site-Name)
445/tcp   open     microsoft-ds?
464/tcp   open     kpasswd5?
593/tcp   open     ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open     tcpwrapped
3268/tcp  open     ldap          Microsoft Windows Active Directory LDAP (Domain: return.local0., Site: Default-First-Site-Name)
3269/tcp  open     tcpwrapped
5985/tcp  open     http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open     mc-nmf        .NET Message Framing
16515/tcp filtered unknown
28911/tcp filtered unknown
30028/tcp filtered unknown
33923/tcp filtered unknown
40939/tcp filtered unknown
47001/tcp open     http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47020/tcp filtered unknown
49664/tcp open     msrpc         Microsoft Windows RPC
49665/tcp open     msrpc         Microsoft Windows RPC
49666/tcp open     msrpc         Microsoft Windows RPC
49667/tcp open     msrpc         Microsoft Windows RPC
49671/tcp open     msrpc         Microsoft Windows RPC
49676/tcp open     ncacn_http    Microsoft Windows RPC over HTTP 1.0
49677/tcp open     msrpc         Microsoft Windows RPC
49678/tcp open     msrpc         Microsoft Windows RPC
49681/tcp open     msrpc         Microsoft Windows RPC
49728/tcp open     msrpc         Microsoft Windows RPC
50859/tcp filtered unknown
50956/tcp filtered unknown
58849/tcp filtered unknown
Service Info: Host: PRINTER; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 18m33s
| smb2-time: 
|   date: 2023-12-23T16:36:20
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 143.45 seconds
```

1. Based from the nmap results, the machine runs a web application hosted with Microsoft IIS httpd 10.0 web server and open public SMB.
2. Noticed port **5985** (WinRM or Windows Remote Management) also opened, this should allows us to use **evil-winrm**.

> WEB APP - Welp, we are in the admin panel.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/11a8acbe-87b9-4fb4-b7df-964d5321ac79)


2. Few ports also opened and noticed the machine uses LDAP service.
3. To enumerate public smb shares, you can use either **smbclient** or **enum4linux**.
4. Anyway, enumerating it using **smbclient** found no workgroup.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31f869dc-37b9-4c5b-b256-7b80359c0b44)


5. It goes the same with **enum4linux** but it provides another information, which states that the host is part of the **RETURN** domain.

> Usage in enum4linux

```
enum4linux -a return.htb
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/219c992c-aa57-4661-ad0e-9dabeeda62e3)


6. With this result, we can identified that `SMB does not allow guest sessions or NULL`.
7. Moving on our attention to the web app and navigating to the **settings** option. Found out we can see the username but the password is hidden.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59978b87-b3f7-4664-b00d-be913f213a3e)


8. However, this page disclose an information that **svc-printer** cred can be seen by watching the request at port 389 (runs LDAP services).
9. We can leak the password by setting a listener to that port and change the server address to our public ip. ANOTHER way to make it clear in case we can't see the leaked password clear, we can run **wireshark** when clicking the submit button.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0755bbe1-d1f6-4a11-9588-6165ec4e0505)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fc99ae94-b8fc-4421-88fa-c8fa8891e42c)


> RESULT IN WIRESHARK

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbae58ec-3662-4944-8344-ea1aa15d2a1b)


10. Nice! Let's use **evil-winrm**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/12e1c654-b1f0-4384-b14c-ad6689167798)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4e6cdcec-7b3f-4496-82b6-41a3e429715f)


## USER FLAG

```
5216ac3a0475fe671c786c662e88194e
```

11. To gain root, I start by enumerating the group memberships.

```
net user svc-printer
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/af3da7c4-b906-401c-bb42-77beea08612b)


12. Next, I check the user's priviege.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a12db1dd-60b9-41b7-9350-1c8d2c2cbd83)


13. Not a fond in windows pentesting, so I digging more about **Active Directory Security Groups** and found this website.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/88c5aeef-e140-47f8-a506-58850fa8ce95)


14. Long story short, **Server Operators Group** is our interest here. The most important here is, it can start and stop service. 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4abaa734-a7ba-43cf-9809-93b9feed786d)


15. There is a binary in windows which used for communicating with the Service Control Manager (SCM) and services. It's called SC.
16. Not only that, remembering the user has **SeBackupPrivilege** and **SeRestorePrivilege**, it makes 

## IMPORTANT LINKS

```
https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups#bkmk-serveroperators
```
