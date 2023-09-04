# Steam Cloud
> Write-up author: jon-brandy
## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.133 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-04 04:50 PDT
Nmap scan report for 10.10.11.133
Host is up (0.024s latency).
Not shown: 65528 closed tcp ports (conn-refused)
PORT      STATE SERVICE          VERSION
22/tcp    open  ssh              OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 fcfb90ee7c73a1d4bf87f871e844c63c (RSA)
|   256 46832b1b01db71646a3e27cb536f81a1 (ECDSA)
|_  256 1d8dd341f3ffa437e8ac780889c2e3c5 (ED25519)
2379/tcp  open  ssl/etcd-client?
| tls-alpn: 
|_  h2
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=steamcloud
| Subject Alternative Name: DNS:localhost, DNS:steamcloud, IP Address:10.10.11.133, IP Address:127.0.0.1, IP Address:0:0:0:0:0:0:0:1
| Not valid before: 2023-09-04T10:38:42
|_Not valid after:  2024-09-03T10:38:42
2380/tcp  open  ssl/etcd-server?
| tls-alpn: 
|_  h2
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=steamcloud
| Subject Alternative Name: DNS:localhost, DNS:steamcloud, IP Address:10.10.11.133, IP Address:127.0.0.1, IP Address:0:0:0:0:0:0:0:1
| Not valid before: 2023-09-04T10:38:42
|_Not valid after:  2024-09-03T10:38:43
8443/tcp  open  ssl/https-alt
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 403 Forbidden
|     Audit-Id: e03fcb20-4c12-491a-893f-6adfb04454e4
|     Cache-Control: no-cache, private
|     Content-Type: application/json
|     X-Content-Type-Options: nosniff
|     X-Kubernetes-Pf-Flowschema-Uid: 133183cc-26de-40a3-80ed-956fa5d78715
|     X-Kubernetes-Pf-Prioritylevel-Uid: df207222-fbeb-42ee-b526-763adaf111ed
|     Date: Mon, 04 Sep 2023 11:51:15 GMT
|     Content-Length: 212
|     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/nice ports,/Trinity.txt.bak"","reason":"Forbidden","details":{},"code":403}
|   GetRequest: 
|     HTTP/1.0 403 Forbidden
|     Audit-Id: b41f28a8-e8dc-4720-b484-9bd0be5e72c6
|     Cache-Control: no-cache, private
|     Content-Type: application/json
|     X-Content-Type-Options: nosniff
|     X-Kubernetes-Pf-Flowschema-Uid: 133183cc-26de-40a3-80ed-956fa5d78715
|     X-Kubernetes-Pf-Prioritylevel-Uid: df207222-fbeb-42ee-b526-763adaf111ed
|     Date: Mon, 04 Sep 2023 11:51:14 GMT
|     Content-Length: 185
|     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
|   HTTPOptions: 
|     HTTP/1.0 403 Forbidden
|     Audit-Id: af7ae914-e616-437b-afeb-909f1a51398d
|     Cache-Control: no-cache, private
|     Content-Type: application/json
|     X-Content-Type-Options: nosniff
|     X-Kubernetes-Pf-Flowschema-Uid: 133183cc-26de-40a3-80ed-956fa5d78715
|     X-Kubernetes-Pf-Prioritylevel-Uid: df207222-fbeb-42ee-b526-763adaf111ed
|     Date: Mon, 04 Sep 2023 11:51:15 GMT
|     Content-Length: 189
|_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
|_http-title: Site doesn't have a title (application/json).
| ssl-cert: Subject: commonName=minikube/organizationName=system:masters
| Subject Alternative Name: DNS:minikubeCA, DNS:control-plane.minikube.internal, DNS:kubernetes.default.svc.cluster.local, DNS:kubernetes.default.svc, DNS:kubernetes.default, DNS:kubernetes, DNS:localhost, IP Address:10.10.11.133, IP Address:10.96.0.1, IP Address:127.0.0.1, IP Address:10.0.0.1
| Not valid before: 2023-09-03T10:38:39
|_Not valid after:  2026-09-03T10:38:39
| tls-alpn: 
|   h2
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
10249/tcp open  http             Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
10250/tcp open  ssl/http         Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=steamcloud@1693823926
| Subject Alternative Name: DNS:steamcloud
| Not valid before: 2023-09-04T09:38:45
|_Not valid after:  2024-09-03T09:38:45
| tls-alpn: 
|   h2
|_  http/1.1
10256/tcp open  http             Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8443-TCP:V=7.93%T=SSL%I=7%D=9/4%Time=64F5C4B2%P=x86_64-pc-linux-gnu
SF:%r(GetRequest,22F,"HTTP/1\.0\x20403\x20Forbidden\r\nAudit-Id:\x20b41f28
SF:a8-e8dc-4720-b484-9bd0be5e72c6\r\nCache-Control:\x20no-cache,\x20privat
SF:e\r\nContent-Type:\x20application/json\r\nX-Content-Type-Options:\x20no
SF:sniff\r\nX-Kubernetes-Pf-Flowschema-Uid:\x20133183cc-26de-40a3-80ed-956
SF:fa5d78715\r\nX-Kubernetes-Pf-Prioritylevel-Uid:\x20df207222-fbeb-42ee-b
SF:526-763adaf111ed\r\nDate:\x20Mon,\x2004\x20Sep\x202023\x2011:51:14\x20G
SF:MT\r\nContent-Length:\x20185\r\n\r\n{\"kind\":\"Status\",\"apiVersion\"
SF::\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"forbidden:
SF:\x20User\x20\\\"system:anonymous\\\"\x20cannot\x20get\x20path\x20\\\"/\
SF:\\"\",\"reason\":\"Forbidden\",\"details\":{},\"code\":403}\n")%r(HTTPO
SF:ptions,233,"HTTP/1\.0\x20403\x20Forbidden\r\nAudit-Id:\x20af7ae914-e616
SF:-437b-afeb-909f1a51398d\r\nCache-Control:\x20no-cache,\x20private\r\nCo
SF:ntent-Type:\x20application/json\r\nX-Content-Type-Options:\x20nosniff\r
SF:\nX-Kubernetes-Pf-Flowschema-Uid:\x20133183cc-26de-40a3-80ed-956fa5d787
SF:15\r\nX-Kubernetes-Pf-Prioritylevel-Uid:\x20df207222-fbeb-42ee-b526-763
SF:adaf111ed\r\nDate:\x20Mon,\x2004\x20Sep\x202023\x2011:51:15\x20GMT\r\nC
SF:ontent-Length:\x20189\r\n\r\n{\"kind\":\"Status\",\"apiVersion\":\"v1\"
SF:,\"metadata\":{},\"status\":\"Failure\",\"message\":\"forbidden:\x20Use
SF:r\x20\\\"system:anonymous\\\"\x20cannot\x20options\x20path\x20\\\"/\\\"
SF:\",\"reason\":\"Forbidden\",\"details\":{},\"code\":403}\n")%r(FourOhFo
SF:urRequest,24A,"HTTP/1\.0\x20403\x20Forbidden\r\nAudit-Id:\x20e03fcb20-4
SF:c12-491a-893f-6adfb04454e4\r\nCache-Control:\x20no-cache,\x20private\r\
SF:nContent-Type:\x20application/json\r\nX-Content-Type-Options:\x20nosnif
SF:f\r\nX-Kubernetes-Pf-Flowschema-Uid:\x20133183cc-26de-40a3-80ed-956fa5d
SF:78715\r\nX-Kubernetes-Pf-Prioritylevel-Uid:\x20df207222-fbeb-42ee-b526-
SF:763adaf111ed\r\nDate:\x20Mon,\x2004\x20Sep\x202023\x2011:51:15\x20GMT\r
SF:\nContent-Length:\x20212\r\n\r\n{\"kind\":\"Status\",\"apiVersion\":\"v
SF:1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"forbidden:\x20
SF:User\x20\\\"system:anonymous\\\"\x20cannot\x20get\x20path\x20\\\"/nice\
SF:x20ports,/Trinity\.txt\.bak\\\"\",\"reason\":\"Forbidden\",\"details\":
SF:{},\"code\":403}\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 105.87 seconds
```

1. Based from the nmap result, it's clear that we're exploiting kubernetes.
2. **Etcd**, is a kubernetes component.

> It listens on port 2379 as a client & port 2380 as a server.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/75f84365-ff85-406a-b417-ccb16be4f077)


> Kubernetes API listens on port 8443.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4d104d28-e6b3-4c70-a693-eba7dbf6e3e7)


> By default, a Kubernetes extension (Kubelet) listens on port 10250.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f4a41d7-4ca1-4149-8628-04b8c824f6fe)





