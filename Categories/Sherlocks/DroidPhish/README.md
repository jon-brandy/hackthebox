# DroidPhish
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/5eb8bcfc-b9c1-4097-9e15-b1b84611c115)


## Lessons Learned:
1. Reviewing android image file using FTK imager and mount it on linux (identify last device boot time).
2. Performing android e-mail and browser forensics (identify phish mail, malicious apk file, and installation timestamp).
3. Performing static analysis on Android APKs (identify runtime permissions and C2 IP address).

## SCENARIO:

<p align="justify">Last night, most employees' mobile devices were compromised, putting them at significant risk of leaking personal and private information. We require your expertise in digital forensics to help investigate this breach.</p>

## STEPS:
1. In

> 1ST QUESTION -> ANS: `2024-11-24 12:05:19`

![image](https://github.com/user-attachments/assets/930df378-b105-433f-9196-94e52575d92a)


> 2ND QUESTION -> ANS: `Proton Mail`

![image](https://github.com/user-attachments/assets/e97d6772-71de-4578-b480-3e25fdccc0e2)


> 3RD QUESTION -> ANS: `Celebrating 3 Years of Success – Thank You!`

![image](https://github.com/user-attachments/assets/30bc8212-dc83-47fb-a503-49ff63e783c6)


> 4TH QUESTION -> ANS: `2024-11-24 17:04:42` 

![image](https://github.com/user-attachments/assets/e8613de0-e392-4e0e-93f1-83572ea3c802)


> 5TH QUESTION -> ANS: `https://provincial-consecutive-lbs-boots.trycloudflare.com/Booking.apk`

![image](https://github.com/user-attachments/assets/b35758b4-6202-4768-87a0-1ee83010a2b0)


> 6TH QUESTION -> ANS: `af081cd26474a6071cde7c6d5bd971e61302fb495abcf317b4a7016bdb98eae2`

![image](https://github.com/user-attachments/assets/178b1359-5927-486f-9fa3-d1fca19b6c59)


> 7TH QUESTION -> ANS: `com.hostel.mount`

![image](https://github.com/user-attachments/assets/f065d9e4-e43f-41ea-8f7b-20944ae09ce3)


> 8TH QUESTION -> ANS: `2024-11-24 17:14:34`

![image](https://github.com/user-attachments/assets/26bb6b4e-b304-4ca2-88f2-ec492cb4a3ee)


> 9TH QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/29a8011e-49ce-4488-93e2-74a3f69cce82)


> 10TH QUESTION -> ANS: `3.121.139.82:10824`

![image](https://github.com/user-attachments/assets/72b79ea6-3904-44a8-99c2-8d8b74c0509e)

