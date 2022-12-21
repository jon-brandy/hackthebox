# LoveTok
> Write-up author: jon-brandy
## DESCRIPTION:
True love is tough, and even harder to find. Once the sun has set, the lights close and the bell has rung... you find yourself licking 
your wounds and contemplating human existence. You wish to have somebody important in your life to share the experiences that come with it, the good and the bad. 
This is why we made LoveTok, the brand new service that accurately predicts in the threshold of milliseconds when love will come knockin' (at your door). 
Come and check it out, but don't try to cheat love because love cheats back. 💛

## HINT:
- NONE
## STEPS:
1. Open the host given.

```
http://178.62.88.144:30462/
```

![image](https://user-images.githubusercontent.com/70703371/208852818-eff7e27c-150b-4ef1-b1b9-7f0da03f284c.png)


2. When i clicked `try again`, new date & time displayed.

![image](https://user-images.githubusercontent.com/70703371/208853461-ab996aa8-b721-4125-af5c-c3cb13181231.png)


3. Notice we have `format` parameter.

![image](https://user-images.githubusercontent.com/70703371/208853448-88975e17-dbb5-46a5-bdc3-49d3540a1f92.png)

4. Anyway let's `unzip` the zip file given.

![image](https://user-images.githubusercontent.com/70703371/208854243-710879f2-d77f-40e6-a42f-10856b128208.png)


5. Jump to the extracted folder.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208854373-8d0707b3-beaf-40e2-9d71-87b266095bab.png)


6. Since i don't want to exploit in local, so let's jump to the `challenge` directory to find the source code.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208919382-2ceced11-9573-4aa3-b614-69afdb66ff59.png)


> INDEX.PHP

```php
<?php 
date_default_timezone_set('UTC');
spl_autoload_register(function ($name){
    if (preg_match('/Controller$/', $name))
    {
        $name = "controllers/${name}";
    }
    else if (preg_match('/Model$/', $name))
    {
        $name = "models/${name}";
    }
    include_once "${name}.php";
$router = new Router();
$router->new('GET', '/', 'TimeController@index');
$response = $router->match();
die($response);
```

7. Based from the `index.php` file, i let's open the `controller` directory.
8. Great we found the time controller source.

> TIMECONTROLLER.PHP

```php
<?php
class TimeController
    public function index($router)
    {
        $format = isset($_GET['format']) ? $_GET['format'] : 'r';
        $time = new TimeModel($format);
        return $router->view('index', ['time' => $time->getTime()]);
    }
```

9. Based from it we know that the value of `format` parameter passed to the TimeModel class.
10. Now let's check the `TimeModel.php` file in the **models** directory.


> TIMEMODEL.PHP

```php
<?php
class TimeModel
    public function __construct($format)
    {
        $this->format = addslashes($format);
        [ $d, $h, $m, $s ] = [ rand(1, 6), rand(1, 23), rand(1, 59), rand(1, 69) ];
        $this->prediction = "+${d} day +${h} hour +${m} minute +${s} second";
    }
    public function getTime()
    {
        eval('$time = date("' . $this->format . '", strtotime("' . $this->prediction . '"));');
        return isset($time) ? $time : 'Something went terribly wrong';
    }

```

11. Based from it, we know that the format parameter is sanitized by the `addslashes()` function.
12. The `addslashes()` function add a forward slash in front of these characters:

```
", ', \, NULL BYTE
```

13. At the `getTime()` function we realize that out input is executed inside the `eval()` function. 
14. `eval()` function is a vuln in php, because the attacker can utilize the func to do RCE to get the flag.
15. However, there's an `addslashes()` func, so we can't add the quote and do a system call resulting in RCE.
16. So i did a small outsource about how to bypass the `addslashes()` function.

```
THE LINK
https://www.programmersought.com/article/30723400042/
http://www.securityidiots.com/Web-Pentest/SQL-Injection/addslashes-bypass-sql-injection.html
```

17. When we add `${system("ls")}` as the format value won't do anything, based from the article we 


## LEARNING REFERENCES

```
http://www.securityidiots.com/Web-Pentest/SQL-Injection/addslashes-bypass-sql-injection.html
https://www.programmersought.com/article/30723400042/
```

