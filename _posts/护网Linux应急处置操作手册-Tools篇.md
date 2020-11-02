## 护网Linux应急处置操作手册-Tools篇

原创 PINGX [BugFor安全团队](javascript:void(0);) *今天*

不点蓝字，哪学姿势？







![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)





前言



**HVV行动已经进行到了11天，处置的工作明显增多，随着各种情况发生，所以这两天分别整理一些关于Linux和Windows的排查手册。**



**昨天收集了关于Linux的应急响应排查处置手册，里面内容我认为还是比较详细的，对于所在单位安全制度不允许down文件下来，且又不能upfile排查辅助工具的单位是实用的。**



**但是今天的，是****针对那些制度上允许在问题主机上传辅助排查工具的单位****。在这里，作为BUGFOR团队的颜值担当，接着昨天的文章继续推荐两款本人在用的排查工具。**



**Tools：**

  **Gscan and LinuxEmergency**

  





**一.Tools**

0

a





Gscan



本程序旨在为安全应急响应人员对Linux主机排查时提供便利

实现主机侧Checklist的自动全面化检测

根据检测结果自动数据聚合，进行黑客攻击路径溯源。



**⚠️文章中部段落位置有运行截图****可以先看运行截图然后回到开头阅读**

**
**

a





LinuxEmergency



Linux下的应急工具，支持CentOS系统和RedHat系统。





学会Linux应急新操作





***Part. 1. Gscan***





**【Github、部署和执行】
**

- 
- 
- 

```
git clone https://github.com/grayddq/GScan.gitcd /GSscanpython2 Gscan.py
```



**【CheckList检测项-****自动化程序的CheckList项如下：】**

**
**

```
1、主机信息获取
2、系统初始化alias检查
3、文件类安全扫描
  3.1、系统重要文件完整行扫描
  3.2、系统可执行文件安全扫描
  3.3、临时目录文件安全扫描
  3.4、用户目录文件扫描
  3.5、可疑隐藏文件扫描
4、各用户历史操作类
  4.1、境外ip操作类
  4.2、反弹shell类
5、进程类安全检测
  5.1、CUP和内存使用异常进程排查
  5.2、隐藏进程安全扫描
  5.3、反弹shell类进程扫描
  5.4、恶意进程信息安全扫描
  5.5、进程对应可执行文件安全扫描
6、网络类安全检测
  6.1、境外IP链接扫描
  6.3、恶意特征链接扫描
  6.4、网卡混杂模式检测
7、后门类检测
  7.1、LD_PRELOAD后门检测
  7.2、LD_AOUT_PRELOAD后门检测
  7.3、LD_ELF_PRELOAD后门检测
  7.4、LD_LIBRARY_PATH后门检测
  7.5、ld.so.preload后门检测
  7.6、PROMPT_COMMAND后门检测
  7.7、Cron后门检测
  7.8、Alias后门
  7.9、SSH 后门检测
  7.10、SSH wrapper 后门检测
  7.11、inetd.conf 后门检测
  7.12、xinetd.conf 后门检测
  7.13、setUID 后门检测
  7.14、8种系统启动项后门检测
8、账户类安全排查
  8.1、root权限账户检测
  8.2、空口令账户检测
  8.3、sudoers文件用户权限检测
  8.4、查看各账户下登录公钥
  8.5、账户密码文件权限检测
9、日志类安全分析
  9.1、secure登陆日志
  9.2、wtmp登陆日志
  9.3、utmp登陆日志
  9.4、lastlog登陆日志
10、安全配置类分析
  10.1、DNS配置检测
  10.2、Iptables防火墙配置检测
  10.3、hosts配置检测
11、Rootkit分析
  11.1、检查已知rootkit文件类特征
  11.2、检查已知rootkit LKM类特征
  11.3、检查已知恶意软件类特征检测
12.WebShell类文件扫描
  12.1、WebShell类文件扫描
```

***\*【测试环境：】\****

- 
- 

```
【系统：CentOS (6、7) + python (2.x、3.x)】【权限：root权限启动 】
```

***\**\*【执行时间：】\*\**\***

- 
- 
- 
- 

```
【默认安全扫描大概执行时间为4～6分钟】【完全扫描在1～2小时之间】【程序执行时间的长度由检测文件的多少决定】【有可能会存在较长的时间，请耐心等待】
```

***\**\*【兼容性：】\*\**\***

- 
- 
- 

```
【目前程序只针对Centos进行开发测试】【其他系统并未做兼容性】【检测结果未知】
```

***\**\*【参数和参考：】\*\**\***

