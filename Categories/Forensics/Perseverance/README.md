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

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212272170-018e887b-e3e3-4ae6-9969-4311a33a0402.png)


![image](https://user-images.githubusercontent.com/70703371/212272204-e901bf39-fcd0-4c9f-aa0d-afc256689db8.png)


2. Based from the description, we can assume that these files are the WMI repository of a compromised user's workstation.
3. Since it's new for me, so i did a small outsource about WMI and found [this](https://netsecninja.github.io/dfir-notes/wmi-forensics/) website which contains great information about WMI Forensics.

```
C:\Windows\System32\wbem\Repository - Stores the CIM database files
- OBJECTS.DATA - Objects managed by WMI
- INDEX.BTR - Index of files imported into OBJECTS.DATA
- MAPPING[1-3].MAP - correlates data in OBJECTS.DATA and INDEX.BTR

C:\Windows\System32\wbem\AutoRecover - MOF files with #PRAGMA AUTORECOVER in first line will be saved here in case the repo needs to be built again, establishing persistence.
- Review file timestamps
```

4. We should be able to parse the compromised user's WMI repository and extract information about types of commands executed. So i did a small outsource again on the internet and found [this](https://github.com/davidpany/WMI_Forensics) script, let's use it to parse our files.

##### Notes: Can't run the script with python3, run it with python2

```py
python2 PyWMIPersistenceFinder.py ../../../../../Downloads/bin/foren/perse/OBJECTS.DATA
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212274527-3cd98208-30b5-4501-b459-c273f89a344a.png)


![image](https://user-images.githubusercontent.com/70703371/212274564-0acf4ecd-7497-4236-b236-f93336697de6.png)


5. Based from the result we know that the WMI consumer name is `Windows Update`.



## LEARNING REFERENCES:

```
https://netsecninja.github.io/dfir-notes/wmi-forensics/
https://github.com/davidpany/WMI_Forensics
```
