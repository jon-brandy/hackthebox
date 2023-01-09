# Reminiscent
> Write-up author: jon-brandy
## DESCRIPTION:
Suspicious traffic was detected from a recruiter's virtual PC. 
A memory dump of the offending VM was captured before it was removed from the network for imaging and analysis. 
Our recruiter mentioned he received an email from someone regarding their resume. 
A copy of the email was recovered and is provided for reference. Find and decode the source of the malware to find the flag.

## HINT:
- NONE

## STEPS:
1. First, unzip the file given and jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211340551-ec70bb4f-1baa-40f7-ac08-1152a28d3c6b.png)


2. Based from the `imageinfo.txt` file , we know the suggested profile is **Win7SP1x64**.

![image](https://user-images.githubusercontent.com/70703371/211341060-34e7aca9-d816-4262-9a39-95bc68f0e694.png)


3. Based from the `.eml` file, we can assume there's might be a resume file inside the memory, let's check it then.

```
volatility -f flounder-pc-memdump.elf --profile=Win7SP1x64 filescan | grep resume
```

![image](https://user-images.githubusercontent.com/70703371/211341178-572bf843-78f7-4e25-aa0f-d923242cb12d.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/211341513-47bf97f3-6664-4f2d-9cf8-e0c0f0257c5e.png)


4. The 2nd one seems shall be our interest, let's extract that to a directory (make the dir first).

```
volatility -f flounder-pc-memdump.elf --profile=Win7SP1x64 dumpfiles --physoffset 0x000000001e8feb70 --dump-dir dumpedMemory
```

5. Now jump to the directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211342572-0e65b01a-a561-44b1-9f84-1b40708ad83f.png)



6. Let's cat the first file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211342945-5a52cf48-56ad-45fe-9cd8-a6356d29d68d.png)


7. Looks like there's an encoded base64 strings, let's decode that.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211345245-aa45374c-dfcd-4f31-8306-abb2c6d24d8d.png)


8. I tried several things to decode the next one, until i got the flag when i used `echo -n`.

![image](https://user-images.githubusercontent.com/70703371/211346055-39c023fa-f642-4e6c-9a1e-ffefca48291c.png)


9. Got the flag

```
HTB{$_j0G_y0uR_M3m0rY_$}
```




