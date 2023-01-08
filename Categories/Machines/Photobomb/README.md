# Photobomb
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's check all open ports and it's services from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187399-28b9242d-ad0b-4fb0-a255-eb0e7fe46ab4.png)


2. Based from the output, it seems the machine is running a web application.
3. So let's open the webapp.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187862-a8c8ee89-b456-4a0f-b1e8-43125353176c.png)


4. Let's click this:

![image](https://user-images.githubusercontent.com/70703371/211187884-27fe79c0-97d4-49d5-a55e-2db4a2b69d93.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187889-bde4bf7a-a15d-48ae-b340-7de1102c675f.png)


5. Well we don't have any creds, let's check the page source.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187961-98e9ad44-061e-4e4a-8178-48a0d3539c74.png)


6. Let's check the `.js` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187975-b432a7ef-7a85-4c03-b159-f511c4b6ec43.png)


![image](https://user-images.githubusercontent.com/70703371/211187993-b6eb2ef8-7633-4800-b00e-3154f28bb366.png)



7. Got a hint there, open the link then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188002-03f41d74-a975-4068-b9de-a3ac4f030445.png)


![image](https://user-images.githubusercontent.com/70703371/211188016-93639302-051f-45b5-a030-7d96ee78947e.png)


8. It seems we can downlaod any image we click here.

![image](https://user-images.githubusercontent.com/70703371/211188145-a76d347c-4916-4e46-8bbb-cf96c3c260ea.png)


9. Hence, let's see the download request using burpsuite.

> RESULT