```
sh-3.2# python GScan.py -h

  _______      _______.  ______      ___      .__   __.
 /  _____|    /       | /      |    /   \     |  \ |  |    {version:v0.1}
|  |  __     |   (----`|  ,----'   /  ^  \    |   \|  |
|  | |_ |     \   \    |  |       /  /_\  \   |  . `  |    {author:咚咚呛}
|  |__| | .----)   |   |  `----. /  _____  \  |  |\   |
 \______| |_______/     \______|/__/     \__\ |__| \__|    http://grayddq.top
  
  
Usage: GScan.py [options]
 
Options:
 
  -h, --help     show this help message and exit
  --version      当前程序版本
 
 Mode:
    GScan running mode options
   
    --overseas   境外模式，此参数将不进行境外ip的匹配
    --full       完全模式，此参数将启用完全扫描
    --debug      调试模式，进行程序的调试数据输出
    --dif        差异模式，比对上一次的结果，输出差异结果信息。
    --sug        排查建议，用于对异常点的手工排查建议
    --pro        处理方案，根据异常风险生成初步的处理方案
   
 Optimization:
    Optimization options
   
    --time=TIME  搜索指定时间内主机改动过的所有文件，demo: --time='2019-05-07
                 00:00:00~2019-05-07 23:00:00'
    --job        添加定时任务，用于定时执行程序
    --log        打包当前系统的所有安全日志（暂不支持）
