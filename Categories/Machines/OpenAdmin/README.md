# OpenAdmin
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9908a103-8c8b-4771-bb74-0bf955c31f61)


## Lessons Learned:
- Using dirsearch to enumerate webpages.
- Exploiting OpenNetAdmin (ONA) v.18.1.1 --> Remote Code Execution, Command Injection.

## STEPS:
> PORT SCANNNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC openadmin.htb --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2024-05-05 20:41 PDT
Nmap scan report for openadmin.htb (10.10.10.171)
Host is up (0.019s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4b98df85d17ef03dda48cdbc9200b754 (RSA)
|   256 dceb3dc944d118b122b4cfdebd6c7a54 (ECDSA)
|_  256 dcadca3c11315b6fe6a489347c9be550 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.64 seconds
```

1. Based from the nmap results, the machine runs web application at port 80 and opens ssh login at port 22.
2. Noticed based from the service's detail, once we open the webapp it shall rendered Ubuntu Default Page.

> WEB DEFAULT PAGE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/061c4f0e-2d71-4aa9-a168-99436176d7df)


3. Knowing this condition, seems the approach is to do directory listing.

> RESULT USING DIRSEARCH

```
dirsearch -u http://openadmin.htb:80
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a74ba915-39d9-418d-a4bf-26bde6d2a304)


4. Interesting! We found 2 accessible endpoint.

> Accessing /music/

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1f38ff98-6fa1-425e-8788-53856e547961)


5. Long story short, after reviewing every feature. Figured out that login feature shall redirect us to `/ona` endpoint.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4c9b4311-3f21-42bf-bc44-71ababe5b4a7)


> Accessing /ona/


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f16362b7-372d-40c6-ba05-34704060d1a7)


6. By checking for documentation, turns out ONA is an abbreviation of **OpenNetAdmin**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/45440e69-a7b4-4781-9f26-697aaed46333)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/44663749-8bbf-49eb-b6fd-d9e97afc4f98)


7. Noticed, it disclosed the service's version --> `18.1.1`. Using `searchsploit` or internet to find vuln related to this version, found these results:

> Internet

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ab29c1d-0c5f-4864-8f4d-4347e780176c)

> Searchsploit



8. It's remote code execution, also there's github POC's which can be useful.
9. Anyway, let's use the exploit from exploit.db first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/680d056a-3507-48d7-a5b0-fd42fe46fe17)


```txt

```

