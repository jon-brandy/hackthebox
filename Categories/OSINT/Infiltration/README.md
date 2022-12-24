# Infiltration
> Write-up author: jon-brandy
## DESCRIPTION:
Can you find something to help you break into the company 'Evil Corp LLC'. Recon social media sites to see if you can find any useful information.
## HINT:
- NONE
## STEPS:
1. Based from the description, let's google `Evil Corp LLC`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209418064-5d589ded-be28-41ec-871c-af8bb82a132c.png)


2. We found the LinkedIn.
3. On their profile looks like there's A `base64` encoding text, let's decode it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209418084-abd52370-5517-4c20-a73d-7975df74c43c.png)


4. When i tried to submit the flag, it says the flag is incorrect.
5. At the **about** tab, i found their website's link, let's jump there.

![image](https://user-images.githubusercontent.com/70703371/209418211-e8516b6a-bd30-4af7-9d25-74894574a041.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/209418300-ea343916-4a49-4114-b95f-e20ef8257da8.png)


6. I tried to check one of the machine, but i think it's not the right way (?)

![image](https://user-images.githubusercontent.com/70703371/209418287-953ddc66-ea2b-44ee-86ae-d0cfe532b481.png)


7. So i go back the the LinkedIn page.
8. Let's check all the employees that are working on this company.

![image](https://user-images.githubusercontent.com/70703371/209418370-b2b23fb2-c9f5-43ac-b2e3-c739278b380a.png)


9. When i tried to check a profile with `LinkedIn member` as the username, i got this message.

![image](https://user-images.githubusercontent.com/70703371/209418411-8a01c3c5-c11c-44b2-8648-5aa31961de4f.png)


10. So i googled again `Evil Corp LLC`.
11. And got this instagram page.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209418533-737b287a-81de-4a23-9658-a36826c6a88d.png)


12. After checked every post, every comments.
13. Finally got a post that shows the flag.

![image](https://user-images.githubusercontent.com/70703371/209418547-3ff3a335-6b55-494b-a6b3-d3b1b3549671.png)


14. Got the flag!

## FLAG

```
HTB{Y0ur_Enum3rat10n_1s_Str0ng_Y0ung_0ne}
```
