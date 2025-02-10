# Loggy
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/41446e39-2c0d-4e6c-9963-ffc99f29db20)


## Lessons Learned:
1. Using Ghidra and **ANY.RUN** to identify Programming Language used by the Malware.
2. Using PE Studio and Detect it Easy (DIE) to identify Malicious Function Call.
3. Identify the FTP domain Used for Data Exfiltration.
4. Using GoReSym plugin for Binary Ninja.

## DESCRIPTION:

<p align="justify">Janice from accounting is beside herself! She was contacted by the SOC to tell her that her work credentials were found on the dark web by the threat intel team. We managed to recover some files from her machine and sent them to the our REM analyst.</p>

## STEPS:
1. In this case, the SOC notified a credential leak involving a user from the accounting division named Janice.
2. The credentials were found on the dark web by the threat intelligence team.
3. Afterward, the SOC team successfully recovered some files from her machine and sent them to the REM analyst.
4. As Reverse Engineering Malware (REM) Analyst, we are tasked with further investigating this case.

> INSIDE ZIP FILE

![image](https://github.com/user-attachments/assets/df7faa35-9490-4a8a-924b-b6c2899bb9a8)

> 1ST QUESTION --> ANS: `6acd8a362def62034cbd011e6632ba5120196e2011c83dc6045fcb28b590457c`

![image](https://github.com/user-attachments/assets/6bf474f8-55e6-46b0-8a95-51f89ffd7009)


5. For our initial analysis, let's load the hash to threat intelligence tool so we obtain additional info regarding this file.

![image](https://github.com/user-attachments/assets/a498fdfd-8750-4456-a06c-7dc75d71bd80)


![image](https://github.com/user-attachments/assets/333b697d-0e34-4c3d-9640-4c21607a4829)


6. Based on the result, the file marked as malicious by few security vendors and reviewing the **details** section, we can identify that the malware is compiled with Golang compiler.

![image](https://github.com/user-attachments/assets/d21bcdc2-7d94-4ac6-a6cf-be516db4ca35)

7. Checking the graph representation, it is known there are 4 contacted domains and most of them are to microsoft. It could indicate a windows API usage for network communication.

![image](https://github.com/user-attachments/assets/19b474f1-2c61-4d9a-aa89-2bcf09a781ef)


> 2ND QUESTION --> ANS: `Golang 1.22.3`

![image](https://github.com/user-attachments/assets/c2a77e91-03a3-4ba5-80b8-1bdd50341624)

8. Baseed on our previous identification, we know that we are dealing with golang binary. To identify the compiler version, we can just strings the binary and filter for **go1**.

![image](https://github.com/user-attachments/assets/1f08b726-456d-46c5-8198-b341837163a7)


> 3RD QUESTION --> ANS: `github.com/jlaffaye/ftp`

![image](https://github.com/user-attachments/assets/5da6ae1a-d4d0-49bc-bb1c-04993532cd40)


9. Next, to identify imported github repo, I used ghidra to decompile the binary.

> GHIDRA

![image](https://github.com/user-attachments/assets/f3c900b8-6e30-484b-9758-ace64781feab)

![image](https://github.com/user-attachments/assets/610a9bfd-3d7f-4fba-9277-bfef2b12c2ef)

10. Found 5 github repos and by logic the repo used for data exfiltration should be jlaffaye's repo. However to prove our assumption, we can investigate each repos since the repo's path is visible to us. (no one knows, the repo might be named different than it's actual purpose).

|hashicorp|jlaffaye|kbinani|
|:-------:|:------:|:-----:|
|![image](https://github.com/user-attachments/assets/d4ac31bc-409b-4bb8-9685-e5a3770ee259)|![image](https://github.com/user-attachments/assets/83f5073e-1468-4b75-b8e1-bd598be0a19c)|![image](https://github.com/user-attachments/assets/4becc0a3-0d1b-4451-a5fa-cd0892cca238)|


|lxn|TheTitanrain|
|:-:|:----------:|
|![image](https://github.com/user-attachments/assets/4b3c7572-8453-42e3-ae42-49d94aa3e7d9)|![image](https://github.com/user-attachments/assets/c7696ead-a04d-496b-bac5-1eaacb14b1b1)|

11. Based on the evidence above, we can much conclude github likely used to exfiltrate data should be from user **jlaffaye** (using File Transfer Protocol). Another convincing evidence is function usage related to FTP for handling files.

![image](https://github.com/user-attachments/assets/b1fd4bf0-7af5-4a8b-b28e-cd6f2159217c)



> 4TH QUESTION --> ANS: `github.com/kbinani/screenshot`

![image](https://github.com/user-attachments/assets/457e2656-482d-443f-92bb-59eb27146c01)


12. Again,  it's clear the mentioned dependency should be **github.com/kbinani/screenshot**.

![image](https://github.com/user-attachments/assets/0f180c09-0985-43ee-b217-8ed27efd54eb)


> 5TH QUESTION --> ANS: `WriteFile`

![image](https://github.com/user-attachments/assets/dd48ff11-ba9b-464d-b727-95c2f1ccd00c)


13. Now, to identify which function is used by the malware to create a file after execution, we need to list all the available functions.
14. Since it's related to file creation at windows, the function should be related to API function.

> 6TH QUESTION --> ANS: `gotthem.htb`

![image](https://github.com/user-attachments/assets/5a67d8ab-1aea-4307-bd13-8f169cb5be47)

> 7TH QUESTION --> ANS: `NottaHacker:Cle@rtextP@ssword`

![image](https://github.com/user-attachments/assets/e9561698-3f49-4bd6-b249-f5c26c290bab)

> 8TH QUESTION --> ANS: `keylog.txt`

![image](https://github.com/user-attachments/assets/4e606a27-bd4c-4482-9340-ca1505bfc984)

> 9TH QUESTION --> ANS: `janice:Password123`

![image](https://github.com/user-attachments/assets/70b56b94-e350-4444-a74e-a67d4d613534)

> 10TH QUESTIO --> ANS: `Solitaire`

![image](https://github.com/user-attachments/assets/2e3b671b-8cef-4a2d-8e14-3475107c13a8)

## IMPORTANT LINKS:

```
https://github.com/mandiant/GoReSym
```
