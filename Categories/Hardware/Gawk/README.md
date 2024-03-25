# Gawk
> Write-up author: jon-brandy

## Lessons Learned:
- Printer Exploitation.

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
8. 

