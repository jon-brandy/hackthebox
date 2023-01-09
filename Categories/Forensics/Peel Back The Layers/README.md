# Peel Back The Layers
> Write-up author: jon-brandy
## DESCRIPTION:
A well known hacker rival of ours, managed to gain access to our dockehub profile and insert a backdoor to one of our public docker images in order to distribute his malware and fullfil his soul purpose, 
which is to destroy our steampunk robot using his steam malware. 
When we started tracing him back he deleted his backdoor. Can you help us retrieve his backdoor? Docker Image: `steammaintainer/gearrepairimage`
## HINT:
- NONE
## STEPS:
1. Based from the description, let's pull the image using `docker` command.

```
docker pull steammaintainer/gearrepairimage
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211318845-7a3c51af-d55a-4354-81e6-165461a1f2a2.png)


2. Let's save it on a `.tar` file.

```
sudo docker save steammaintainer/gearrepairimage > peel.tar
```

3. Let's untar the `.tar` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211324234-4d1a3c89-fca2-4d8b-ba2f-2e9cb165c8f5.png)


4. Let's jump to this directory first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211324391-cb27da40-a187-461e-bafe-f85676f12a4f.png)


5. Now let's untar the `layer.tar` file, then jump to the extracted directory.
6. Got a binary file.

![image](https://user-images.githubusercontent.com/70703371/211325107-ca6954e1-272e-4c12-a834-e073606c44fd.png)


7. Let's strings it first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211325209-5ad4af99-9a6d-474d-b926-3d53b842bbfd.png)


8. Surprisingly got the flag!

## FLAG

```
HTB{1_r3H4lly_l1kH3_st34mpHunk_r0b0Hts!!!}
```
