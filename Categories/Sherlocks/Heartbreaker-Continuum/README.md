# Heartbreaker-Continuum
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/7fe97ce5-0ab7-43a6-97ef-2e981e1c373a)

## Lessons Learned:
1. Using **PEStudio** and **Ghidra** to identify size of code bytes.
2. Using threat intelligence tool to identify conversion filename and file creation time.
3. Using hexeditor to identify the obfuscated strings offset.
4. 

## SCENARIO:

<p align="justify">Following a recent report of a data breach at their company, the client submitted a potentially malicious executable file. The file originated from a link within a phishing email received by a victim user. Your objective is to analyze the binary to determine its functionality and possible consequences it may have on their network. By analyzing the functionality and potential consequences of this binary, you can gain valuable insights into the scope of the data breach and identify if it facilitated data exfiltration. Understanding the binary's capabilities will enable you to provide the client with a comprehensive report detailing the attack methodology, potential data at risk, and recommended mitigation steps.</p>

## STEPS:
1. In this investigation case, we're tasked to reverse engineer a malicious executable file which originated from a link within an email identified as phising.
2. Once we gained valuable insights into the scope of the data breach, we're asked to provide the client with a comprehensive report detailing the attack methodology, potential data at risk, and a recommended mitigation steps (which we won't do in this writeup).

> Basic File Check

