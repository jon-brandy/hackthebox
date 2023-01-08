# Logger
> Write-up author: jon-brandy
## DESCRIPTION:
A client reported that a PC might have been infected, as it's running slow. 
We've collected all the evidence from the suspect workstation, and found a suspicious trace of USB traffic. Can you identify the compromised data?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211186757-d132606b-00c4-43b7-b1fe-54693aeda94c.png)


2. Since it's a `.pcap` file, let's open it using wireshark.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211186800-6cb497ee-ee85-43d7-a522-5d52f0cab23a.png)


3. Notice there are many `URB_INTERRUPT` packets.

![image](https://user-images.githubusercontent.com/70703371/211187630-862ddb35-c4ce-4c8e-8d65-aa6b84885f7a.png)


4. These USB packets are keystrokes, there was some vuln that affect USB wireless devices. (Wireless mouse, keyboard, etc.).
5. Let's export all of it as the indicates keystrokes.
