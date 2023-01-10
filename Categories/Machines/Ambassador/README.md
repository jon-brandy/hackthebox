# Ambassador
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, scan all open ports and it's services from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211477599-52565279-a5b7-4e19-917b-cd9cf6a6a856.png)


![image](https://user-images.githubusercontent.com/70703371/211477638-9256b39b-f97a-4797-affe-af64c8501495.png)


![image](https://user-images.githubusercontent.com/70703371/211477673-74d0d4bd-85d3-4604-8ad8-290c18b327e8.png)


![image](https://user-images.githubusercontent.com/70703371/211477703-b27865b7-f113-49b6-ab70-b3b31a9babf8.png)


![image](https://user-images.githubusercontent.com/70703371/211477725-b2d8e93a-07a0-4137-9097-aeac6e8562e5.png)


2. Based from the output we know that the machine is running a web application, hence let's open it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211477897-0232551b-9ed1-435c-b32b-3513f2f6b540.png)


![image](https://user-images.githubusercontent.com/70703371/211477967-7beb1d95-b90d-48e8-9e2a-9d25744803b7.png)


3. Remember there's port `3000` with `ppp?` as it's service.

![image](https://user-images.githubusercontent.com/70703371/211479120-a0330dac-c1db-4076-88dc-c7128d2c3d01.png)


4. Based from it's info, it opens a login page.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211479182-3b461ea9-f0ec-46af-9f5e-2547d74e817a.png)


5. I did a small outsource about grafana and found CVE about [grafana exploit](https://github.com/pedrohavay/exploit-grafana-CVE-2021-43798).

6. Let's use the script from the github documentation.

> RESULT

