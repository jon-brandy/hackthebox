# Event Horizon
> Write-up author: jon-brandy
## DESCRIPTION:
Our CEO's computer was compromised in a phishing attack. The attackers took care to clear the PowerShell logs, so we don't know what they executed. Can you help us?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209458111-64fad8f6-bcc5-4851-a76e-fa72f60ab02d.png)


2. Got 2 directories.
3. Looks like there's nothing in Traceformat directory.

![image](https://user-images.githubusercontent.com/70703371/210166652-2efe495b-b351-46d8-ab34-c66c2e21a2be.png)


4. Hence, all of these 324 files are inside the Logs directory.

![image](https://user-images.githubusercontent.com/70703371/210166679-b96ff294-57ff-422e-a06f-ffb8e4b4cfbf.png)


5. When i checked all the file types. It's MS Windows Vista Event Log.

![image](https://user-images.githubusercontent.com/70703371/210166706-c5e2d357-c979-44e7-aa93-eb17a5758007.png)


6. Based on the description, the attackers clear the PowerShell logs. Let's filter the file listing.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210166786-55d61a5a-50c8-41a4-b1ed-520d10200808.png)


7. 

