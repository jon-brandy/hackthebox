# Delivery
> Write-up author: jon-brandy | Lesson learned --> 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2b87883c-038e-46bb-82e8-6a38ad52c1a1)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ nmap -p- -sVC 10.10.10.222 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-17 20:53 PST
Nmap scan report for 10.10.10.222
Host is up (0.038s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 9c40fa859b01acac0ebc0c19518aee27 (RSA)
|   256 5a0cc03b9b76552e6ec4f4b95d761709 (ECDSA)
|_  256 b79df7489da2f27630fd42d3353a808c (ED25519)
80/tcp   open  http    nginx 1.14.2
|_http-title: Welcome
|_http-server-header: nginx/1.14.2
8065/tcp open  unknown
| fingerprint-strings: 
|   GenericLines, Help, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Accept-Ranges: bytes
|     Cache-Control: no-cache, max-age=31556926, public
|     Content-Length: 3108
|     Content-Security-Policy: frame-ancestors 'self'; script-src 'self' cdn.rudderlabs.com
|     Content-Type: text/html; charset=utf-8
|     Last-Modified: Sat, 18 Nov 2023 04:43:46 GMT
|     X-Frame-Options: SAMEORIGIN
|     X-Request-Id: aucm3j3smjfhmcq1zw46om9xno
|     X-Version-Id: 5.30.0.5.30.1.57fb31b889bf81d99d8af8176d4bbaaa.false
|     Date: Sat, 18 Nov 2023 04:54:56 GMT
|     <!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=0"><meta name="robots" content="noindex, nofollow"><meta name="referrer" content="no-referrer"><title>Mattermost</title><meta name="mobile-web-app-capable" content="yes"><meta name="application-name" content="Mattermost"><meta name="format-detection" content="telephone=no"><link re
|   HTTPOptions: 
|     HTTP/1.0 405 Method Not Allowed
|     Date: Sat, 18 Nov 2023 04:54:56 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8065-TCP:V=7.93%I=7%D=11/17%Time=655843A0%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20
SF:text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\
SF:x20Request")%r(GetRequest,DF3,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ranges:
SF:\x20bytes\r\nCache-Control:\x20no-cache,\x20max-age=31556926,\x20public
SF:\r\nContent-Length:\x203108\r\nContent-Security-Policy:\x20frame-ancest
SF:ors\x20'self';\x20script-src\x20'self'\x20cdn\.rudderlabs\.com\r\nConte
SF:nt-Type:\x20text/html;\x20charset=utf-8\r\nLast-Modified:\x20Sat,\x2018
SF:\x20Nov\x202023\x2004:43:46\x20GMT\r\nX-Frame-Options:\x20SAMEORIGIN\r\
SF:nX-Request-Id:\x20aucm3j3smjfhmcq1zw46om9xno\r\nX-Version-Id:\x205\.30\
SF:.0\.5\.30\.1\.57fb31b889bf81d99d8af8176d4bbaaa\.false\r\nDate:\x20Sat,\
SF:x2018\x20Nov\x202023\x2004:54:56\x20GMT\r\n\r\n<!doctype\x20html><html\
SF:x20lang=\"en\"><head><meta\x20charset=\"utf-8\"><meta\x20name=\"viewpor
SF:t\"\x20content=\"width=device-width,initial-scale=1,maximum-scale=1,use
SF:r-scalable=0\"><meta\x20name=\"robots\"\x20content=\"noindex,\x20nofoll
SF:ow\"><meta\x20name=\"referrer\"\x20content=\"no-referrer\"><title>Matte
SF:rmost</title><meta\x20name=\"mobile-web-app-capable\"\x20content=\"yes\
SF:"><meta\x20name=\"application-name\"\x20content=\"Mattermost\"><meta\x2
SF:0name=\"format-detection\"\x20content=\"telephone=no\"><link\x20re")%r(
SF:HTTPOptions,5B,"HTTP/1\.0\x20405\x20Method\x20Not\x20Allowed\r\nDate:\x
SF:20Sat,\x2018\x20Nov\x202023\x2004:54:56\x20GMT\r\nContent-Length:\x200\
SF:r\n\r\n")%r(RTSPRequest,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConte
SF:nt-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\
SF:n400\x20Bad\x20Request")%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\
SF:r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20clos
SF:e\r\n\r\n400\x20Bad\x20Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x
SF:20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nCo
SF:nnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(TerminalServerCooki
SF:e,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain
SF:;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request
SF:");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 167.26 seconds
```

1. Based from the nmap results, the machine runs a web application, opens ssh login, and opens unknown service at port 8065.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/86e1c57a-3c1f-404a-944b-093b0affd817)


2. Clicking the **helpdesk** hyperlink shall redirects us to a subdomain which runs a support ticketing powered by osTicket.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/89c005d3-4611-4bf3-ac2f-470cd8f55084)


3. 
