# Wifinetic
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1cb403c0-cbd0-4266-a643-3428e88ad253)


## Lessons Learned:
- Anonymous FTP login.
- 

## STEPS:
> PORT SCANNING

```
┌──(vreshco㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.247 --min-rate 1000
Starting Nmap 7.92 ( https://nmap.org ) at 2024-04-05 00:51 PDT
Nmap scan report for 10.10.11.247
Host is up (0.021s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE    VERSION
21/tcp open  ftp        vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.11
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          4434 Jul 31  2023 MigrateOpenWrt.txt
| -rw-r--r--    1 ftp      ftp       2501210 Jul 31  2023 ProjectGreatMigration.pdf
| -rw-r--r--    1 ftp      ftp         60857 Jul 31  2023 ProjectOpenWRT.pdf
| -rw-r--r--    1 ftp      ftp         40960 Sep 11  2023 backup-OpenWrt-2023-07-26.tar
|_-rw-r--r--    1 ftp      ftp         52946 Jul 31  2023 employees_wellness.pdf
22/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
53/tcp open  tcpwrapped
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.06 seconds
```

1. Based from the nmap result, the machine opens 3 ports --> 21, 22, 53.
2. Noticed we can do anonymous login at the ftp service.

> ANONYMOUS FTP LOGIN

```
Execute this command --> ftp wifinetic.htb, then send "anonymous" as the username input.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34b001b6-daac-4d8b-bba1-bba7d9397e34)


3. 
