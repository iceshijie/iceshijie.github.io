







### 从CTF中学PHP

#### 超全局变量

##### 超全局变量 ***GLOBALS***

$GLOBALS的作用：引用***全局作用域中可用的全部变量***。可以在函数内调用函数外定义的全局变量
这样就会打印出当前定义的**所有变量**，也包括 include 的文件中的变量，flag 也存在在这些变量中。

```
<?php 
include "flag.php";
$a = @$_REQUEST['hello'];
if(!preg_match('/^\w*$/',$a )){//正则表达式^匹配一行的开头，$表示结束。\w表示匹配包括下划线的任何单词字符，等价于'[A-Za-z0-9_]'。*号：匹配前面的子表达式零次或多次。
  die('ERROR');
}
eval("var_dump($$a);");//var_dump — 打印变量的相关信息
show_source(__FILE__);//__FILE__当前运行文件的完整路径和文件名。
?>
```



------



#####  $_SERVER 变量

$_SERVER 这种超全局变量保存关于报头、路径和脚本位置的信息。

| 元素/代码                       | 描述                                                         |
| :------------------------------ | :----------------------------------------------------------- |
| $_SERVER['PHP_SELF']            | 返回当前执行脚本的文件名。                                   |
| $_SERVER['GATEWAY_INTERFACE']   | 返回服务器使用的 CGI 规范的版本。                            |
| $_SERVER['SERVER_ADDR']         | 返回当前运行脚本所在的服务器的 IP 地址。                     |
| $_SERVER['SERVER_NAME']         | 返回当前运行脚本所在的服务器的主机名（比如 www.w3school.com.cn）。 |
| $_SERVER['SERVER_SOFTWARE']     | 返回服务器标识字符串（比如 Apache/2.2.24）。                 |
| $_SERVER['SERVER_PROTOCOL']     | 返回请求页面时通信协议的名称和版本（例如，“HTTP/1.0”）。     |
| $_SERVER['REQUEST_METHOD']      | 返回访问页面使用的请求方法（例如 POST）。                    |
| $_SERVER['REQUEST_TIME']        | 返回请求开始时的时间戳（例如 1577687494）。                  |
| $_SERVER['QUERY_STRING']        | 返回查询字符串，如果是通过查询字符串访问此页面。             |
| $_SERVER['HTTP_ACCEPT']         | 返回来自当前请求的请求头。                                   |
| $_SERVER['HTTP_ACCEPT_CHARSET'] | 返回来自当前请求的 Accept_Charset 头（ 例如 utf-8,ISO-8859-1） |
| $_SERVER['HTTP_HOST']           | 返回来自当前请求的 Host 头。                                 |
| $_SERVER['HTTP_REFERER']        | 返回当前页面的完整 URL（不可靠，因为不是所有用户代理都支持）。 |
| $_SERVER['HTTPS']               | 是否通过安全 HTTP 协议查询脚本。                             |
| $_SERVER['REMOTE_ADDR']         | 返回浏览当前页面的用户的 IP 地址。                           |
| $_SERVER['REMOTE_HOST']         | 返回浏览当前页面的用户的主机名。                             |
| $_SERVER['REMOTE_PORT']         | 返回用户机器上连接到 Web 服务器所使用的端口号。              |
| $_SERVER['SCRIPT_FILENAME']     | 返回当前执行脚本的绝对路径。                                 |
| $_SERVER['SERVER_ADMIN']        | 该值指明了 Apache 服务器配置文件中的 SERVER_ADMIN 参数。     |
| $_SERVER['SERVER_PORT']         | Web 服务器使用的端口。默认值为 “80”。                        |
| $_SERVER['SERVER_SIGNATURE']    | 返回服务器版本和虚拟主机名。                                 |
| $_SERVER['PATH_TRANSLATED']     | 当前脚本所在文件系统（非文档根目录）的基本路径。             |
| $_SERVER['SCRIPT_NAME']         | 返回当前脚本的路径。                                         |
| $_SERVER['SCRIPT_URI']          | 返回当前页面的 URI。                                         |

代码示例

```
<!DOCTYPE html>
<html>
<body>

<?php 
echo $_SERVER['PHP_SELF'];
echo "<br>";
echo $_SERVER['SERVER_NAME'];
echo "<br>";
echo $_SERVER['HTTP_HOST'];
echo "<br>";
echo $_SERVER['HTTP_REFERER'];
echo "<br>";
echo $_SERVER['HTTP_USER_AGENT'];
echo "<br>";
echo $_SERVER['SCRIPT_NAME'];
?>

</body>
</html>

```



结果

```
/example/php/demo_php_global_server.php
www.w3school.com.cn
www.w3school.com.cn
https://www.w3school.com.cn/tiy/s.asp?f=demo_php_global_server
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
/example/php/demo_php_global_server.php
```



-------

#### 解析参数

##### parse_url 解析URL，返回组成部分

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

用法

```
<?php
$url = '//www.example.com/path?googleguy=googley';

// 在 5.4.7 之前这会输出路径 "//www.example.com/path"
var_dump(parse_url($url));
?> 


```

以上例程会输出：

```
array(3) {
  ["host"]=>
  string(15) "www.example.com"
  ["path"]=>
  string(5) "/path"
  ["query"]=>
  string(17) "googleguy=googley"
}
```







-------







#### 功能性参数

##### Static 保留局部变量功能

当一个函数完成时，它的所有变量通常都会被删除。然而，有时候您希望某个局部变量不要被删除。

```
<?php
function myTest()
{
    static $x=0;  //每次调用该函数时，该变量将会保留着函数前一次被调用时的值。
    echo $x;
    $x++;
    echo PHP_EOL;    // 换行符
}
 
myTest();
myTest();
myTest();
?>
```

##### preg_match 参数匹配正则表达式

```
preg_match('/^\w*$/',$a )  //匹配变量$a中的任意字符
```





#### 读文件

##### file()

file — 把整个文件读入一个数组中

file('test.php')

```
<?php 
$a = file('test.php');
var_dump($a);  
?>

输出结果
array(4) {
  [0]=>
  string(8) "<?php 
"
  [1]=>
  string(24) "$a = file('test.php');
"
  [2]=>
  string(17) "var_dump($a);  
"
  [3]=>
  string(2) "?>"
}

```



##### file_get_contents('test.php');

```
<?php 
$a = file_get_contents('test.php');
var_dump($a);  
?>
输出结果
string(64) "<?php 
$a = file_get_contents('test.php');
var_dump($a);  
?>"
```

