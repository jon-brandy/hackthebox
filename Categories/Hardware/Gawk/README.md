# Gawk
> Write-up author: jon-brandy

## Lessons Learned:
- Printer Exploitation.
- Using PRET to communicate with the printer.
- Identifying printer language.

## HINT:
- NONE

## DESCRIPTION:
I lost access to my computer and need a document urgently which got stuck in a printer. Can you get me the document?

## STEPS:
1. In this challenge seems we are tasked to recover a document that got stuck in their printer.
2. Also we're given an instance which we can exploit using **Printer Exploitation Toolkit (PRET)**. It's open source and posted at Github.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7d889e49-90ed-445b-a6af-62c1b4cc82a1)


3. The github documentations also provided with the system operations executeable in every printer language.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/79cfa74f-0f18-4644-ac6f-a217ac79a820)


4. Great! Let's follow the documentations.
5. Using `ps` resulting to no feedback but it connected. It means the printer does not understand the language which also correlates that it's not the correct printer language.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1e2ebe60-b5f5-4aef-8247-eaa7fcc8d355)


6. Using `pjl` shall resulting to the printer feedback!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/48c22af1-4baa-4683-8168-34fb36988006)


7. Noticed that it also provide the device name that we're going to exploit.
8. BUT, somehow we got `watchdog timeout` everytime we want to run `ls` command even though the `ls` command is available.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/632c614b-9c16-4b9b-8683-85e2dfcd2cbb)


9. Possibly because there is a session which has a timeout but does not terminate the shell directly.
10. Running the script again and execute `ls` again, the printer shall reflects the result to the terminal.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37a5db07-baab-4b29-b77e-9abc2c7b2f32)


11. Long story short, after traversing through the directory seems we found the stuck document at `saveDevice/SavedJobs/InProgress` directory.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2f780cd4-6668-4133-bd27-cf93125ab064)


12. To download the document we can use `get` command.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2c26addf-2095-4ee4-acc8-e1d257988b44)


13. Upon attempt to render the PDF we got this result:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2bb9a1d4-c307-4452-a6a8-61dbe009ae93)


14. Interesting, after running a basic file check we found out that it contains base64 text.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0dba387-8a60-4d3a-9c28-0b4d5bfd122c)


15. Let's use cyberchef to decode it and download the content again from there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef39feec-3d50-4eae-af26-89d83eb04ae1)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/572c3e64-1052-49d8-9204-6a66ab4cb7dc)


16. Got the flag!

## FLAG:

```
HTB{tr4v3rs3_m4n4g3ment_d3240!}
```
