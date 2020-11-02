利用CMD来修改环境windows环境变量

格式

​     ``` set 变量名=%变量名%;变量内容     ```

添加一个新的路径，输入“ set path=%path%;d:\nmake.exe





```vb
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
@echo off
REM 声明采用UTF-8编码
chcp 65001&cls

REM 备份当前环境变量
echo 当前环境变量：
echo %Path%

echo 永久设置Java、 go、python、mvn、mingw-get...环境变量

SETX /M GO_ROOT "D:\toolsPath\GO\bin"
SETX /M JAVA_HOME "D:\toolsPath\Java\jdk1.8.0_211"

SETX /M Path "%Path%;%Java_Home%\bin;%Java_Home%\jre\bin;D:\toolsPath\Python27;D:\toolsPath\Python37;D:\toolsPath\php-7.4.5;D:\toolsPath\mingw-get\bin;D:\toolsPath\apache-maven-3.6.3\bin"

echo 修改完成, 即将重启文档管理器explorer
pause

REM 重启explorer.exe使环境变量立即生效
taskkill /im explorer.exe /f
echo ================================================
echo 开始重启“explorer.exe”进程
start explorer.exe

pause


```

