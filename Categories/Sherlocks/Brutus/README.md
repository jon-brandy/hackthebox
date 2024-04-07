# Brutus
> Write-up author: jon-brandy

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

> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7af97fb5-68f5-418a-898a-cde091decf5e)


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

