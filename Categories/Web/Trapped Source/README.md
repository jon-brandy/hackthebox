# Trapped Source
> Write-up author: jon-brandy
## DESCRIPTION:
Intergalactic Ministry of Spies tested Pandora's movement and intelligence abilities. She found herself locked in a room with no apparent means of escape. Her task was to unlock the door and make her way out. Can you help her in opening the door?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a webapps with a pin feature as it's password, it seems we need to guess the correct pin with 4 digits either to login or get the flag.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/1ec168c5-d25d-4b63-b49d-d604915c1710)


2. What comes to my mind we might have to make a script to bruteforce the pin, but when i opened the page source, there's a pin hardcoded there.

> PIN - 1977

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/81852a56-1774-4c58-b556-a9e1c20c0069)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4e0aba50-8ef9-4372-958f-bef03b545f6c)


3. Got the flag!

## FLAG

```
HTB{vi3w_cli13nt_s0urc3_S3cr3ts!}
```
