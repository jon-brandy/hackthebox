# baby todo or not todo
> Write-up author: jon-brandy
## DESCRIPTION:
I'm so done with these bloody HR solutions coming from those bloody HR specialists, I don't need anyone monitoring my thoughts, or do I... ?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209808749-b7db813e-4d56-40f4-a3b3-691f917f0cfc.png)

2. Let's try to input `<script>alert('1')</script>` to the textbox.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209809664-c7253e8e-0156-491a-9627-61ea8964476b.png)


3. Hmm let's analyze `index.html` then.
4. Something caught my attention.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209810813-612fd0e2-f293-46ea-b9ce-f95dc16de4c2.png)


5. Let's try to run `getstatus('all')` at the webapps's console then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209811017-73a7dd20-1c67-453f-97b6-4690d97bfa72.png)


6. Hmm.. Let's run setInterval(update,3000) then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209811393-01ffb9fe-041e-4dac-9c30-6b814fd6d467.png)


7. Nothing happens.
8. Let's try `setInterval(getTasks('userce6aB01E'), 3000)`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209811532-19802c31-40b9-4f23-9abc-50eab47246cf.png)


9. Again nothing happen, i tried to change the parameter of getTasks to `all`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209811682-5e1925df-ab83-4f26-b05c-54919e5f4e49.png)


10. Nice, looks like we can see the flag there.
11. But since it closed too fast, let's use burpsuite to catch request, then send the request to repeater.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209812173-c5eda10d-9ae6-4110-99a1-7fb2e08f5154.png)


12. Got the flag!

## FLAG

```
HTB{l3ss_ch0r3s_m0r3_h4ck1ng...right?!!1}
```
