## Waf  绕过



### 一、什么是waf？

先上波百度介绍
WAF(Web应用防火墙，Web Application Firewall的简称)是通过执行一系列针对HTTP/HTTPS的安全策略来专门为Web应用提供保护的产品。WAF可以发现和拦截各类Web层面的攻击，记录攻击日志，实时预警提醒，在Web应用本身存在缺陷的情况下保障其安全。 但是，WAF不是万能的、完美的、无懈可击的，在种种原因下，它们也会有各自的缺陷，作为用户不可以盲目相信WAF而不注重自身的安全。

### 二、攻击者可利用哪些方面来绕过WAF？

1、 Web容器的特性
2、 Web应用层的问题
3、 WAF自身的问题（本次LIVE重点）
4、 数据库的一些特性
先说一下web容器的特性

#### 1、IIS+ASP的神奇%

在IIS+ASP的环境中，对于URL请求的参数值中的%，如果和后面的字符构成的字符串在URL编码表之外，ASP脚本处理时会将其忽略。
例： 现在假设有如下请求：
http://www.test.com/1.asp?id=1 union all se%lect 1,2,3,4 fro%m adm%in 在WAF层，获取到的id参数值为1 union all se%lect 1,2,3,4 fro%m adm%in，此时waf因为%的分隔，无法检测出关键字 select from等
但是因为IIS的特性，id获取的实际参数就变为1 union all select 1,2,3,4 from admin，从而绕过了waf。 这个特性仅在iis+asp上 asp.net并不存在

#### 2、IIS的unicode编码字符

