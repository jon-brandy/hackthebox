# Persistence
> Write-up author: jon-brandy
## DESCRIPTION:
We're noticing some strange connections from a critical PC that can't be replaced. We've run an AV scan to delete the malicious files and rebooted the box, but the connections get re-established. We've taken a backup of some critical system files, can you help us figure out what's going on?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Check the type of extracted file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211127382-6e86f092-73de-4eac-a5e1-e33e96e3ce38.png)


3. Since it's a `registry file`, let's open the file with **Registry Viewer**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211130333-770da493-06ae-47d3-95c2-9fab51546f61.png)


4. I did a small outsouce about **Persistence - Registry Run Kes** and found out that the key must be stored inside these paths.

![image](https://user-images.githubusercontent.com/70703371/211130524-ae74bb3a-7fd4-4221-87eb-bc748293a81a.png)


5. Now let's open software.

> INSIDE - SOFTWARE

![image](https://user-images.githubusercontent.com/70703371/211130395-746a147c-6512-4a69-ad0b-4335dd4724d4.png)


6. Check inside microsoft.

> INSIDE - MICROSOFT

![image](https://user-images.githubusercontent.com/70703371/211130406-fd9b3b2a-c7d7-4e28-a540-dab38b2d5923.png)


![image](https://user-images.githubusercontent.com/70703371/211130411-ea6066e4-e9c1-4367-944c-12c4df1ed2c5.png)


![image](https://user-images.githubusercontent.com/70703371/211130418-0d94070b-4e44-41e5-8ebb-4fd2071d0243.png)



7. 
