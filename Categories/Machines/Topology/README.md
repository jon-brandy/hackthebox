# Topology
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1614206e-d7d4-428b-b223-97aa9b0ae5a0)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.217 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-01 06:44 PDT
Nmap scan report for toplogy.htb (10.10.11.217)
Host is up (0.028s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 dcbc3286e8e8457810bc2b5dbf0f55c6 (RSA)
|   256 d9f339692c6c27f1a92d506ca79f1c33 (ECDSA)
|_  256 4ca65075d0934f9c4a1b890a7a2708d7 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Miskatonic University | Topology Group
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.15 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7ad08a3f-dc9b-47ed-9587-c3dfaec73705)


2. After ran **dirsearch** found nothing interesting.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2f24b03b-d2eb-43da-ae26-7937ec8d9bff)


3. Checking the webpage, found an interesting link.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ff66afa-3e4e-4d87-ad1d-b2f2dc6f37eb)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c43c371-ace2-49c7-ba62-391ed423a32f)


4. Interesting, I think we all have the same thought here of what the vuln might be.
5. It could be **command injection** or **SSTI**.
6. Anyway, after searching on the internet about `latex injection` found this --> `https://book.hacktricks.xyz/pentesting-web/formula-doc-latex-injection`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/62712b93-030e-4552-b826-d00b98c008f6)


7. Let's try to read a file using these template payloads.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/53dc4ab9-197a-4ad7-941d-e5158916f536)

> Input --> $\lstinputlisting{/etc/passwd}$

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2c782fdc-4af0-4542-b193-97da0ee4ff39)


8. It creates a .png file and shows what's inside passwd. Great! This is our foothold, noticed we found 2 users --> root and vdaisley.
9. Anyway, I think the intended way is to get a reverse shell using command injection payload for LaTeX. But since it allows us to do arbitrary files read.
10. Hence, I tried to traverse all common dir and files location, but somehow can't access them.
11. Stuck in this for a while, until I check for subdomains and found this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5fcdef3c-39cd-4774-ba85-a4ba1b671a03)


12. Found a subdomain --> `dev`.

> dev.topology.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f0ea81b3-f30d-4d0b-8023-a6a51000d744)


13. Interesting! Let's run dirsearch again for this subdomain.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/375d4fec-b8f9-48db-8a07-9054c2c371f2)


14. As you can see, I think it will shows the same result as the **topology.htb** domain.
15. But the unique thing is, there is no such ".htpasswd" inside it but indeed there seems ".htpasswds".
16. Even accessing ".htpasswds" shall gave me error message. Trying access ".htpasswd" shows us cred for **vdaisley** user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/857a61e2-ade6-44fc-8ef8-abf6b8594a4d)


17. Awesome, let's crack it with john.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b136ae3a-6698-423a-a9b8-ec99594f9ea7)


18. Let's login to ssh as **vdaisley:calculus20**.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d7c7b382-dfd9-4222-ada4-183a27621582)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b933157-3c71-4c52-856d-e7f73dfff36e)


## USER FLAG

```
fa74b70a848ed9002b4ba1ded4dba244
```

19. When tried to check sudo permission for **vdaisley**, sadly he/she does not run sudo on this machine.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/98152475-44b8-48ec-84b3-6ae7c5cdb414)


20. Noticed there's a **pspy64**, we won't need to grab linpeas or another pspy64 version from our local machine, let's just make it executeable then run it.
21. This two should be interesting.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae81472d-dbe0-489d-ac2e-a64d3184e520)


22. **gnuplot** is being run as root.
23. Scrolling down the pspy64 result shall find files inside gnuplot is executed again.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b410f74b-92cf-483d-8ae5-11ec90d5ae8c)


24. It's part of the cronjob! Great!
25. 
