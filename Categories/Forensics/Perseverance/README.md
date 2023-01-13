# Perseverance
> Write-up author: jon-brandy
## DESCRIPTION:
During a recent security assessment of a well-known consulting company, the competent team found some employees' credentials in publicly available breach databases. 
Thus, they called us to trace down the actions performed by these users. During the investigation, it turned out that one of them had been compromised. 
Although their security engineers took the necessary steps to remediate and secure the user and the internal infrastructure, the user was getting compromised repeatedly.
Narrowing down our investigation to find possible persistence mechanisms, we are confident that the malicious actors use WMI to establish persistence.
You are given the WMI repository of the user's workstation. Can you analyze and expose their technique?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