![image](https://github.com/user-attachments/assets/43ef02c5-91c7-44fe-ba46-cca1cba66ac9)

3. Based from the evidence above, the binary is identified as a **PE32 executable** and likely written in .NET supported language such as **C#** or **VB.NET**.

> 1ST QUESTION --> ANS: 12daa34111bb54b3dcbad42305663e44e7e6c3842f015cccbbe6564d9dfd3ea3

![image](https://github.com/user-attachments/assets/6bc570a4-4c53-4107-982d-0fa71a470c84)


4. One of the easiest way to identify whether a file is malicious or is a malware file, simply grab the IOC.
5. This time, I grab the **sha256** hash. Afterwards, send it to threat intelligence tool to review the hash.

![image](https://github.com/user-attachments/assets/d08e4903-f528-4b11-998a-2b1cf87748c8)


![image](https://github.com/user-attachments/assets/b012bc47-29b4-45e9-8d16-4df248ff35e6)


![image](https://github.com/user-attachments/assets/7ea63b5f-35f2-4b13-ad2f-f6dcc6b0c5c9)


6. Both **Virus Total** and **Kaspersky OpenTip** shown that the file is indeed a malware categorized as **Trojan**.
7. Also both states that the binary acts as a downloader.

> 2ND QUESTION --> ANS: `2024-03-13 10:38:06`

![image](https://github.com/user-attachments/assets/d781763c-e54a-4170-b887-ec2893e983b4)


8. Next, to identify the creation timestamp, we can check the **details** section at virus total.

![image](https://github.com/user-attachments/assets/fe6b04d2-6aaa-42f6-8658-deddee7b5d1d)


> 3RD QUESTION --> ANS: 38400

![image](https://github.com/user-attachments/assets/b0d6fc07-bb8a-4f80-bf18-d2acd71a92af)

9. Using a decompiler such as **ghidra**, we can identify the maximum size of code of the binary in bytes.

![image](https://github.com/user-attachments/assets/646a2831-b30c-4058-8b96-f05fb08b3925)


#### NOTES:

```
The size of the code in a binary file refers to the total amount of space (in bytes) that is allocated for the actual
executable instructions within the program.

However, this does not include data segments (global / static variables), resources (image, icons), headers, and metadata.
```


10. To identify the code size in the binary file, simply go to window and open the memory map and check for the .text section length.

![image](https://github.com/user-attachments/assets/05cff440-dce5-4425-93c2-193004ccd35a)


![image](https://github.com/user-attachments/assets/67ddcd8e-d5c6-433a-976a-cd93f47ed2e3)


> Another method --> simply check the **sections** in virus total under Details tab


![image](https://github.com/user-attachments/assets/f876a3e2-dd21-4499-82ad-9d2e3d0ac52d)


11. Great! Now we know the size of code is **38400**.

> 4TH QUESTION --> ANS: newILY.ps1

![image](https://github.com/user-attachments/assets/a9a862e2-ff53-483f-b73c-678647e3bb86)


12. Interesting! It states that the binary may have undergone a conversion process and based on the question, the conversion act for the **FILENAME**.
13. Actually there are simple methods to identify it, by checking the details tab, go to the **Dot Net Assembly**, and check the **Manifest Resource** field. 

![image](https://github.com/user-attachments/assets/f4ae956a-b34c-4aa2-82f2-5c5df0c54752)


14. Another method is to use **PEStudio** and check for the resource.

![image](https://github.com/user-attachments/assets/be60e120-826a-498f-8a55-570c45aa096b)


15. As you can see, both states the same filename.

> 5TH QUESTION --> ANS: 2C74

![image](https://github.com/user-attachments/assets/e59a999e-ea14-4b40-a8b6-868bee05ce2e)


16. Next, upon execute strings to identify readable strings from the binary. Found a what looks like a base64 encoded text.
17. Also the text later on decoded and an IEX is performed to naming an alias named **ilY**.

![image](https://github.com/user-attachments/assets/a0e5a96e-49dc-4e34-ba67-aa25214c6f61)


18. Interesting! Indeed the malware is using powershell script then, exactly like what we've identified for the original filename.
19. To identify the offset of which this obfuscated text, I used hexeditor and run **grep** for the initiliazed variable.

![image](https://github.com/user-attachments/assets/ff2895d2-a3dd-4256-9d43-8d86369d69ab)

20. Nice, we identified the offset!

> 6TH QUESTION --> ANS: Base64

![image](https://github.com/user-attachments/assets/02e79b45-0932-40c9-b0e3-5ba047b40201)


21. Base from the previous finding, we identified that the malware used Base64 to encode what might be it's exploit.

> 7TH QUESTION --> ANS: Invoke-WebRequest

![image](https://github.com/user-attachments/assets/3a676649-f8e7-43f1-a61e-a4d16d8b3e54)


22. Anyway, we can simply decode it manually without revise the script, because it just encode the exploit and reversed it.
23. Let's wayback it using cyberchef.

> RESULT

![image](https://github.com/user-attachments/assets/166d9aab-fc4a-4c62-a973-ba0942442f38)


24. Awesome! From now on should be easy for us, because the exploit is stop here, there are no other outbound connections which related to download another malware.
25. Long story short, after review the code, found the cmdlet used by the malware to initiate file downloads.
26. It used **Invoke-WebRequest**, this cmdlet in powershell is used to perform HTTP or HTTPS request to a web resources. In short, this cmdlet quite perform the same as **curl** and **wget**.

![image](https://github.com/user-attachments/assets/2422267f-8715-4d9f-8457-c9818c629b47)

#### NOTE:

```
cmdlet (command-let) is a lightweight command used in powershell environment.
```

> 8TH QUESTION --> ANS: `35.169.66.138,44.206.187.144`

![image](https://github.com/user-attachments/assets/46556a69-7054-4493-a6f6-d9aa3d7ebe4a)


27. Previously we identified the attacker's server IP which used to infiltrate the malware via phising.
28. Then another IP IOC is identified at **sftp** command usage.
29. Interestingly it performed `-hostkey=*/` which a method for hostkey bypass. This method allows the connection without verifying the hostkey.


![image](https://github.com/user-attachments/assets/d69a3089-dd14-411e-8f46-454defd0add3)


> 9TH QUESTION --> ANS: `C:\Users\Public\Public Files`

![image](https://github.com/user-attachments/assets/0c77c419-9648-427e-9826-cb5329987c72)


30. Luckily the deobfuscated script has convential variable naming, reviewing the script at glance, we can quickly identified the specified target directory.

![image](https://github.com/user-attachments/assets/a617c46b-fbb0-4bb8-ac31-7abafe5e7684)


> 10TH QUESTION --> ANS: T1119 

![image](https://github.com/user-attachments/assets/93479846-d902-4bdb-bd33-bbd2e385a3fd)


31. Based from MITRE page, autonomously gather data is defined as **Automated Collection** technique under **Collection**. ID --> T1119


![image](https://github.com/user-attachments/assets/0c79e2f7-0b14-4bf4-9087-5b1aded2ffc7)


> 11TH QUESTION --> ANS: M8&C!i6KkmGL1-#

![image](https://github.com/user-attachments/assets/8429c794-7bf1-4e2c-9426-3bb9264113e2)


32. Again, based from our previous finding. The password used is `M8&C!i6KkmGL1-#`.
33. Great! We've investigated the case!

## IMPORTANT LINKS:

```
https://attack.mitre.org/techniques/T1119/
https://www.virustotal.com/gui/file/12daa34111bb54b3dcbad42305663e44e7e6c3842f015cccbbe6564d9dfd3ea3/relations
```
