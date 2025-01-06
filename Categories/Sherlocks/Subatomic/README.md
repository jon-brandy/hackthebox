# Subatomic
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/7619feaa-40d4-4b8d-8cd5-5fe71e5a31d1)


## Lesson(s) Learned:
1. Using `Detect it Easy (DIE)` to identify file type.
2. Identifying unique GUID used by the malware for installation.

## SCENARIO:

<p align="justify">Forela is in need of your assistance. They were informed by an employee that their Discord account had been used to send a message with a link to a file they suspect is malware. The message read: "Hi! I've been working on a new game I think you may be interested in it. It combines a number of games we like to play together, check it out!". The Forela user has tried to secure their Discord account, but somehow the messages keep being sent and they need your help to understand this malware and regain control of their account! Warning: This is a warning that this Sherlock includes software that is going to interact with your computer and files. This software has been intentionally included for educational purposes and is NOT intended to be executed or used otherwise. Always handle such files in isolated, controlled, and secure environments. One the Sherlock zip has been unzipped, you will find a DANGER.txt file. Please read this to proceed.</p>

## STEPS:
1. A Discord account has been compromised and is being used to send messages containing a link to a suspected malicious file. Despite the owner's efforts to secure the account, the messages continue to be sent.
2. As forensic analysts, our task is to investigate the incident and analyze the malware to understand its behavior and regain control of the account.
3. Unzipping the zip file shall resulting to 2 files. Those are **.txt** file and the zipped malware binary.

