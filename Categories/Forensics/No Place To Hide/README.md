# No Place To Hide
> Write-up author: jon-brandy
## DESCRIPTION:
We found evidence of a password spray attack against the Domain Controller, and identified a suspicious RDP session. We'll provide you with our RDP logs and other files. Can you see what they were up to?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210036188-251c3814-ce9e-4844-b5b3-88c9ea7f6ebb.png)


![image](https://user-images.githubusercontent.com/70703371/210036198-17f35529-93c2-471a-8994-4a2f0d0d5d94.png)


2. Let's strings the `.bmc` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210036284-5d7c6be9-c1a9-42f7-bf50-74d654a14fd2.png)


3. Hmm.. Let's open the other file using hexedit.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210036391-d917a325-fb00-480d-80bb-1fe0b20850ca.png)


4. 
