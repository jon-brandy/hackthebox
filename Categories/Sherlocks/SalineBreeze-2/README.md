# SalineBreeze-2
> Write-up author: jon-brandy

<img width="460" height="166" alt="image" src="https://github.com/user-attachments/assets/94dc13b0-5e69-4506-b708-f633138b92d6" />


## Lessons Learned:
1. Demodex TTPs (associated with Demodex, Salt Typhoon / Earth Estries & Ghost Emperor).
2. PowerShell deobfuscation and reverse engineering (decrypt AES-256-CBC).
3. Dynamic malware analysis using FLARE-VM and Process Hacker.
4. Using API Monitor to capture win32 API function.
5. Static malware analysis using PEStudio and Ghidra.

## SCENARIO:
<p align="justify">Your boss was so impressed with your research skills that you've been "rewarded" with a new task: malware analysis. Your mission is to investigate a piece of malware linked to the infamous cyber espionage group, Salt Typhoon. They've been targeting critical infrastructure, and it's up to you to uncover their tactics and techniques.</p>

## STEPS:
1. In this case, we are tasked with performing a malware analysis on a .ps1 file that is suspected to be linked to an infamous cyber-espionage group known as Salt Typhoon.
2. Upon a quick review of the provided PowerShell script, we can clearly identify encrypted strings and an AES-based decrypt-and-execute loader logic.

> ONEDRIVED.PS1

<img width="1076" height="707" alt="image" src="https://github.com/user-attachments/assets/74f24f95-80b8-4024-aaa9-4a3136724299" />


> 1ST QUESTION --> ANS: `Demodex`

<img width="1414" height="216" alt="image" src="https://github.com/user-attachments/assets/51072693-dabd-493d-bbe7-90fdf570d03a" />