![image](https://github.com/user-attachments/assets/a4859d6d-4738-4fcb-a8df-9ae2ea0505c8)

> Danger.txt

![image](https://github.com/user-attachments/assets/15b5fe39-d4d5-4e41-bf8f-37fe7b691e37)


4. Unzipping the **malware.zip** file using the provided password, shall resulting to a binary named **nsis-installer.exe**.

![image](https://github.com/user-attachments/assets/3d5ea2ad-681b-409a-b80f-928fc65a8c20)

5. Anyway, this is interesting because upon checking the file **properties** found `Unauthenticated Attributes`. This finding could indicate that there is additional data in the file that was not included in Microsoft's signing process.
6. It indicates a masquerading technique.

![image](https://github.com/user-attachments/assets/36a457f4-02de-4837-820b-b4dc6649a9be)

7. As an additional information, another tool like `Detect it Easy (DIE)` is useful to identify the actual file type of a file.

![image](https://github.com/user-attachments/assets/be0b0f89-1b04-4d59-a772-0bb7acb19924)


#### NOTE:

```
Nullsoft Scriptable Install System (NSIS) is a professional open source system
to create windows installers.
```

> 1ST QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/410dbded-ea3d-4810-85a7-f1ab96265ef3)


5. To identify the **imphash** of this malware installer, we can simply grab the checksum and load it at virus total.
6. In **Window Powershell** terminal, we can use this command:

```
Get-Filehash .\nsis-installer.exe -Algorithm <checksum_you_want>
```

![image](https://github.com/user-attachments/assets/2eb19355-bad4-4fcb-8960-62a2b7bba0eb)


> RESULT AT VIRUS TOTAL

![image](https://github.com/user-attachments/assets/2dd3e64c-1db4-400b-ac31-7c80f88e1bbd)


7. To identify the **imphash**, simply check the **Details** tab and view the **Basic Properties** section.

![image](https://github.com/user-attachments/assets/915008cb-6762-4c81-a15b-7de3e4288fc3)


> 2ND QUESTION --> ANS: Windows Update Assistant

![image](https://github.com/user-attachments/assets/5de05f00-3bc8-4a96-a66f-3a1673754327)

8. It is known that the malware contains a digital signature and to identify the program name specified under the `SpcSpOpusInfo` Data Structure we can review the **Signature Info** section at Virus Total.
9. Viewing information under `SpcSpOpusInfo` it is clear the program name is `Windows Update Assistant`.

![image](https://github.com/user-attachments/assets/b7903e58-f60d-486a-800d-ed9c862e1e65)


> 3RD QUESTION --> ANS: `cfbc383d-9aa0-5771-9485-7b806e8442d5`

![image](https://github.com/user-attachments/assets/4131d86e-5199-45b8-920c-396c49305b96)

10. Next, to identify the unique GUID used by the malware during installation, we need to interact with the binary.
11. Since previously we identified the binary file type is indeed an `nsis`, hence it contains a compressed installation files.

#### NOTE:

```
Many installers (NSIS, MSI, Inno Setup, etc) compress their
payload (the files to be installed) to save space.
```

12. Upon listing all the compressed files using `7z`, found an interesting archive file. The archive itself could indicates a bundled payload compressed for efficiency.
13. `$PLUGINSDIR` is a temporary directory created and used by NSIS when an installer runs. It is used to extract and store temporary files, such as plugins, resources, or payloads required during the installation process.
14. The contents of `$PLUGINSDIR` are typically deleted after the installer finishes running, unless the process is interrupted or the files are explicitly left behind.

> COMMAND

```
7z l nsis-installer.exe
```

![image](https://github.com/user-attachments/assets/525b0cd6-2d24-4cfa-9ca8-825c0515ebe2)



15. It is known there are 2 directories and 72 files within the archive file.

![image](https://github.com/user-attachments/assets/858464d4-4ed6-47c0-97e9-868431c04af0)

16. Noticed there is another archive file with `.asar` extension, the size itself is quite big, which indicate storing important data.

![image](https://github.com/user-attachments/assets/62c2fc3d-abd7-40b3-a855-de72c1d99aa8)

17. Anyway, previously we identified another `.nsi` file which should be our interest beside the 7zip archive file. The `.nsi` file is part of the NullSoft installer, this file has instructions about the installation process of the binary.
18. Knowing this, the unique GUID used by the malware for installation process can be found there. To review it we can simply open it on any text editor.

> RESULT ON NOTEPAD++

![image](https://github.com/user-attachments/assets/78a0f56f-df78-4f62-939a-15e442a71229)


19. It seems, **SerenityThrerapyInstaller** should be our interest.

![image](https://github.com/user-attachments/assets/a9ca6eb5-cd79-4672-a88a-70047ad23398)

20. However noticed there are several keys that reference to GUID `cfbc383d-9aa0-5771-9485-7b806e8442d5`. An uninstall instruction is also reference to the same GUID along with the publisher name stated the **SerenityTherapyInstaller**.
21. For the sake of consistency in registry entries, the GUID associated for the uninstallation is typically the same as the one used during installation.
22. Another reason why it used the same GUID is to avoid conflict with other installations.

![image](https://github.com/user-attachments/assets/b05e39a3-f671-457b-a174-4c96cb25bdd5)


> 4TH QUESTION --> ANS: `ISC`

![image](https://github.com/user-attachments/assets/87cfee9b-69f2-4243-900f-3397b8f18397)


23. Refer back to our previous finding upon unzipping the 7zip archive file, we shall review the `app.asar` file.

![image](https://github.com/user-attachments/assets/226e5fe6-4cbd-40b1-bcc4-c006a5b32f91)

24. Interesting! It seems the malware is using JS utility.
25. Reviewing the **JSON** file, we can identify several metadata associated with the malware and one of them is the license tied to this malware.

![image](https://github.com/user-attachments/assets/4a5a3237-fcf9-4804-9ceb-7e61d37de606)


> 5TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/32b38bf1-d4cf-48a4-b8ee-5d51248508ce)


26. Upon reviewing the Javascript, it is clear that the script is obfuscated and it would take time if we try to conduct static analysis to the JS file.

![image](https://github.com/user-attachments/assets/17f663f7-92b0-4919-b687-dbeb131e2033)

27. So I tried to debug the JS using VSCODE. Anyway don't forget to install all the dependencies we previously identified in order to debug the script. In my case, I just missing both `@primno/dpapi` and `sqlite3` npm modules, if you facing the same problem, here lies the command line to install those two modules.

> Command to install

```sh
npm install @primno/dpapi
npm install sqlite3
```

> Don't forget to beautify the script first, so we can easily fix for syntax error

![image](https://github.com/user-attachments/assets/d79e6d70-9ecf-4931-b1c8-5e2647b85f70)

29. If you face the same syntax problem like me, simply remove the **5** number before **_0**.

> BEFORE

![image](https://github.com/user-attachments/assets/36d607d5-6c03-469d-8143-2422cf374a99)


> AFTER

![image](https://github.com/user-attachments/assets/58476ed9-9d3d-420d-9de4-f8204a97d530)


> 6TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/4fb2fde3-b386-4402-8d00-fa3e71bfd8f4)


> 7TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/8d3f126d-7893-4c2c-bad0-0701b26ee91d)


> 8TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/9191e24b-562f-490a-b4a9-c6fa306cf94a)


> 9TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/cad17c45-bb9a-4d48-a6ed-a3034d6eb855)


> 10TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/7893cb57-ef91-43d4-b3df-5a79a0c81e45)


> 11TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/254bb4b9-423d-4069-a2c8-3c3faa0ca93c)


> 12TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/b8921284-21c9-413f-a332-78432de9550e)


> 13TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/54ed6588-8c39-422f-b6d8-466d6ba9fdc3)



## IMPORTANT LINK(S):

```

```
