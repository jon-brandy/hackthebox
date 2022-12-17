# Cat
> Write-up author: jon-brandy
## DESCRIPTION:
Easy leaks
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208221674-f8857aa2-f6fe-49f7-81fc-6099cb30b9f2.png)


2. Check the file type.

![image](https://user-images.githubusercontent.com/70703371/208221703-5ae08cea-d6be-431c-8e44-92b83ad319bc.png)


3. Since it's an android backup file, we can extract it using **abp** or android-backup-processor.

> RESULT

```
java -jar abp.jar unpack cat.ab cat.rar
```

![image](https://user-images.githubusercontent.com/70703371/208222426-66928def-3416-406a-9432-bb749e46ff8c.png)

4. Extract the `.rar` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208222539-a510854b-4288-450a-9067-b6991d451c48.png)


![image](https://user-images.githubusercontent.com/70703371/208222548-8af92c8b-42a8-40bb-ba7b-d182155fa2f3.png)


5. We got 2 new folders.
6. Let's jump to `shared`.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/208222577-a2e2e0fc-9c98-4530-916c-f1b9b18e709d.png)

> JUMP TO 0

![image](https://user-images.githubusercontent.com/70703371/208222669-1fd97442-d3ae-4343-a119-fe50810d94f9.png)



