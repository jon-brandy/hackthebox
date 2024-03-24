# SpookTastic
> Write-up author: jon-brandy

## Lessons Learned:
- Source code review.


## DESCRIPTION:
On a moonless night, you delve into the dark web to uncover the hacker group "The Cryptic Shadows." 
You find an encrypted message guiding you to a web challenge. They claim a cursed amulet, the 'Amulet of Samhain,' can unveil their treasures location

## HINT:
- NONE

## STEPS:
1. In this challenge, the source codes are disclosed.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/20ea6c64-b255-4e73-9505-dfb34f619e8c)


2. Upon checking the functionalities in the webapp, found no other endpoints or features which is interesting.
3. But the webapp seems accept user input from the **Newsletter** section.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/adf7d9fc-f6e6-4318-8c8c-a6cac7f8f599)


4. Let's review the source code at the **Newsletter** section.
5. Noticed the "Book Now" button shall executes --> `javascript:void()` every time users click the button to submit their input.
6. BUT, there is a certain condition to trigger this, because there is no direct calls for this function.
7. Reviewing the `app.py` script, found LOC that reflect the flag to the user desktop if an alert is happen.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/68e47fa6-c8f2-4fec-9ffe-ea0bf4ac9084)


8. Great! Let's just send simple XSS payload then.
9. I start by sending `<script>alert('1')</script>` but nothing happened.
10. Seems the webapp filters it.
