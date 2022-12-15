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
1. First, unzip the file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207777216-c27ab91f-d18a-4300-b02f-70b716d25b30.png)


2. Jump the extracted folder.

![image](https://user-images.githubusercontent.com/70703371/207777280-2282bbf5-a6c9-41bd-a5d4-6148af472705.png)


3. Let's `strings` the imageinfo.txt file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207777675-41520362-973a-4cdd-9326-bad0f00c3130.png)


4. I think it provides information on flounder-pc-memdump.elf memory file. Now Strings the `.eml` file.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/207778293-376ada2c-1d4e-4dc1-93fd-b0cd0016ae10.png)


5. It looks like there's a `.zip` file?

![image](https://user-images.githubusercontent.com/70703371/207778361-c0075d3a-bdb2-4537-bf2f-509f0ff784ad.png)


6. I