```



**【执行命令参考：】**

root# python GScan.py

root# python GScan.py --sug --pro

进行定时任务设置，异常日志将按行输出到./GScan/log/log.log，可通过syslog等服务同步日志信息。

root# python GScan.py --job #每天零点执行一次

root# python GScan.py --job --hour=2 #每2小时执行一次



**【程序脚本说明：】**

```
GScan
----GScan.py                   #主程序
----log                        #日志和结果记录
----lib                        #模块库文件
-------core                    #调用库文件
----------common.py            #公共库模块
----------globalvar.py         #全局参数管理模块
----------option.py            #参数管理模块
----------ip                   ##ip地址定位库
-------egg                     #yara打包动态库
-------malware                 #恶意特征库
-------plugins                 #检测插件模块库
----------Host_Info.py         #主机信息获取
----------File_Analysis.py     #文件类安全检测
----------History_Analysis.py  #用户历史操作类
----------Proc_Analysis.py     #进程类安全检测
----------Network_Analysis.py  #网络类安全检测
----------Backdoor_Analysis.py #后门类检测
----------User_Analysis.py     #账户类安全排查
----------Log_Analysis.py      #日志类安全分析
----------Config_Analysis.py   #安全配置类分析
----------Rootkit_Analysis.py  #Rootkit分析
----------SSHAnalysis.py       #secure日志分析
----------Webserver.py         #获取当前web服务的web根目录
----------Webshell_Analysis.py #webshell检测
----------webshell_rule        #webshell检测的规则
```

**【程序特点：】**

```
1、程序检测的逻辑和方法，均是由一线安全应急人员根据多年实战经验总结出来的。2、程序包括10W+的恶意特征信息，用于恶意文件的比对和查杀。3、结果自动化分析，进行黑客攻击溯源
```

**【程序对标：】**

```
入侵痕迹的检测按照经验归纳为如下子项，省去了一些安全配置和基线类等无关项。
注：对比内容为程序的实际检测输出结果，其仅代表个人的观点，不代表产品说明。
```

**【对标四款标准Linux安全检查工具】
**

```
GScan      程序定位为安全人员提供的一项入侵检测工具，旨在尽可能的发现入侵痕迹，溯源出黑客攻击的整个路径。
chkrootkit 程序定位为安全人员提供的一项入侵检测工具，旨在发现被植入的后门或者rootkit。
rkhunter   程序定位为安全人员提供的一项入侵检测工具，旨在发现被植入的后门或者rootkit。
lynis      程序定位为安全人员日常使用的一款用于主机基线和审计的工具，可辅助漏洞扫描和配置管理，也可部分用于入侵检测。
【检查项目List】
```



| 检测项                                                      | GScan | chkrootkit | rkhunter | lynis  |
| ----------------------------------------------------------- | ----- | ---------- | -------- | ------ |
| 对比版本                                                    | v0.1  | v0.53      | v1.4.6   | v2.7.1 |
| 【检测前检查项】文件alias检查                               | √     | √          |          |        |
| 【检测前检查项】系统重要文件完整性检测                      | √     | √          |          |        |
| 【主机文件检测】系统重要文件权限检测                        |       | √          | √        |        |
| 【主机文件检测】文件恶意特征扫描                            | √     |            |          |        |
| 【主机文件检测】文件境外IP特征扫描                          | √     |            |          |        |
| 【主机文件检测】敏感目录mount隐藏检测                       |       |            | √        | √      |
| 【主机操作检测】境外IP操作记录检测                          | √     |            |          |        |
| 【主机操作检测】可疑操作或异常检测                          | √     | √          |          |        |
| 【主机进程检测】CPU&内存使用异常检测                        | √     |            |          | √      |
| 【主机进程检测】I/O异常检测                                 |       |            |          | √      |
| 【主机进程检测】隐藏进程检测                                | √     |            | √        |        |
| 【主机进程检测】反弹shell进程检测                           | √     |            |          |        |
| 【主机进程检测】可疑进程名称检测                            | √     |            |          |        |
| 【主机进程检测】进程exe恶意特征检测                         | √     |            |          |        |
| 【主机进程检测】僵尸进程检测                                |       |            |          | √      |
| 【主机进程检测】可疑的较大共享内存检测                      |       |            | √        |        |
| 【主机进程检测】内存恶意特征检测                            |       |            |          |        |
| 【网络链接检测】境外IP链接检测                              | √     |            |          |        |
| 【网络链接检测】恶意特征链接检测                            | √     | √          | √        |        |
| 【网络链接检测】网卡混杂模式检测                            | √     | √          | √        | √      |
| 【常规后门检测】LD_PRELOAD后门检测                          | √     |            | √        |        |
| 【常规后门检测】LD_AOUT_PRELOAD后门检测                     | √     |            | √        |        |
| 【常规后门检测】LD_ELF_PRELOAD后门检测                      | √     |            | √        |        |
| 【常规后门检测】LD_LIBRARY_PATH后门检测                     | √     |            | √        |        |
| 【常规后门检测】ld.so.preload后门检测                       | √     |            | √        |        |
| 【常规后门检测】PROMPT_COMMAND后门检测                      | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/var/spool/cron/)              | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/etc/cron.d/)                  | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/etc/cron.daily/)              | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/etc/cron.weekly/)             | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/etc/cron.hourly/)             | √     |            |          |        |
| 【常规后门检测】Cron后门检测(/etc/cron.monthly/)            | √     |            |          |        |
| 【常规后门检测】alias后门检测                               | √     |            | √        |        |
| 【常规后门检测】其他环境变量未知后门检测                    | √     |            |          |        |
| 【常规后门检测】SSH后门检测                                 | √     |            |          |        |
| 【常规后门检测】SSH Wrapper后门检测                         | √     |            |          |        |
| 【常规后门检测】inetd.conf后门检测                          | √     |            | √        |        |
| 【常规后门检测】xinetd.conf后门检测                         | √     |            | √        |        |
| 【常规后门检测】setUID后门检测                              | √     |            |          |        |
| 【常规后门检测】setGID后门检测                              |       |            |          |        |
| 【常规后门检测】fstab后门检测                               |       |            |          |        |
| 【常规后门检测】系统启动项(/etc/init.d/)后门检测            | √     |            | √        |        |
| 【常规后门检测】系统启动项(/etc/rc.d/)后门检测              | √     |            | √        |        |
| 【常规后门检测】系统启动项(/etc/rc.local)后门检测           | √     |            | √        |        |
| 【常规后门检测】系统启动项(/usr/local/etc/rc.d)后门检测     | √     |            | √        |        |
| 【常规后门检测】系统启动项(/usr/local/etc/rc.local)后门检测 | √     |            | √        |        |
| 【常规后门检测】系统启动项(/etc/conf.d/local.start)后门检测 | √     |            | √        |        |
| 【常规后门检测】系统启动项(/etc/inittab)后门检测            | √     |            | √        |        |
| 【常规后门检测】系统启动项(/etc/systemd/system)后门检测     | √     |            | √        |        |
| 【账户安全检测】root权限账户检测                            | √     |            | √        | √      |
| 【账户安全检测】空口令账户检测                              | √     |            | √        | √      |
| 【账户安全检测】sudoers文件检测                             | √     |            |          | √      |
| 【账户安全检测】用户组文件检测                              |       |            | √        | √      |
| 【账户安全检测】密码文件检测                                | √     |            | √        | √      |
| 【账户安全检测】用户免密登录公钥检测                        | √     |            | √        |        |
| 【日志安全检测】secure日志安全检测                          | √     |            |          |        |
| 【日志安全检测】wtmp日志安全检测                            | √     | √          |          |        |
| 【日志安全检测】utmp日志安全检测                            | √     | √          |          |        |
| 【日志安全检测】lastlog日志安全检测                         | √     | √          |          |        |
| 【日志安全检测】web日志安全检测                             |       |            |          |        |
| 【日志安全检测】其他服务日志安全检测                        |       |            |          |        |
| 【安全配置检测】DNS设置检测                                 | √     |            |          | √      |
| 【安全配置检测】防火墙设置检测                              | √     |            |          | √      |
| 【安全配置检测】hosts安全检测                               | √     |            |          | √      |
| 【Rootkit检测】已知Rootkit文件特征检测                      | √     | √          | √        |        |
| 【Rootkit检测】已知Rootkit LKM类特征检测                    | √     | √          | √        |        |
| 【Rootkit检测】恶意软件类特征检测                           | √     |            | √        |        |
| 【WEBShell检测】Nginx服务WebShell检测                       | √     |            |          |        |
| 【WEBShell检测】Apache服务WebShell检测                      | √     |            |          |        |
| 【WEBShell检测】Tomcat服务WebShell检测                      | √     |            |          |        |
| 【WEBShell检测】Jetty服务WebShell检测                       | √     |            |          |        |
| 【WEBShell检测】Resin服务WebShell检测                       | √     |            |          |        |
| 【WEBShell检测】Jenkins服务WebShell检测                     | √     |            |          |        |
| 【WEBShell检测】其他默认web目录WebShell检测                 | √     |            |          |        |
| 【漏洞类检查】服务漏洞或配置错误检查                        |       |            |          | √      |
| 【自动攻击路径追溯】攻击路径追溯                            | √     |            |          |        |

**监测结果：
**



- 

```
日志及结果目录默认：./GScan/log/gscan.log
```

**运行截图：**

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

***Part. 1. LinuxEmergency***



**【Github、部署和执行：】**

**
**

```
git clone https://github.com/cisp/LinuxEmergency.git
cd LinuxEmergency
sh ./install.sh
```

要求是root权限



**【查看操作系统信息：】**

```
[root@centos emergency]# python emergency.py -o

        内核版本 : Linux-3.10.0-514.26.2.el7.v7.4.qihoo.x86_64-x86_64-with-centos-7.2.1511-Core
        CORE数量 : 16
        CPU数量 : 16
        CPU使用率 : scputimes(user=1.0, nice=0.0, system=0.0, idle=15.0, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
        内存总量  : 33736994816
        内存使用率 : 5.1

[root@centos emergency]#
```

**【查看内核模块信息：】**

```
[root@centos emergency]# python emergency.py -k
内核模块 : nfnetlink_queue  来源  :
内核模块 : nfnetlink_log  来源  :
内核模块 : nfnetlink  来源  :  nfnetlink_log,nfnetlink_queue
内核模块 : bluetooth  来源  :
```

**【查看所有登录成功失败的IP地址：】**

```
[root@scentos emergency]# python emergency.py -l
192.168.100.35  失败
192.168.100.31  失败
127.0.0.1  失败
192.168.100.20  成功
```

**【查看登录成功和失败日志：】
**

```
# 成功的 -s
[root@centos emergency]# python emergency.py -s | more
账户 : emergency    时间 : 2017-08-09-11:20  来源 : (192.168.100.24)
账户 : emergency    时间 : 2017-08-09-14:34  来源 : (192.168.100.24)
账户 : root    时间 : 2017-09-28-12:38  来源 : (192.168.100.65)
账户 : root    时间 : 2017-09-28-12:46  来源 : (192.168.100.65)
账户 : root    时间 : 2017-09-28-13:13  来源 : (192.168.100.65)

# 失败的 -f
[root@centos emergency]# python emergency.py -f | more
账户 : emergency    时间 : 192.168.100.34  来源 : Jul-6-21:27---21:27
账户 : emergency    时间 : 192.168.100.34  来源 : Jul-6-21:25---21:25
账户 : admin    时间 : 127.0.0.1  来源 : Jul-5-15:32---15:32

# 如果需要指定IP 加-i参数 ，例如 -i 192.168.100.34；
```

**【查看进程列表和详细信息：】**

```
# 列表信息
[root@centos emergency]# python emergency.py -a
***********************************************************************************************************
进程ID号: 2     进程名称: kthreadd     进程用户: root     启动时间: 2018-06-16 07:40:48
CPU占比: 0.0%     内存占比: 0.0%
网络连接:
***********************************************************************************************************
***********************************************************************************************************
进程ID号: 3     进程名称: ksoftirqd/0     进程用户: root     启动时间: 2018-06-16 07:40:48
CPU占比: 0.0%     内存占比: 0.0%
网络连接:
***********************************************************************************************************
...

#  详细信息
[root@centos emergency]# python emergency.py -p 28344
***********************************************************************************************************
进程ID号: 28344     进程名称: screen     进程用户: emergency     启动时间: 2018-06-22 13:25:30
工作路径: /home/emergency/
进程命令: SCREEN
父母进程: 1
亲子进程: [28345]
CPU占比: 0.0%     内存占比: 0.0046135703802%
网络连接:
进程环境:
        终端会话    :  /bin/bash
        安全会话    :
        登录账户    :  emergency
        工作账户    :  emergency
        权限路径    :  /usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/emergency/tools:/usr/local/bin:/usr/local/sbin:/usr/local/python3/bin:/home/emergency/.local/bin:/home/emergency/bin
        用户目录    :  /home/emergency

***********************************************************************************************************
```

**【添加virustotal基本查询功能：】**

**
**

```
# 检查样本
[root@centos emergency]# python vt.py -f ./LICENSE
******************************************
检测时间: 2018-07-09 07:31:04
报毒数量: 0
报毒引擎: []
引擎总数: 59
******************************************

# 检查URL
[root@centos emergency]# python vt.py -u http://1.1.1.2/bmi/docs.autodesk.com
******************************************
检测时间: 2018-07-09 16:33:29
关联样本: 0
关联连接: 0
关联域名: 0
******************************************

# 检查域名
[root@centos emergency]# python vt.py -d baidu.com
******************************************
检测时间: 2018-07-09 16:33:35
关联样本: 202
关联连接: 100
关联域名: 8
******************************************

# 检查IP
[root@centos emergency]# python vt.py -a 114.114.114.114
******************************************
检测时间: 2018-07-09 16:34:05
关联样本: 135
关联连接: 93
```

**【增加查看whois信息的功能：】**



```
[root@centos emergency]# python mywhois.py -d baidu.com
Domain Name: baidu.com
Registry Domain ID: 11181110_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2017-07-27T19:36:28-0700
Creation Date: 1999-10-11T04:05:17-0700
Registrar Registration Expiration Date: 2026-10-11T00:00:00-0700
Registrar: MarkMonitor, Inc.
Registrar IANA ID: 292
Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
Registrar Abuse Contact Phone: +1.2083895740
Domain Status: clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)
Domain Status: clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)
Domain Status: clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)
Domain Status: serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)
Domain Status: serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)
Domain Status: serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)
Registrant Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Registrant State/Province: Beijing
Registrant Country: CN
Admin Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Admin State/Province: Beijing
Admin Country: CN
Tech Organization: Beijing Baidu Netcom Science Technology Co., Ltd.
Tech State/Province: Beijing
Tech Country: CN
Name Server: ns4.baidu.com
Name Server: ns3.baidu.com
Name Server: dns.baidu.com
Name Server: ns2.baidu.com
Name Server: ns7.baidu.com
DNSSEC: unsigned
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
>>> Last update of WHOIS database: 2018-07-09T02:21:59-0700 <<<

