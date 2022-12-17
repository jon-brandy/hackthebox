# Easy Phish
> Write-up author: jon-brandy
## DESCRIPTION:
Customers of secure-startup.com have been recieving some very convincing phishing emails, can you figure out why?
## HINT:
- NONE
## STEPS:
1. For this challenge we may use several enumeration tools for OSINT.
2. I used `dig` for this challenge.
3. Run -> `dig TXT secure-startup.com`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208222134-71b5436d-1e2e-436f-a470-04388459a2e9.png)


4. Notice there's a partition of the flag.

![image](https://user-images.githubusercontent.com/70703371/208222158-193600ef-2cae-42c4-9a0d-d29e447bcc15.png)


5. Next, run `dig TXT secure-startup.com _dmarc.secure-startup.com`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208222177-06ac55be-0e98-4cd3-8e41-2106edc501da.png)


6. Got another one, but this time has the `}`.
7. Concate all the partition.

> RESULT

```
HTB{RIP_SPF_Always_2nd_F1ddl3_2_DMARC}
```

8. Got the flag!


## FLAG

```
HTB{RIP_SPF_Always_2nd_F1ddl3_2_DMARC}
```