IIS支持Unicode编码字符的解析，但是某些WAF却不一定具备这种能力。 例： 已知 's' 的unicode编码为：%u0053, 'f' 的unicode编码为%u0066)
http://www.test.com/1.asp?id=1 union all %u0053elect 1,2,3,4 %u0066rom admin
在WAF层，获取到的id参数值为1 union all %u0053elect 1,2,3,4 %u0066rom admin
但是IIS后端检测到了Unicode编码会将其自动解码，脚本引擎和数据库引擎最终获取到的参数会是：1 union all select 1,2,3,4 from admin
此方法还存在另外一种情况，多个不同的widechar可能会被转换为同一个字符
(http://blog.sina.com.cn/s/blog_85e506df0102vo9s.html WideChar和MultiByte字符转换问题)
s%u0065lect->select
s%u00f0lect->select
这种情况需要根据不同的waf进行相应的测试，并不是百发百中。但是对于绕过来说，往往只要一个字符成功绕过即可达到目的。

#### 3、HPP：HTTP参数污染

在HTTP协议中是允许同样名称的参数出现多次的。例如：http://www.test.com/1.asp?id=123&id=456 根据WAF的不同，一般会同时分开检查id=123和id=456，也有的仅可能取其中一个进行检测。但是对于IIS+ASP/ASP.NET来说，它最终获取到的ID参数的值是123,空格456(asp)或123,456(asp.net)。
所以对于这类过滤规则，攻击者可以通过：
id=union+select+password/&id=/from+admin
来逃避对select * from的检测。因为HPP特性，id的参数值最终会变为：
union select password/,/from admin
所以对于这类过滤规则，攻击者可以通过：
id=union+select+password/&id=/from+admin
来逃避对select * from的检测。因为HPP特性，id的参数值最终会变为：
union select password/,/from admin>>>>>union select password from admin

#### 4、畸形HTTP请求

当向web服务器发送畸形的，非RFC2616标准的HTTP请求时。web服务器出于兼通的目的，会尽可能解析畸形的HTTP请求。而如果Web服务器的兼容方式与waf不一致，则可能会出现绕过的情况。
例：一个正常的post请求 POST /id.php?id=1%20union//select HTTP/1.1 HOST:[www.test.com](http://www.test.com/) Content-Type: application/x-www-form-urlencoded Accept: text/html,application/xhtm+xml,application/xml;q=0.9,image/webp,/;q=0.8 如果将请求改为 PAXX /id.php?id=1%20union//select Content-Type: application/x-www-form-urlencoded Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8
这个请求包就变成了：Method不合法，没有协议字段HTTP/1.1,也没有Host字段，如果在HTTP/1.1协议中，缺少了HOST字段会返回400 bad request ，但是当某些版本的Apache在处理这个请求时，默认会设置协议为HTTP/0.9,Host则默认使用Apache默认的servername，这种畸形的请求仍然能够被处理 如果某些WAF在处理数据时候严格按照GET
POST方式来获取数据，或者通过正则来处理数据包，就会因为某些版本的Apache宽松的请求方式而被绕过

### 三、应用层的问题

#### 1、多重编码问题

如果Web应用程序能够接收多重编码的数据，而WAF只能解码一层(或少于WEB应用程序能接收的层数)时，WAF会因为解码不完全导致防御机制被绕过
例如：request： [http://www.test.com/1.asp?id=123%2520and%2520=1](http://www.test.com/1.asp?id=123%20and%20=1) 一重URL编码：%25>>%>>>id=123%20and%201=1 二重URL编码：%20>>空格>>>id=123 and 1=1

#### 2、多数据来源问题

如Asp和Asp.NET中的Request对象对于请求数据包的解析过于宽松，没有依照RFC的标准来，开发人员在编写代码时如果使用如下方式接收用户传入的参数
ID=Request("ID") >>asp ID=Request.Params("ID") >>asp.net
WEB程序可从以下3种途径获取到参数ID的参数值：
1.从GET请求中获取ID的参数值；
2.如果GET请求中没有ID参数，尝试从POST的ID参数中获取参数值；
3.如果GET和POST中都获取不到ID的参数值，那么从Cookies中的ID参数获取参数值。
这样对于某些WAF来说，如果仅检查了GET或POST的，那么来自Cookie的注入攻击就无能为力了，更何况来自于这三种方式组合而成的参数污染的绕过方法呢？
例如： 请求内容为： POST /test.aspx?id=123 HTTP/1.1 Host: 192.168.118.128:8080 Accept: / Accept-Language: en User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0) Connection: close Content-Type: application/x-www-form-urlencoded Content-Length: 6 Cookie:id=789
id=456 返回内容为： HTTP/1.1 200 OK Cache-Control: private Connection: close Date: Sat, 22 Sep 2018 07:51:23 GMT Content-Length: 11 Content-Type: text/html; charset=utf-8 Server: Microsoft-IIS/6.0 X-Powered-By: ASP.NET Set-Cookie: yunsuo_session_verify=44fb70a14c10485884a32dfec98a4982; expires=Tue, 25-Sep-18 15:51:23 GMT; path=/; HttpOnly X-AspNet-Version: 2.0.50727
123,456,789
可以看到 id参数值的取值顺序

### 四、WAF自身的问题(重点）

#### 1、白名单机制

WAF存在某些机制，不处理和拦截白名单中的请求数据：
1、指定IP或IP段的数据。
2、来自于搜索引擎爬虫的访问数据。
3、其他特征的数据。
如以前某些WAF为了不影响站点的SEO优化，将User-Agent为某些搜索引擎（如谷歌）的请求当作白名单处理，不检测和拦截。伪造HTTP请求的User-Agent非常容易，只需要将HTTP请求包中的User-Agent修改为谷歌搜索引擎的User-Agent即可畅通无阻。

#### 2、数据获取方式存在缺陷

某些WAF无法全面支持GET、POST、Cookie等各类请求包的检测，当GET请求的攻击数据包无法绕过时，转换成POST可能就绕过去了。或者，POST以Content-Type: application/x-www-form-urlencoded无法绕过时，转换成上传包格式的Content-Type: multipart/form-data就能够绕过去。
某些WAF无法全面支持GET、POST、Cookie等各类请求包的检测，当GET请求的攻击数据包无法绕过时，转换成POST可能就绕过去了。或者，POST以Content-Type: application/x-www-form-urlencoded无法绕过时，转换成上传包格式的Content-Type: multipart/form-data就能够绕过去。
某些WAF从数据包中提取检测特征的方式存在缺陷，如正则表达式不完善，某些攻击数据因为某些干扰字符的存在而无法被提取，常见的如%0a、%0b、%0c、%0d、%09、%0a等。
在以前，针对某些WAF，直接使用以上字符就可以直接绕过。当然，现在不太可能了。

#### 3、数据处理不恰当

1、%00截断
将%00进行URL解码，即是C语言中的NULL字符 如果WAF对获取到的数据存储和处理不当，那么%00解码后会将后面的数据截断，造成后面的数据没有经过检测。 例如： request http://www.test.com/1.asp?id=1/*%00*/union+select+1,2,3 URL解码：%00>>NULL http://www.test.com/1.asp?id=1/*%00*/union+select+1,2,3
id=1/ WAF在获取到参数id的值并解码后，参数值将被截断成1/，后面的攻击语句将没有被WAF拿去进行检测
2、字符处理
某些WAF在对HTTP请求数据包中的参数进行检测时，使用&字符对多个参数进行分割，然后分别进行检测，如： http://test.com/id.php?par1=1&par2=2&par3=3 这些WAF会使用&符号分割par1、par2 和par3，然后对其参数进行检测，但是，如果是以下的构造 http://test.com/id.php?par1=1+union+/*%26x=1*/+select/*%26x2=1*/1,2,3,4,5+from+Admin 注：这里的%26是&字符 /%26/->/&/ 其实只是一个SQL的注释而已 WAF会将上述的参数分割成以下部分： par1=1+union+/ x=1/+select/ x2=1/1,2,3,4,5+from+Admin 如果将这3个参数分别进行检测，某些WAF是匹配不到攻击特征的。

#### 4、数据清洗不恰当

当攻击者提交的参数值中存在大量干扰数据时，如大量空格、TAB、换行、%0c、注释等，WAF需要对其进行清洗，筛选出真实的攻击数据进行检测，以提高检查性能，节省资源。 如果WAF对数据的清洗不恰当，会导致真实的攻击数据被清洗，剩余的数据无法被检测出攻击行为。

#### 5、通用型WAF

通用型的WAF，一般无法获知后端使用的是哪些WEB容器、什么数据库、以及使用的什么脚本语言。 每一种WEB容器、数据库以及编程语言，它们都有自己的特性，想使用通用的WAF规则去匹配和拦截，是非常难的。 通用型WAF在考虑到它们一些共性的同时，也必须兼顾它们的特性，否则就很容易被一些特性给Bypass！

#### 6、为性能和业务妥协

要全面兼容各类Web Server及各类数据库的WAF是非常难的，为了普适性，需要放宽一些检查条件，暴力的过滤方式会影响业务。 对于通用性较强的软WAF来说，不得不考虑到各种机器和系系统的性能，故对于一些超大数据包、超长数据可能会跳过不检测。 然后是数据库的一些特性，不同的数据库有一些属于自己的特性，WAF如果不能处理好这些特性，就会出很大的问题。
总结一下，WAF自身的问题有：
白名单机制
数据获取方式存在缺陷
数据处理不恰当
数据清洗不恰当
规则通用性问题
为性能和业务妥协