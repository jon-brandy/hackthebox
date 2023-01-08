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


4. These USB packets are keystrokes, there was some vuln that affect USB wireless devices. (keyboard).
5. Let's export all of it as the indicates keystrokes.
6. First we need to filter the USB Keyboard packets. I did a small outsource about the command to use, found out this one:

```
usb.transfer_type == 0x01 and frame.len == 35 and !(usb.capdata == 00:00:00:00:00:00:00:00)
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188537-91b755f9-123c-4151-803f-e7ad3162a635.png)


7. Now select all the packets, then click file -> export specified packets.

> RESULT - give any name, then click save.

![image](https://user-images.githubusercontent.com/70703371/211188583-886df1f1-4190-4372-bb96-478d7397c17c.png)


8. Now to get the flag, i used [this](https://github.com/TeamRocketIst/ctf-usb-keyboard-parser) python script.

> COMMAND - to get the .txt file which we will use for the script.

```
tshark -r ../../../../../Downloads/bin/foren/logger/exported.pcapng -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2' > keystrokes.txt
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188892-1d19c6bd-21de-4a40-ba2c-2445ae223552.png)


9. Following the capslock command, we shall get the flag!

## FLAG

```
HTB{i_C4N_533_yOUr_K3Y2}
```
