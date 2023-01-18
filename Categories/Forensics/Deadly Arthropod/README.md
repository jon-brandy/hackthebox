# Deadly Arthropod
> Write-up author: jon-brandy
## DESCRIPTION:
Our operatives have intercepted critical information. Origin? Classified.
Objective: Retrieve the flag!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then open the `.pcap` file we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/213171300-d3af188e-096d-4139-ae73-86bb08451e65.png)



2. Based on the protocol we have here, it seems the chall related to **USB keystroke reconstruction**. Actually already done chall similiar to this and the filter command is template.
3. Let's use this:

```
usb.transfer_type == 0x01 and frame.len == 35 and !(usb.capdata == 00:00:00:00:00:00:00:00)
```

4. Got an HID data, inside **HID** data is a leftover capture data.

![image](https://user-images.githubusercontent.com/70703371/213171236-b843b086-ccf5-4b31-b0ce-277db883eb9a.png)


6. I did a small outsource about this chall and found [this](https://blog.stayontarget.org/2019/03/decoding-mixed-case-usb-keystrokes-from.html) documentation.
7. Let's follow what they did, hence let's export the packets dissections as `.csv` file.

> RESULT



