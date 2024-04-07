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
