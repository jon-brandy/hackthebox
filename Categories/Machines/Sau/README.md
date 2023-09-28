# Sau
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d8ec6c5-88e8-405a-80d5-9f925668b750)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.224 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-27 21:54 PDT
Stats: 0:01:10 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 50.00% done; ETC: 21:56 (0:00:55 remaining)
Stats: 0:01:15 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 50.00% done; ETC: 21:56 (0:01:00 remaining)
Nmap scan report for sau.htb (10.10.11.224)
Host is up (0.050s latency).
Not shown: 65531 closed tcp ports (conn-refused)
PORT      STATE    SERVICE VERSION
22/tcp    open     ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 aa8867d7133d083a8ace9dc4ddf3e1ed (RSA)
|   256 ec2eb105872a0c7db149876495dc8a21 (ECDSA)
|_  256 b30c47fba2f212ccce0b58820e504336 (ED25519)
80/tcp    filtered http
8338/tcp  filtered unknown
55555/tcp open     unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     X-Content-Type-Options: nosniff
|     Date: Thu, 28 Sep 2023 04:55:23 GMT
|     Content-Length: 75
|     invalid basket name; the name does not match pattern: ^[wd-_\.]{1,250}$
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 302 Found
|     Content-Type: text/html; charset=utf-8
|     Location: /web
|     Date: Thu, 28 Sep 2023 04:54:55 GMT
|     Content-Length: 27
|     href="/web">Found</a>.
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Allow: GET, OPTIONS
|     Date: Thu, 28 Sep 2023 04:54:56 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port55555-TCP:V=7.93%I=7%D=9/27%Time=6515071F%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,A2,"HTTP/1\.0\x20302\x20Found\r\nContent-Type:\x20text/html;\
SF:x20charset=utf-8\r\nLocation:\x20/web\r\nDate:\x20Thu,\x2028\x20Sep\x20
SF:2023\x2004:54:55\x20GMT\r\nContent-Length:\x2027\r\n\r\n<a\x20href=\"/w
SF:eb\">Found</a>\.\n\n")%r(GenericLines,67,"HTTP/1\.1\x20400\x20Bad\x20Re
SF:quest\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x
SF:20close\r\n\r\n400\x20Bad\x20Request")%r(HTTPOptions,60,"HTTP/1\.0\x202
SF:00\x20OK\r\nAllow:\x20GET,\x20OPTIONS\r\nDate:\x20Thu,\x2028\x20Sep\x20
SF:2023\x2004:54:56\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRequest
SF:,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;
SF:\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request"
SF:)%r(Help,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20tex
SF:t/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20
SF:Request")%r(SSLSessionReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nCon
SF:tent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\
SF:r\n400\x20Bad\x20Request")%r(TerminalServerCookie,67,"HTTP/1\.1\x20400\
SF:x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nC
SF:onnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(TLSSessionReq,67,"
SF:HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/plain;\x20c
SF:harset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20Request")%r(K
SF:erberos,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:\x20text
SF:/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20Bad\x20R
SF:equest")%r(FourOhFourRequest,EA,"HTTP/1\.0\x20400\x20Bad\x20Request\r\n
SF:Content-Type:\x20text/plain;\x20charset=utf-8\r\nX-Content-Type-Options
SF::\x20nosniff\r\nDate:\x20Thu,\x2028\x20Sep\x202023\x2004:55:23\x20GMT\r
SF:\nContent-Length:\x2075\r\n\r\ninvalid\x20basket\x20name;\x20the\x20nam
SF:e\x20does\x20not\x20match\x20pattern:\x20\^\[\\w\\d\\-_\\\.\]{1,250}\$\
SF:n")%r(LPDString,67,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Type:
SF:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20close\r\n\r\n400\x20
SF:Bad\x20Request")%r(LDAPSearchReq,67,"HTTP/1\.1\x20400\x20Bad\x20Request
SF:\r\nContent-Type:\x20text/plain;\x20charset=utf-8\r\nConnection:\x20clo
SF:se\r\n\r\n400\x20Bad\x20Request");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 109.41 seconds
```

1. Based from the nmap results, the machine runs webapps and opens ssh login.
2. Anyway the webapp which not filtered is only at port 55555.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f462ffac-4cfd-4359-92fe-acaa2ecb8aed)


3. Creating a basket with random names shall resulting to the right red box.
4. Clicking one of the basket, shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8abed4ea-1992-44f2-bdcd-5a3a6817c445)


5. Wappalyzer itself does not show all the version.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c23ca5fd-b812-47ad-bba5-4ad34c3decb9)


6. Searching "Request Baskets Exploit" on the internet shall resulting to this.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0488ecd0-690d-4107-993a-16476e404339)


7. Again the problem is we need to identify the service version for request baskets.
8. Anyway, gathering information about this vuln resulting to the same version discussed --> v1.2.1.
9. The vuln shall stay the same --> SSRF.
10. Also I noticed it lately, the version actually shown at the homepage.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4d16ec67-ee32-4642-af8e-caa348fca27f)


11. So it's clear the vuln should be SSRF and the CVE should be --> CVE-2023-27163.
12. Sadly metasploit does not have that CVE version.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/12b86143-b267-453c-b276-cd8055891cc0)

13. Hence, we need to exploit this manually.
14. Found a github POC --> `https://github.com/entr0pie/CVE-2023-27163` discussing this vuln.
15. Based from this documentation, we're using a bashscript which helps us to access port 80 which is filtered before.
16. Let's follow the steps shown there.

> HOW TO RUN

```
./CVE-2023-27163.sh http://10.10.11.224:55555/ http://127.0.0.1:80/
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7613c722-d6fc-40e8-abff-859db3f62061)

17. Great! Let's access the endpoint shown with it's token.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df5e2a78-1495-4037-8e72-3b383a28f28f)


> ADD /web/ before the basket name, resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7130af28-6b0a-4f2b-93a6-10fe1966d383)


18. Insert the token.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5d74a66-0377-41e1-83ba-6bee3dc555d5)

19. 



