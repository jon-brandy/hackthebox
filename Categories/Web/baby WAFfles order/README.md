# baby WAFfles order
> Write-up author: jon-brandy
## DESCRIPTION:
Our WAFfles and ice scream are out of this world, come to our online WAFfles house and check out our super secure ordering system API!
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209812644-460c5cf9-48be-4ec2-9dd1-a6a288c16413.png)


2. Let's try to order `ICE SCREAM` for table number 1.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209812736-cb17542c-46d5-4f95-90fc-e714f2aaa87d.png)

3. Actually didn't see any change.
4. Notice the web's title named `xxe`. Hence we may do XML injection (?)
5. Let's use burpsuite to play with the request.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209816372-983772e8-3c64-40bd-9d96-a876a8cc8a20.png)


6. Let's try to order "ice scream" for table 1, and open the request in burpsuite.

![image](https://user-images.githubusercontent.com/70703371/209816516-daa9fbb5-c706-4c4e-9114-3240b4fa04c5.png)


7. Now send the request to **repeater**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209816595-ef35fc14-8115-4668-b088-344d82fe8156.png)


8. I used a payload from [this](https://github.com/payloadbox/xxe-injection-payload-list) online cheatsheet.


## LEARNING REFERENCES:

```
https://github.com/payloadbox/xxe-injection-payload-list
```
