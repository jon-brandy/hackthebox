# Soccer
> Write-up author: jon-brandy
## Lesson learned:
- Directory listing using dirsearch.
- h3k tiny file manager exploitations.
- 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4a519534-98c2-4bda-a815-6a4101ab3229)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.194 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-23 22:52 PST
Nmap scan report for 10.10.11.194
Host is up (0.017s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 ad0d84a3fdcc98a478fef94915dae16d (RSA)
|   256 dfd6a39f68269dfc7c6a0c29e961f00c (ECDSA)
|_  256 5797565def793c2fcbdb35fff17c615c (ED25519)
80/tcp   open  http            nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://soccer.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
9091/tcp open  xmltec-xmlmail?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Help, RPCCheck, SSLSessionReq, drda, informix: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|   GetRequest: 
|     HTTP/1.1 404 Not Found
|     Content-Security-Policy: default-src 'none'
|     X-Content-Type-Options: nosniff
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 139
|     Date: Fri, 24 Nov 2023 06:54:01 GMT
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error</title>
|     </head>
|     <body>
|     <pre>Cannot GET /</pre>
|     </body>
|     </html>
|   HTTPOptions, RTSPRequest: 
|     HTTP/1.1 404 Not Found
|     Content-Security-Policy: default-src 'none'
|     X-Content-Type-Options: nosniff
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 143
|     Date: Fri, 24 Nov 2023 06:54:01 GMT
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error</title>
|     </head>
|     <body>
|     <pre>Cannot OPTIONS /</pre>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port9091-TCP:V=7.93%I=7%D=11/23%Time=65604883%P=x86_64-pc-linux-gnu%r(i
SF:nformix,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\
SF:r\n\r\n")%r(drda,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\
SF:x20close\r\n\r\n")%r(GetRequest,168,"HTTP/1\.1\x20404\x20Not\x20Found\r
SF:\nContent-Security-Policy:\x20default-src\x20'none'\r\nX-Content-Type-O
SF:ptions:\x20nosniff\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nC
SF:ontent-Length:\x20139\r\nDate:\x20Fri,\x2024\x20Nov\x202023\x2006:54:01
SF:\x20GMT\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lan
SF:g=\"en\">\n<head>\n<meta\x20charset=\"utf-8\">\n<title>Error</title>\n<
SF:/head>\n<body>\n<pre>Cannot\x20GET\x20/</pre>\n</body>\n</html>\n")%r(H
SF:TTPOptions,16C,"HTTP/1\.1\x20404\x20Not\x20Found\r\nContent-Security-Po
SF:licy:\x20default-src\x20'none'\r\nX-Content-Type-Options:\x20nosniff\r\
SF:nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x20143
SF:\r\nDate:\x20Fri,\x2024\x20Nov\x202023\x2006:54:01\x20GMT\r\nConnection
SF::\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en\">\n<head>\n<m
SF:eta\x20charset=\"utf-8\">\n<title>Error</title>\n</head>\n<body>\n<pre>
SF:Cannot\x20OPTIONS\x20/</pre>\n</body>\n</html>\n")%r(RTSPRequest,16C,"H
SF:TTP/1\.1\x20404\x20Not\x20Found\r\nContent-Security-Policy:\x20default-
SF:src\x20'none'\r\nX-Content-Type-Options:\x20nosniff\r\nContent-Type:\x2
SF:0text/html;\x20charset=utf-8\r\nContent-Length:\x20143\r\nDate:\x20Fri,
SF:\x2024\x20Nov\x202023\x2006:54:01\x20GMT\r\nConnection:\x20close\r\n\r\
SF:n<!DOCTYPE\x20html>\n<html\x20lang=\"en\">\n<head>\n<meta\x20charset=\"
SF:utf-8\">\n<title>Error</title>\n</head>\n<body>\n<pre>Cannot\x20OPTIONS
SF:\x20/</pre>\n</body>\n</html>\n")%r(RPCCheck,2F,"HTTP/1\.1\x20400\x20Ba
SF:d\x20Request\r\nConnection:\x20close\r\n\r\n")%r(DNSVersionBindReqTCP,2
SF:F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n")
SF:%r(DNSStatusRequestTCP,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnec
SF:tion:\x20close\r\n\r\n")%r(Help,2F,"HTTP/1\.1\x20400\x20Bad\x20Request\
SF:r\nConnection:\x20close\r\n\r\n")%r(SSLSessionReq,2F,"HTTP/1\.1\x20400\
SF:x20Bad\x20Request\r\nConnection:\x20close\r\n\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.20 seconds
```

1. Based from the nmap results, we can identified the machine opens ssh login, running web app at port 80, and xmltec-xmlmail service at port 9091.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d6b3679-ced0-479c-893a-839a9915e757)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c5bb1d3f-f1f9-4a96-9037-f2351c8d1c15)


2. Scrolling down and clicking the navbar item, shall found nothing interesting.
3. Hence the approach is to do directory listing or enumerate subdomain.
4. Running both with ffuf and dirsearch, found interesting directory named `tiny`.

```
dirsearch -u http://soccer.htb -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ffa5631e-e919-40e3-a74c-e16a694313bc)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/046768ed-3b68-403b-92cc-acf470db2ad6)


5. Searching on the internet for `h3k tiny file manager default credentials` shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/29a563fd-fc3a-4699-82e6-b6531ca81021)


6. We successfully logged in after using the admin cred as admin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c058e8f7-94ef-4fdc-baf2-902b1e32e496)


7. Checking all images, seems there's nothing interesting, it goes the same for the .html file.
8. But checking **tiny** directory, found .php files which hardcoded the creds there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4620ca6a-419c-4569-a0f5-590f884e3429)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7febed41-fd73-4cf4-baf5-c2c6aabefaff)


9. After checked the **Uploads** directory's permission, found out as admin we are allowed to RWX.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f35d23ed-b9dd-4354-a860-b24c3487f2fc)


10. Interesting, we can try to upload **php reverse shell** then.
11. For the php reverse_shell I used --> `https://github.com/pentestmonkey/php-reverse-shell`.
12. Don't forget to change these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/386d5119-4bf4-44ea-88ed-dfc33bc0c7a4)


14. Upload the file inside the **uploads** directory, then access the endpoint of the uploaded file --> `/tiny/uploads/<filename>`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8689f8a9-0f71-41f7-bff8-2fcb498c6a8e)


> RESULT AT LISTENER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8c621c7-7a1d-4fa7-8a78-e76a2779c122)


15. We can't get the user flag obviously because we didn't get shell as user.
16. Took me a while to find a foothold which useful to get shell as user.
17. Enumerating `/var/www/` found nothing interesting. Remembering the web server is running using **nginx**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea589c54-3e6e-482c-840e-43e4f0e8fe98)


18. Hence I started to enumerate the **nginx** settings and luckily found a foothold.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e665b9d7-5d59-4eb2-a435-3e2ff78454c0)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/885a0d27-ff52-404b-ab29-794a8cab262b)


> soc-player.soccer.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/64b84cfa-9a74-4dad-96de-5928b43d5520)


19. Interesting we found the similiar views but there are 3 other navbar item.
20. But this time default credential for admin is invalid.
21. After I tried to create an account with both username and password is admin, found this result.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4116ef83-2321-4f9a-b1d3-6bfb50b38128)


22. Also there is another endpoint which is **/check**, this is getting more interesting and this could tell that the interest should be about port 9091 (another open port found at our nmap scan before).
23. 
