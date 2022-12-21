# Debugging Interface
> Write-up author: jon-brandy
## DESCRIPTION:
We accessed the embedded device's asynchronous serial debugging interface while it was operational and captured some messages that were being transmitted over it. 
Can you decode them?

## HINT:
- NONE

## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208967855-4857a086-5c1a-4289-992b-83c4d994f003.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208967911-74fd1183-8749-4802-b019-23bb223c4b5c.png)


3. Since the file's extension is `.sal`. Means we can analyze it using saleae logic analyzer.
4. Now open the file in saleae.
5. Zoom it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208970027-69f2bed7-ef1d-4f2d-960a-9d9e91d503e1.png)


6. Now choose the `analyzer` tab then click the `Async Serial`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208970324-665f33b4-12c4-4acb-b33b-8dbc300d7b5b.png)


7. Click save.
8. We can see that there are many framing errors.

![image](https://user-images.githubusercontent.com/70703371/208970545-641c445d-e5bd-4b7c-a9e3-ea38bd97c3ee.png)

![image](https://user-images.githubusercontent.com/70703371/208970938-dee35f55-5af6-4dbc-b6cb-2542c82ef05e.png)


9. Change the data representation to ASCII.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208971058-9cab0bc8-f740-40c3-aa63-36eb58248939.png)


10. Now let's solve the framing errors.
11. A framing errors occurs when the bit being read is too fast or too slow.
12. If the bits are being read too fast or too slow, the bits will give different values.
13. To fix the errors simply find the each shortest interval.
14. Based from the graph we know that the shortest from each is 32.02 microseconds.
15. Hence to calculate the actual bit rate, we shall use this formula:

```
Actual Bit Rate = 1 / (32.02 * 10^(-6)) -> 31230.480949406621
```

16. Since there's no decimal place in number of bits to read, so we can exclude the decimal number.
17. At the `Async Serial` click edit.
18. Change the bit rate value.

![image](https://user-images.githubusercontent.com/70703371/208973575-74a6ba75-a490-4249-9e62-8253bc12bc5f.png


19. Now click save.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208973645-bc3c5a6b-fa0b-4e4d-aeb0-8c1020a7b5e2.png)


20. Change the data results to terminal.


![image](https://user-images.githubusercontent.com/70703371/208973785-c4f9145c-a617-4191-96d3-a7ceb18f81f4.png)


![image](https://user-images.githubusercontent.com/70703371/208973848-c083ca5d-72c6-40b0-805a-eb875881b00f.png)


21. Got the flag!


## FLAG

```
HTB{d38u991n9_1n732f4c35_c4n_83_f0und_1n_41m057_3v32y_3m83dd3d_d3v1c3!!52}
```

## LEARNING REFERENCES:

```
s/analyzer-user-guid
```
