# Timelapse
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6ae9f7ae-3c2d-47b0-96c8-611d44ecf6ce)


## Lesson learned:
- Enumerate public smb share with **smbclient**.
- Cracking Personal Information Exchange (PFX) file.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.152 --min-rate 1000 -Pn 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-29 02:11 PST
Nmap scan report for 10.10.11.152
Host is up (0.019s latency).
Not shown: 65517 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-11-29 18:13:50Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5986/tcp  open  ssl/http      Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_ssl-date: 2023-11-29T18:15:22+00:00; +7h59m58s from scanner time.
| ssl-cert: Subject: commonName=dc01.timelapse.htb
| Not valid before: 2021-10-25T14:05:29
|_Not valid after:  2022-10-25T14:25:29
|_http-title: Not Found
| tls-alpn: 
|_  http/1.1
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49692/tcp open  msrpc         Microsoft Windows RPC
49701/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2023-11-29T18:14:44
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required
|_clock-skew: mean: 7h59m57s, deviation: 0s, median: 7h59m57s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 320.43 seconds
```

1. Based from the nmap results, it opens few ports (which is not good) and it runs web application at port 5986.
2. Noticed there are SMB share opens, let's enumerate it with **smbclient**.

> Using smbclient, for password using your own machine password.

```
smbclient -L //timelapse.htb/
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ smbclient -L //timelapse.htb/
Password for [WORKGROUP\brandy]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        Shares          Disk      
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to timelapse.htb failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

3. Nice there's `ADMIN$` sharename, but the only sharename we can access without credential is `Shares`.

```
smbclient //timelapse.htb/Shares
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/164a12a2-9dc5-429e-8895-73e6c381f3e1)


4. After listing all files inside `Dev` directory, found a .zip file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/90b3257a-76ba-4d73-a210-d624fe8693fd)


5. To download a file from smb share, we use `get` command.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1b81c185-9b93-444c-9a64-d11334e368cb)


6. Interesting! Inside it, there's a .pfx file and it seems we need to use john to crack the password.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/140376c2-ba5f-4a4c-bf42-5e015d8e033b)


> Using john

```
┌──(brandy㉿bread-yolk)-[~/Downloads/machine/machine_timelapse]
└─$ zip2john winrm_backup.zip > hash.txt                                                                                                                           
ver 2.0 efh 5455 efh 7875 winrm_backup.zip/legacyy_dev_auth.pfx PKZIP Encr: TS_chk, cmplen=2405, decmplen=2555, crc=12EC5683 ts=72AA cs=72aa type=8
```

> supremelegacy

```
┌──(brandy㉿bread-yolk)-[~/Downloads/machine/machine_timelapse]
└─$ john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt                
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 6 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
supremelegacy    (winrm_backup.zip/legacyy_dev_auth.pfx)     
1g 0:00:00:00 DONE (2023-11-29 04:11) 4.761g/s 16559Kp/s 16559Kc/s 16559KC/s surkerior..supalove
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```


7. Personal Information Exchange (PFX) also known as PKCS #12 or P12 file is a binary format file that is commonly used to store a private key with its associated public key and certificates.
8. It securely exporting and importing private keys and certificates, especially in scenarios where you need to move or back up a certificate and its associated private key.
9. They are often used in web server configurations, for example, when installing SSL/TLS certificates. The PFX format provides a convenient way to bundle all the necessary components securely into a single file.
10. Great! Now we know what **.pfx** file is, let's extract what inside it and used them with **WinRM** so we can login to the remote server without a password.

> Command to extract pfx file

#### NOTES:

```
For those who wonders why .pem (Privacy Enhanced Mail), because PEM file is a text file that typically contains one or more cryptographic elements,
encoded in the PEM format. The contents of a PEM file are encoded using Base64 encoding and are enclosed between
"-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----" (or a similar marker depending on the type of data).
```

```
openssl pkcs12 -in legacyy_dev_auth.pfx -nocerts -out key.pem -nodes
```

11. It failed when I reused the previous password, hence let's crack it again using john.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/91600221-4507-4378-903e-5cdb6ece009d)


12. Anyway, inside john directory you shall found several python script which convert few file extension to **.john**. Also all of them still rely on python2.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7d10ac0-3f38-483b-bca9-cd623f7fab9b)






## IMPORTANT LINKS

```

```




