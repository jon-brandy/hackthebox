# Brutus
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/332c0735-36c7-4419-8b0a-c3bd0e6699f2)


## Lessons Learned:
- sdasd

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

> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4b3119b-f1a6-48e8-b4ec-5c689da1984a)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/110ca3ed-445d-435a-9b97-d24c45ba47fd)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9357b082-412e-4fe2-8418-9770175aa017)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/66eb2ed9-d302-4e9b-b3f2-367dcc8ecb67)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ccabb66-c177-4d59-9657-e2e411f6dbd7)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4dffcc64-f4c4-48d9-b674-1e7c3140be20)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e2e4ac94-d7a5-48ec-af40-ea78df85b254)

