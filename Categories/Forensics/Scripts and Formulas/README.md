# Scripts and Formulas
> Write-up author: jon-brandy

## DESCRIPTION:

After the last site UNZ used to rely on for the majority of Vitalium mining ran dry, 
the UNZ hired a local geologist to examine possible sites that were used in the past for secondary mining operations. 
However, after finishing the examinations, and the geologist was ready to hand in his reports, he mysteriously went missing! 
After months, a mysterious invoice regarding his examinations was brought up to the Department. 
Being new to the job, the clerk wasn't aware of the past situation and opened the Invoice. Now all of a sudden, 
the Arodor faction is really close to taking the lead on Vitalium mining! Given some Logs from the Clerk's Computer and the Invoice, 
pinpoint the intrusion methods used and how the Arodor faction gained access!

## HINT:
- NONE

## STEPS:
1. In this challenge we're given few windows event log file, a .lnk file, and a visual basic script file.
2. Checking the properties for .lnk file, it used to create an .exe shortcut.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/644bc255-1a4b-4ccf-9351-d8fedab604f8)

> 1ST QUESTION --> ANS: cscript.exe:calc.exe

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e6e79241-d32b-48aa-986c-68f03cfa4dde)


3. To answer this question, I started by analyzing the `Windows Powershell event log`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dab06316-ad04-46fa-b060-b9500b6383c8)


4. Noticed, there's a **cp** command which indicate a copy attempt.
5. It seems the attacker attempts to copy a file named cscript.exe to another file named calc.exe.
