# Traverxec
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8c34a13-fe79-45bf-9a19-19faf531ca67)


## Lessons Learned:
- Exploiting nostromo 1.9.6.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.10.165 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-01-22 01:12 PST
Nmap scan report for 10.10.10.165
Host is up (0.25s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 aa99a81668cd41ccf96c8401c759095c (RSA)
|   256 93dd1a23eed71f086b58470973a388cc (ECDSA)
|_  256 9dd6621e7afb8f5692e637f110db9bce (ED25519)
80/tcp open  http    nostromo 1.9.6
|_http-server-header: nostromo 1.9.6
|_http-title: TRAVERXEC
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 147.43 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login at port 22.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e4d8bd58-623a-4e35-9953-84ca3b1c28cd)


2. Enumerating endpoint or files using dirsearch shall resulting to no interesting result.
3. Scrolling down the webapp, found a contact form.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/88a3839b-0f72-4c93-a687-2882e93e2b45)


4. After tried to sent message, got result which indicates this form is not our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ec58eabb-8dd8-4f18-b13c-d3dbdedcc857)


5. Based from the nmap result for port 80, we can identified that the web server is **nostromo 1.9.6**.
6. Searching on the internet for CVE related to that service's version, shall resulting to these exploitDB and github POC.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3606a17-a359-4904-8880-d5a5bd18fe05)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f70372bf-82ce-4968-95db-ab1d866ddde1)


> RESULT OF USING THE GITHUB'S POC

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/64248c7e-6edb-4902-af46-86e3da97e91a)


7. Great! Using the github's poc shall helps us grab the user flag.

> GETTING THE USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d597ca89-df1b-4283-9284-d145608c2a92)


8. Sadly we don't have permission to access david's home directory. Checking **nostromo** configuration file might help us.
9. Let's enumerate the service's directory --> `/var/nostromo`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea4554c3-85e3-4d83-91bf-8e2a2638909f)


10. Checking what's inside **nhttpd.conf** shall resulting to another interest again.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f95a7146-2823-419d-abe4-71db2c48994e)


11. So far we identified that we can get the user's password hash by checking **.htpasswd** and we identified **HOMEDIRS** section.

##### NOTES:

```
Based from the above result, the HOMEDIRS section determines that public_www directory might be inside the david's home directory. Even though david's home is not accessible by other user but public_www is accessible.
```


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e33ea64-7f1a-4e31-8b26-2bed01baeabd)


12. Sadly **hashid** failed to identify the hash type.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4161f3b-9f26-46a3-aa43-cf2a33b4194a)


13. Seems we need to go another way around. Let's check what's inside **public_www**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b7754e31-1a45-4d60-af3c-875429b63648)


14. We found a backup ssh file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0b2c596a-075e-43ad-8ec7-8b8f16f44935)


15. Anyway, let's obtain a proper shell from now on so we can exfiltrate the backup file with ease.

> OBTAINING PROPER SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/63165329-fe72-455b-8265-0171420d5a12)


16. Let's exfiltrate the backup file.






## IMPORTANT LINKS

```
https://github.com/aN0mad/CVE-2019-16278-Nostromo_1.9.6-RCE
https://www.exploit-db.com/exploits/47837
```
