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


7. Since it's windows event log, so we shall open it in windows.
8. Let's check this file first:

![image](https://user-images.githubusercontent.com/70703371/210166891-c5e63040-17ba-46b1-81e1-6cbbb2c485d1.png)


> RESULT - 0 events

![image](https://user-images.githubusercontent.com/70703371/210166895-0a3ec1a3-45bc-4bdc-981d-a70c2c33b00a.png)

9. Try this one:

![image](https://user-images.githubusercontent.com/70703371/210166912-8d584c83-a066-4673-b68d-a41b975a3ad2.png)


> RESULT - 0 events

![image](https://user-images.githubusercontent.com/70703371/210166908-9e573235-5616-47f3-8a8b-bafb5a4f8458.png)


10. Now this one:

![image](https://user-images.githubusercontent.com/70703371/210166932-e7482e68-2897-4aeb-b1e5-90a5be38aa3d.png)


> RESULT - 149 events

![image](https://user-images.githubusercontent.com/70703371/210166928-28ec1767-95a0-451c-a1ee-0a07b08a2f21.png)


11. At eventID 4100 we got a warning.

![image](https://user-images.githubusercontent.com/70703371/210166965-389dce20-197d-4115-8ff1-0cf0c44caa06.png)


12. Looks like there's a htb flag prefix encoded in base64.

![image](https://user-images.githubusercontent.com/70703371/210167001-794c732e-17f1-4d87-bd18-5ac4426d50a0.png)


13. Try to decode that.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210167005-92262860-22bb-475e-8f5a-a9a69ac536c3.png)


14. Got the flag!

## FLAG

```
HTB{8Lu3_734m_F0r3v3R}
```