3. While reviewing online articles about Salt Typhoon, one article curated by [Trend Micro](https://www.trendmicro.com/en_us/research/24/k/earth-estries.html) describes a DEMODEX rootkit infection chain that used the same PowerShell script name as the one we have now.
4. Also note that it will also drop a DLL named `msmp4dec.dll`.

<img width="1480" height="776" alt="image" src="https://github.com/user-attachments/assets/c1c970bc-dfc4-4089-9ae1-4c24e8701095" />


5. The article also states that, based on Trend Micro telemetry, they identified specific commands used by the threat actor to make the script functional.
6. Let's try that on our sandbox.

<img width="927" height="348" alt="image" src="https://github.com/user-attachments/assets/7847d7be-1b60-4ff7-a9f4-b8597d33a499" />

7. Comparing the results of executing the PowerShell script with and without the password mentioned in the article shows different outcomes.
8. When the password is used, the script executes without errors.

<img width="1165" height="587" alt="image" src="https://github.com/user-attachments/assets/de067aac-d83f-441d-b39f-3a14adcc3a58" />

9. It also dropped the same DLL name documented in the article.

<img width="634" height="409" alt="image" src="https://github.com/user-attachments/assets/b9b6066a-6d3e-42d0-9dfa-688fc05b67e0" />
  
10. This briefly concludes that we are dealing with the Demodex malware family.

> 2ND QUESTION --> ANS: `System.Security.Cryptography.AesManaged`

<img width="1413" height="214" alt="image" src="https://github.com/user-attachments/assets/7f5ab020-64fe-4141-9ad7-bc8fc202989e" />

10. Previously we identified an encoded base64 strings which utilized as AES object creation.
11. Decoding the base64 strings shall revealed -> `System.Security.Cryptography.AesManaged`.

<img width="1355" height="796" alt="image" src="https://github.com/user-attachments/assets/9994681b-8b1c-4041-9f52-0e978fde419c" />


11. It means the related line actually referred as:

```ps1
$0 = New-Object System.Security.Cryptography.AesManaged
```

12. It is also important to note that, since there is no explicit mode assignment, the AES mode defaults to CBC with PKCS7 padding.


> 3RD QUESTION --> ANS: `$k`

<img width="1413" height="213" alt="image" src="https://github.com/user-attachments/assets/f681489d-69b6-4c31-ae28-e563b8193fc9" />


13. Upon reviewing the script again, it is clear that the variable `$k` is used to store the first argument passed by the user.
14. The argument passed is `password@123`.

<img width="1890" height="152" alt="image" src="https://github.com/user-attachments/assets/a6fc82e3-304b-4fa3-8a5e-803f9f021f85" />


> 4TH QUESTION --> ANS: `password@123`

<img width="1413" height="219" alt="image" src="https://github.com/user-attachments/assets/22fa89d4-95a7-4408-81d1-eeeeebd1ead0" />


15. Previously we identified `password@123` indeed the correct one.

> 5TH QUESTION --> ANS: `midihelp`

<img width="1416" height="215" alt="image" src="https://github.com/user-attachments/assets/43aa3efb-ae9d-438a-a608-d99d5cc357a7" />


16. Since we already know which encryption is used to obfuscate the payload, we can attempt to decrypt it using the same encryption logic (AES-256-CBC).
17. In this case, I used a customized Python script to decrypt the payload:

```py
from Crypto.Cipher import AES
import base64

def decr(enc, argp):
    key = argp.ljust(32, '0')
    keyb = key.encode('utf-8')
    iv = bytes(16)
    
    encr_data= base64.b64decode(enc)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    
    decr_bytes = cipher.decrypt(encr_data)
    
    # Remove PKCS7 padding
    padding_length = decr_bytes[-1]
    decr_bytes = decr_bytes[:-padding_length]
  
    res = decr_bytes.decode('utf-8')
    
    return res

encrypted_string = "" # pass the encrypted payload here
key = "password@123"
try:
  result = decr(encrypted_string, key)
  print(f"Decrypted content: {result}")
except Exception as e:
  print(f"Decryption failed: {e}")
```

> RESULT

<img width="1647" height="1096" alt="image" src="https://github.com/user-attachments/assets/9b1d5910-97a1-46f1-a328-b5d2f2496aa4" />

18. Great! After decrypting the payload, we can now identify the value assigned to the variable `$cregvalue`.

<img width="889" height="422" alt="image" src="https://github.com/user-attachments/assets/db94bb56-773d-4aaa-aed1-aec0de916281" />

19. In the top lines of the script, the value "midihelp" is assigned to the variable `$cregvalue`.

> 6TH QUESTION --> ANS: `3b1c251b0b37b57b755d4545a7dbbe4c29c15baeca4fc2841f82bc80ea877b66`

<img width="1414" height="215" alt="image" src="https://github.com/user-attachments/assets/e5a51a57-a916-46e6-aa8b-6ad54e5b53a6" />

20. To identify the SHA-256 checksum, based on the script logic, we simply need to decode the Base64-encoded bytes and then calculate the checksum.

<img width="801" height="524" alt="image" src="https://github.com/user-attachments/assets/f70ebfad-3c72-4867-8d11-2f0b9e7da2e2" />

21. Since we also want to analyze the binary further, I saved the output. To decode and save it, I used a Python script.

```py
import base64, sys

strings = "" # the encoded strings.
res = base64.b64decode(strings)
# print(res)
out = 'decode_htb.bin'
with open(out, 'wb') as f:
    f.write(res)
```

> GET SHA-256 CHECKSUM

```
O:\HTB
λ sha256sum decode_htb.bin
3b1c251b0b37b57b755d4545a7dbbe4c29c15baeca4fc2841f82bc80ea877b66 *decode_htb.bin
```


> 7TH QUESTION --> ANS: `MsMp4Hw`

<img width="1415" height="214" alt="image" src="https://github.com/user-attachments/assets/b9111235-9749-49b8-94b7-fb64e91a842e" />

22. To identify the name of the malicious service, we need to detonate onedrived.ps1 again. However, this time, we execute Process Hacker first.
23. Using it, we were able to monitor the process names spawned by the PowerShell script.

> PROCESS HACKER

<img width="1747" height="690" alt="image" src="https://github.com/user-attachments/assets/318d6a0d-49e6-4ed6-967d-a7832214a055" />



24. Great! We found the newly created service name and the it's file location.

> 8TH QUESTION --> ANS: `C:\Windows\System32\msmp4dec.dll`

<img width="1415" height="218" alt="image" src="https://github.com/user-attachments/assets/37adc5e6-62d9-48d1-8b1c-496c98a7a1f0" />


25. Based on our previous findings, the path to the malicious DLL is at `C:\Windows\System32\msmp4dec.dll`


> 9TH QUESTION --> ANS: `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SvcHost`

<img width="1416" height="214" alt="image" src="https://github.com/user-attachments/assets/7fd53a92-f782-4b65-9a0d-2329530ac7cc" />


26. To identify the registry path used to associate the service group (msgroup) with the malicious service, we can start by checking the registry key for the `MsMp4Hw` service.

<img width="808" height="267" alt="image" src="https://github.com/user-attachments/assets/8d7bf098-ade6-4642-9011-8bf8bcb8c821" />


27. Based on our findings above, we can conclude that the registry path `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost` is used to associate the msgroup with the malicious service.
28. We can double-check it by visiting that location or we can also perform static analysis for the decrypted payload.

> CHECKING THE REGISTRY PATH

<img width="778" height="207" alt="image" src="https://github.com/user-attachments/assets/2057646d-e1a6-4ab7-8ae9-37dd1970f1c8" />

> THE LINE THAT SPECIFIES THE PATH

<img width="1533" height="260" alt="image" src="https://github.com/user-attachments/assets/e788fc30-351f-45eb-83da-fa5affa54a83" />


29. Great! It is true.

> 10TH QUESTION --> ANS: `Start-Service -name $svcname;`

<img width="1414" height="217" alt="image" src="https://github.com/user-attachments/assets/553c9d92-013a-411d-afea-fb7909d284a7" />


30. Upon reviewing the code again, at the last line after the service installation. The service is invoked by this command -> `Start-Service -name $svcname;`

<img width="1534" height="321" alt="image" src="https://github.com/user-attachments/assets/323286c9-d774-473e-8454-dda2fa276a4c" />


> 11TH QUESTION --> ANS: `GetComputerNameA`

<img width="1415" height="215" alt="image" src="https://github.com/user-attachments/assets/697d9ac8-2044-4b91-89c6-0b663728353e" />


31. There are two ways to identify the Windows API imported by the malicious DLL to obtain the local computer name: you can use `pestudio` or `ApiMonitor`.

> USING PESTUDIO

<img width="1159" height="566" alt="image" src="https://github.com/user-attachments/assets/9118dc1d-f0fb-4d23-b93e-a2ac6d707153" />


> APIMONITOR

32. Now, to verify whether this is true, we can use ApiMonitor by attaching it to the PID of the malicious svchost.exe and enabling a filter for the `GetComputerNameA` win32 API function.

<img width="1819" height="928" alt="image" src="https://github.com/user-attachments/assets/e1558d12-4a24-49f1-8151-75ced32ef9fb" />


33. Great! It clearly shows `GetComputerNameA` is utilized to obtain our local computer name.

<img width="682" height="609" alt="image" src="https://github.com/user-attachments/assets/f25911d0-782b-4b2f-86d7-aaeec0218fc3" />


> 12TH QUESTION --> ANS: `ServiceMain`

<img width="1416" height="216" alt="image" src="https://github.com/user-attachments/assets/bc5a3d16-bfd9-4b35-82f8-3e3a1ff4d098" />


34. Again, there are several ways to identify the function responsible for initiating the service. In ApiMonitor, this can be identified by checking its threads.

<img width="404" height="419" alt="image" src="https://github.com/user-attachments/assets/3d42a3c3-39e9-4fdb-aae4-84652e2b8c50" />


35. On the other hand, using Pestudio is sufficient for static analysis by reviewing the exported functions.

<img width="1134" height="445" alt="image" src="https://github.com/user-attachments/assets/65443676-68f1-441a-a520-792470205310" />


> 13TH QUESTION --> ANS: `10000`

<img width="1415" height="242" alt="image" src="https://github.com/user-attachments/assets/c2d2f5ce-23bd-4839-aa27-6076143ad90a" />


36. Decompiling and pseudonym at ghidra, we can 
 
## REFERENCE:

```
https://www.trendmicro.com/en_us/research/24/k/earth-estries.html
```
