# misDIRection
> Write-up author: jon-brandy
## DESCRIPTION:
During an assessment of a unix system the HTB team found a suspicious directory. They looked at everything within but couldn't find any files with malicious intent.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next since the extracted directory is hidden, run `ls -a`, then jump to the hidden directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/210123662-5380297f-e73d-4819-9fdb-728cbcddfea7.png)


3. Since there's many directories, we can filter it using `find` to delete all directories which contain no file.

```
find . -type d -empty -delete | to delete.
find . -type d -empty -print | to print all empty directories.
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210123800-3cbd2e86-4993-44a3-80bb-c2ce0fed8a39.png)

4. Now let's traverse every directory.

> 0

![image](https://user-images.githubusercontent.com/70703371/210123818-e3d1ebff-a5a6-4c10-baf7-f32a0f4f65a7.png)


> 1

![image](https://user-images.githubusercontent.com/70703371/210123825-8af981e8-b6bb-4847-9fc2-80a38314389d.png)


5. Hmm.. Confused here, anyway we can list all of it without jump to the directory, simply run `ls -LR`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210123863-ac31e3bb-7dda-4ce9-856d-5b0d90cf7f3d.png)


![image](https://user-images.githubusercontent.com/70703371/210123864-f7e4f42b-ecd4-45e4-a65a-246a9a51e80c.png)


6. Confused here. But maybe the number's here refers to the directory name order. 
7. When i tried to concate the directory name based on their number inside it.
8. Got this string:

```
SFRCe0RJUjNjdEx5XzFuX1BsNDFuX1NpN2V9
```

9. Remember the prefix looks like a `HTB` strings encoded in base64, let's try to decode it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210124004-7ff87022-8424-484d-83f2-94397a543513.png)


10. Got the flag!

## FLAG

```
HTB{DIR3ctLy_1n_Pl41n_Si7e}
```





