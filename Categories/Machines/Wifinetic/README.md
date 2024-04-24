# Wifinetic
> Write-up author: scorch

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/fe6395db-e99e-4b31-863b-30c3131d07cb)


## Lessons Learned:
- FTP Anonymous Login (information disclosure).
- Enumerating Wireless Network Interfaces.
- Identifying which network interface used as Access Point and which one is used as the WIFI Client.
- Dump Detailed each of Wireless Network Configurations (identified misconfig).
- Bruteforce WPS PIN using reaver (gained root access to the actual WIFI).

## STEPS:
> PORT SCANNING

```
┌──(scorch㉿getsleep)-[~/Downloads]
└─$ nmap -p- -sV -sC wifinetic.htb --min-rate 1000
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-04-23 22:41 PDT
Nmap scan report for wifinetic.htb (10.10.11.247)
Host is up (0.029s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE    VERSION
21/tcp open  ftp        vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          4434 Jul 31  2023 MigrateOpenWrt.txt
| -rw-r--r--    1 ftp      ftp       2501210 Jul 31  2023 ProjectGreatMigration.pdf
| -rw-r--r--    1 ftp      ftp         60857 Jul 31  2023 ProjectOpenWRT.pdf
| -rw-r--r--    1 ftp      ftp         40960 Sep 11  2023 backup-OpenWrt-2023-07-26.tar
|_-rw-r--r--    1 ftp      ftp         52946 Jul 31  2023 employees_wellness.pdf
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.8
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
53/tcp open  tcpwrapped
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.50 seconds
```

1. Based from the nmap results, the machine opens FTP service, ssh service, and it's unclear what service is running at port 53. But based on it's port number, most likely it acts as a DNS Server.
2. Noticed we can login using anonymous user in FTP.

> LOGIN USING ANONYMOUS USER

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/ad250528-b56f-4844-af97-7101be0d0870)


3. Found few files there! Let's download eadh files from current FTP directory to our local machine.
4. 