If certain contact information is not shown for a Registrant, Administrative,
or Technical contact, and you wish to send a message to these contacts, please
send your message to whoisrelay@markmonitor.com and specify the domain name in
the subject line. We will forward that message to the underlying contact.

If you have a legitimate interest in viewing the non-public WHOIS details, send
your request and the reasons for your request to abusecomplaints@markmonitor.com
and specify the domain name in the subject line. We will review that request and
may ask for supporting documentation and explanation.

The Data in MarkMonitor.com's WHOIS database is provided by MarkMonitor.com for
information purposes, and to assist persons in obtaining information about or
related to a domain name registration record.  MarkMonitor.com does not guarantee
its accuracy.  By submitting a WHOIS query, you agree that you will use this Data
only for lawful purposes and that, under no circumstances will you use this Data to:
 (1) allow, enable, or otherwise support the transmission of mass unsolicited,
     commercial advertising or solicitations via e-mail (spam); or
 (2) enable high volume, automated, electronic processes that apply to
     MarkMonitor.com (or its systems).
MarkMonitor.com reserves the right to modify these terms at any time.
By submitting this query, you agree to abide by this policy.

MarkMonitor is the Global Leader in Online Brand Protection.

MarkMonitor Domain Management(TM)
MarkMonitor Brand Protection(TM)
MarkMonitor AntiPiracy(TM)
MarkMonitor AntiFraud(TM)
Professional and Managed Services

Visit MarkMonitor at http://www.markmonitor.com
Contact us at +1.8007459229
In Europe, at +44.02032062220

For more information on Whois status codes, please visit
 https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en
--
```



