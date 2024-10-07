# Ultimatum
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3ee7200-1193-4c98-9a5a-39593799f95f)


## Lessons Learned:
- Reviewing catscale data acquisition.
- Identify CVE version related to ultimate-member plugin.
- Identify backdoor user and persistence activity.

## SCENARIO:

<p align="justify">
One of the Forela WordPress servers was a target of notorious Threat Actors (TA). The website was running a blog dedicated to the Forela Social Club, where Forela employees can chat and discuss random topics. Unfortunately, it became a target of a threat group. The SOC team believe this was due to the blog running a vulnerable plugin. The IT admin already followed the acquisition playbook and triaged the server for the security team. Ultimately (no pun intended) it is your responsibility to investigate the incident. Step in and confirm the culprits behind the attack and restore this important service within the Forela environment.
</p>

## STEPS:
1. This time we're tasked to investigate an incident from Forela WordPress Servers. It is known that the server running a website with a vulnerable plugin. We're asked to hunt and confirm the culprits and restore the service.
2. Based from the acquisition performed, it is clear that the IT admin team is using a Linux acquisition tool named **CatScale**.

![image](https://github.com/user-attachments/assets/5f06bdcb-2f18-4e64-ba9c-9ba809d53378)


![image](https://github.com/user-attachments/assets/7018b428-59f0-400a-b588-5579896f426e)


> 1ST QUESTION --> ANS: WPScan/3.8.24

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6401b787-0892-49bd-ba1a-43647a099025)

3. To identify fingerprinting activity, we can review log at **Logs** directory.
4. Our interest should be log inside --> `ip-172-31-11-131-20230808-0937-var-log.tar.gz`.
5. Upon extracting it, found several **Apache** directory which indicates a web server log. Great!

![image](https://github.com/user-attachments/assets/611e783a-70da-4f0c-aa6f-d5d52c4818b7)

![image](https://github.com/user-attachments/assets/bd4c1008-0fd3-4763-8e23-c9dc391453c7)


6. Upon reviewing the log, found the scanning tool used by the attacker and it's version.
7. It's **WPScan** version **3.8.24**.

![image](https://github.com/user-attachments/assets/1ddb3037-c6bf-4f26-9fc7-048d02ada4e9)

> 2ND QUESTION --> ANS: CVE-2023-3460	

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf6ee9e8-e58b-40da-9652-2fe8302a1754)


8. It's not efficient to review the log using text editor. It's best to integrate it with ELK stack or other tools which help user in collect and visualize data.
9. Anyway, long story short found an agent named **Secragon Offensive**.

![image](https://github.com/user-attachments/assets/26a31cf2-9bd8-4088-bb24-9da3056f4494)


10. Search it on the internet, resulting to few CVEs POC.

![image](https://github.com/user-attachments/assets/6857a8f4-42f5-4b7e-bc8c-093b3992e072)


11. Both POC states the same objective --> to be authorized for admin access.
12. Also noticed a plugin is used previously. This could be a hint to our CVE version guess.

![image](https://github.com/user-attachments/assets/ab8f31ba-1919-4f94-b142-79028ac91073)


13. Searching about CVE related to the plugin, resulting to same CVE version we found before.

![image](https://github.com/user-attachments/assets/34177f8d-f262-461d-a8dd-b2d78d1f959f)


14. Reviewing the first website, seems it matched our finding. Actually our finding itself is not enough to identify wheter we found the correct CVE.
15. For better analysis, another artifacts and further correlation is needed, but I am just too lazy to do it.

![image](https://github.com/user-attachments/assets/edbb13d3-d9b3-441e-b6fa-97012170357d)


16. Reviewing another log file named --> **access.log.1** found different plugin version used. But this match the CVE details we read before.

![image](https://github.com/user-attachments/assets/3197fcd6-bf14-4447-9d22-6f75df5173b2)


#### NOTES:

```
The plugin does not prevent visitors from creating user accounts with arbitrary capabilities, effectively allowing
attackers to create administrator accounts at will. This is actively being exploited in the wild.
```

17. Another outsource found WPScan documentation that shows convincing details.

![image](https://github.com/user-attachments/assets/60e65778-5f8d-4eee-aa3f-0a2cdad1a45a)


18. Remembering the very first log we analyzed is identified using version 2.6.4. We can tell that we already find the correct CVE version!
19. As you can see afterwards the plugin is accessed, the threat actor can access the admin resource. The threat actor IP is **198.16.74.45**.
20. Interesting it is a public cloud IP, this could indicates that the attacker manually explored the website after logging in.

![image](https://github.com/user-attachments/assets/c6a0eaeb-2d65-44e9-8019-8342431883d9)

![image](https://github.com/user-attachments/assets/01f79946-943d-47a9-9aa6-5a3d53cec286)


> 3RD QUESTION --> ANS: `23.106.60.163`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6348ab3c-7129-49da-bdfd-2ff915980650)


20. Now to identify the real threat actor IP, we need to find the initial access OR the easiest way simply by check the IP used for the scanning activity.

![image](https://github.com/user-attachments/assets/da9d50ce-fbb5-4867-8f39-66ecde526dcd)

21. Great! Now we know the real threat actor IP is **23.106.60.163**.

> 4TH QUESTION --> ANS: secragon.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c02c2301-69c0-4b70-9014-5bcec3fed18f)


22. To identify backdoor user, simply search the attempt to register account after the exploitation attempt.

![image](https://github.com/user-attachments/assets/340e579e-a14d-4484-ab7d-c9f5b48e5c43)


23. Great! Now we know the backdoor user is **secragon**.

> 5TH QUESTION --> ANS: `198.16.74.45`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/81716e5f-3cbf-4c7e-9b99-592b139fd35b)


24. Noticed after it gained access to admin resource, the attacker IP changed to the public cloud IP --> **198.16.74.45**.

> 6TH QUESTION --> ANS: /var/www/html/wp-content/themes/twentytwentythree/patterns/hidden-comments.php

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68be2673-8d48-45fe-be2e-356974454ec9)


25. Long story short, found a suspicious file access inside the admin resource. It's a php file named hidden-comments.
26. It's because afterwards, a shell execution is attempted.

![image](https://github.com/user-attachments/assets/67681c9a-e244-4a2e-8cac-7c120bcc5dd9)


![image](https://github.com/user-attachments/assets/414d0132-706b-41cc-a052-b79abe071595)


27. More interestingly, the plugin used is a plugin that can upload, edit, create, and remove theme files.

![image](https://github.com/user-attachments/assets/5072eb09-e746-4997-8f28-08754341d05c)


29. It's very straight forward that **hidden-comments.php** is a theme file that used for persistence.
30. Anyway let's correlate with **error.log**, remembering it's a **source** file which edited and it's human activity, hence an error could happen during the code writing.
31. After reviewing it, indeed an error happened at timestamp `09:01:04` right after the file is edited at `09:00:51`.

> error.log

![image](https://github.com/user-attachments/assets/ff01bd28-59a8-402b-a5fd-f1866c441509)


> access.log

![image](https://github.com/user-attachments/assets/a4f8cf6b-25b2-4d6a-be21-9963ef23216b)


32. Remembering no other theme files opened, hence it's clear that **hidden-comments.php** is the backdoor file.
33. For the full path can be seen at the **error.log**.

> 7TH QUESTION --> ANS: `'uname -a; w; id; /bin/bash -i';`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4deadac-6f4d-4192-b2a7-a333880835b5)


34. Now to review the code of it, we need to traverse to **Misc -> ip-172-31-11-131-20230808-0937-pot-webshell-first-1000.txt**.
35. Then search for --> **hidden-comments.php**.

![image](https://github.com/user-attachments/assets/bd686b50-89b3-4467-8bd9-58bd04608851)


36. `$shell` variable contains `uname -a; w; id; /bin/bash -i`
37. Shortly those commands are for gather system information and user details by printig the systems's kernel version and arch.
38. Also shows logged-in user and their activities, and displaying current user's UID, GID, and groups.
39. Lastly it launch an interactive shell.

> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/48a7eaa2-643a-42a2-838b-f4729c98d6f3)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f3587f8b-b17c-4c32-a10b-3618a0d8c281)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5697102e-1e65-4668-9538-eb41c154e870)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/53a93703-6ecc-43a3-b1fe-553e73ca73be)


## IMPORTANT LINKS:

```
https://github.com/WithSecureLabs/LinuxCatScale
https://wpscan.com/vulnerability/694235c7-4469-4ffd-a722-9225b19e98d7/
```
