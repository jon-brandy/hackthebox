# Broker
> Write-up author: jon-brandy
## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.243 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-16 23:46 PST
Nmap scan report for 10.10.11.243
Host is up (0.031s latency).
Not shown: 65526 closed tcp ports (conn-refused)
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3eea454bc5d16d6fe2d4d13b0a3da94f (ECDSA)
|_  256 64cc75de4ae6a5b473eb3f1bcfb4e394 (ED25519)
80/tcp    open  http       nginx 1.18.0 (Ubuntu)
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  basic realm=ActiveMQRealm
|_http-title: Error 401 Unauthorized
|_http-server-header: nginx/1.18.0 (Ubuntu)
1883/tcp  open  mqtt
| mqtt-subscribe: 
|   Topics and their most recent payloads: 
|     ActiveMQ/Advisory/Consumer/Topic/#: 
|_    ActiveMQ/Advisory/MasterBroker: 
5672/tcp  open  amqp?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GetRequest, HTTPOptions, RPCCheck, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
|     AMQP
|     AMQP
|     amqp:decode-error
|_    7Connection from client using unsupported AMQP attempted
|_amqp-info: ERROR: AQMP:handshake expected header (1) frame, but was 65
8161/tcp  open  http       Jetty 9.4.39.v20210325
|_http-title: Error 401 Unauthorized
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  basic realm=ActiveMQRealm
|_http-server-header: Jetty(9.4.39.v20210325)
46053/tcp open  tcpwrapped
61613/tcp open  stomp      Apache ActiveMQ
| fingerprint-strings: 
|   HELP4STOMP: 
|     ERROR
|     content-type:text/plain
|     message:Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolException: Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolConverter.onStompCommand(ProtocolConverter.java:258)
|     org.apache.activemq.transport.stomp.StompTransportFilter.onCommand(StompTransportFilter.java:85)
|     org.apache.activemq.transport.TransportSupport.doConsume(TransportSupport.java:83)
|     org.apache.activemq.transport.tcp.TcpTransport.doRun(TcpTransport.java:233)
|     org.apache.activemq.transport.tcp.TcpTransport.run(TcpTransport.java:215)
|_    java.lang.Thread.run(Thread.java:750)
61614/tcp open  http       Jetty 9.4.39.v20210325
|_http-title: Site doesn't have a title.
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Jetty(9.4.39.v20210325)
61616/tcp open  apachemq   ActiveMQ OpenWire transport
| fingerprint-strings: 
|   NULL: 
|     ActiveMQ
|     TcpNoDelayEnabled
|     SizePrefixDisabled
|     CacheSize
|     ProviderName 
|     ActiveMQ
|     StackTraceEnabled
|     PlatformDetails 
|     Java
|     CacheEnabled
|     TightEncodingEnabled
|     MaxFrameSize
|     MaxInactivityDuration
|     MaxInactivityDurationInitalDelay
|     ProviderVersion 
|_    5.15.15
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5672-TCP:V=7.93%I=7%D=11/16%Time=65571A5E%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19\x02\0\0\0\0S\x10
SF:\xc0\x0c\x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0\0\0S\x18\xc0S\x0
SF:1\0S\x1d\xc0M\x02\xa3\x11amqp:decode-error\xa17Connection\x20from\x20cl
SF:ient\x20using\x20unsupported\x20AMQP\x20attempted")%r(HTTPOptions,89,"A
SF:MQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19\x02\0\0\0\0S\x10\xc0\x0c\x04\xa
SF:1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0\0\0S\x18\xc0S\x01\0S\x1d\xc0M\x
SF:02\xa3\x11amqp:decode-error\xa17Connection\x20from\x20client\x20using\x
SF:20unsupported\x20AMQP\x20attempted")%r(RTSPRequest,89,"AMQP\x03\x01\0\0
SF:AMQP\0\x01\0\0\0\0\0\x19\x02\0\0\0\0S\x10\xc0\x0c\x04\xa1\0@p\0\x02\0\0
SF:`\x7f\xff\0\0\0`\x02\0\0\0\0S\x18\xc0S\x01\0S\x1d\xc0M\x02\xa3\x11amqp:
SF:decode-error\xa17Connection\x20from\x20client\x20using\x20unsupported\x
SF:20AMQP\x20attempted")%r(RPCCheck,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0
SF:\0\x19\x02\0\0\0\0S\x10\xc0\x0c\x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x
SF:02\0\0\0\0S\x18\xc0S\x01\0S\x1d\xc0M\x02\xa3\x11amqp:decode-error\xa17C
SF:onnection\x20from\x20client\x20using\x20unsupported\x20AMQP\x20attempte
SF:d")%r(DNSVersionBindReqTCP,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19
SF:\x02\0\0\0\0S\x10\xc0\x0c\x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0
SF:\0\0S\x18\xc0S\x01\0S\x1d\xc0M\x02\xa3\x11amqp:decode-error\xa17Connect
SF:ion\x20from\x20client\x20using\x20unsupported\x20AMQP\x20attempted")%r(
SF:DNSStatusRequestTCP,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19\x02\0\
SF:0\0\0S\x10\xc0\x0c\x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0\0\0S\x
SF:18\xc0S\x01\0S\x1d\xc0M\x02\xa3\x11amqp:decode-error\xa17Connection\x20
SF:from\x20client\x20using\x20unsupported\x20AMQP\x20attempted")%r(SSLSess
SF:ionReq,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19\x02\0\0\0\0S\x10\xc
SF:0\x0c\x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0\0\0S\x18\xc0S\x01\0
SF:S\x1d\xc0M\x02\xa3\x11amqp:decode-error\xa17Connection\x20from\x20clien
SF:t\x20using\x20unsupported\x20AMQP\x20attempted")%r(TerminalServerCookie
SF:,89,"AMQP\x03\x01\0\0AMQP\0\x01\0\0\0\0\0\x19\x02\0\0\0\0S\x10\xc0\x0c\
SF:x04\xa1\0@p\0\x02\0\0`\x7f\xff\0\0\0`\x02\0\0\0\0S\x18\xc0S\x01\0S\x1d\
SF:xc0M\x02\xa3\x11amqp:decode-error\xa17Connection\x20from\x20client\x20u
SF:sing\x20unsupported\x20AMQP\x20attempted");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port61613-TCP:V=7.93%I=7%D=11/16%Time=65571A59%P=x86_64-pc-linux-gnu%r(
SF:HELP4STOMP,27F,"ERROR\ncontent-type:text/plain\nmessage:Unknown\x20STOM
SF:P\x20action:\x20HELP\n\norg\.apache\.activemq\.transport\.stomp\.Protoc
SF:olException:\x20Unknown\x20STOMP\x20action:\x20HELP\n\tat\x20org\.apach
SF:e\.activemq\.transport\.stomp\.ProtocolConverter\.onStompCommand\(Proto
SF:colConverter\.java:258\)\n\tat\x20org\.apache\.activemq\.transport\.sto
SF:mp\.StompTransportFilter\.onCommand\(StompTransportFilter\.java:85\)\n\
SF:tat\x20org\.apache\.activemq\.transport\.TransportSupport\.doConsume\(T
SF:ransportSupport\.java:83\)\n\tat\x20org\.apache\.activemq\.transport\.t
SF:cp\.TcpTransport\.doRun\(TcpTransport\.java:233\)\n\tat\x20org\.apache\
SF:.activemq\.transport\.tcp\.TcpTransport\.run\(TcpTransport\.java:215\)\
SF:n\tat\x20java\.lang\.Thread\.run\(Thread\.java:750\)\n\0\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port61616-TCP:V=7.93%I=7%D=11/16%Time=65571A59%P=x86_64-pc-linux-gnu%r(
SF:NULL,140,"\0\0\x01<\x01ActiveMQ\0\0\0\x0c\x01\0\0\x01\*\0\0\0\x0c\0\x11
SF:TcpNoDelayEnabled\x01\x01\0\x12SizePrefixDisabled\x01\0\0\tCacheSize\x0
SF:5\0\0\x04\0\0\x0cProviderName\t\0\x08ActiveMQ\0\x11StackTraceEnabled\x0
SF:1\x01\0\x0fPlatformDetails\t\0\x04Java\0\x0cCacheEnabled\x01\x01\0\x14T
SF:ightEncodingEnabled\x01\x01\0\x0cMaxFrameSize\x06\0\0\0\0\x06@\0\0\0\x1
SF:5MaxInactivityDuration\x06\0\0\0\0\0\0u0\0\x20MaxInactivityDurationInit
SF:alDelay\x06\0\0\0\0\0\0'\x10\0\x0fProviderVersion\t\0\x075\.15\.15");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.06 seconds
```

1. Based from the nmap results, the machine opens several http services (80, 8161, and 61614). The last ports seems to be inaccessible.
2. But the first two gives me the same result, which prompts a login form.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cdd76154-9c31-48c1-83f1-5cdf9b7ae968)


3. After filled it with random cred or simply cancel the login attempt, the web server's responded with unauth's status code.
4. The good thing we can see identified the webapps using Java Web Server and Java Servlett Container (Jetty).
5. Researching the Jetty version on the internet shall found this:

```
https://security.snyk.io/package/maven/org.eclipse.jetty:jetty-server/9.4.39.v20210325
https://access.redhat.com/security/cve/cve-2021-28169
```

6. But analyzing the vulnerabilities discussed, seems not what can be exploited on this machine.
7. Long story short, I tried to enter `admin:admin` at the login prompt and logged in.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f6eb03f1-752c-425c-b6ff-f72a8aaf5551)


8. Searching the vulnerabilities for the current version, shall resulting to this:

```
https://activemq.apache.org/news/cve-2023-46604?ref=deep-kondah.com
```

9. 
