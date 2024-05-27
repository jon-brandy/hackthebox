# Jugglin
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4cb55499-7ef4-4ed8-9329-06db9c054691)


## Lessons Learned:
- Conduct Forensic Analysis for .apmx64 file.
- Using API Monitor tool to analysis the file and intercept the function call. 

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


> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/93ee9549-38e9-431f-b4e6-fd9d4db829bd)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0fbbcd47-1874-4b3a-a4e1-4a60948393a4)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9c73db6f-c2d2-4a30-8ef5-014dc9945318)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f4543e8-75d1-4155-b0bc-34e2ca218bc8)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9facab44-2a2b-44b2-8c61-ee2cadb09b5a)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/208cef87-467d-4ac6-b57d-7fc451e123dd)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7784474-d9fc-4c32-95b5-2c42bf7bedeb)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f345e08e-65fc-44a2-809f-a172de4a637f)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa73fe3d-f959-4995-82c8-0304909d4809)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3fca114f-def3-4024-b1ff-36dd07d9661a)


> 12TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0bbd4fe3-f547-4140-9e50-129e242890f2)


