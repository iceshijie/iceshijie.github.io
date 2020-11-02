### Android APP测试流程

#### 代码测试

反编译APK

使用反编译软件ApkTool对apk进行反编译。

##### 1.应用配置错误漏洞

###### (1)开启allowbackup备份权限

存在备份数据泄露风险

**整改优先级：高**

**问题描述：** 应用的AndroidManifest.xml文件中allowBackup属性值被设置为true，可通过adb backup对应用数据进行备份，在无root的情况下可以导出应用中存储的所有数据，造成用户数据泄露。

**检查方法和步骤：**

AallowBackup属性，检查是否被设置为true。

**整改建议：**将参数android:allowBackup属性设置为false，防止数据泄漏。



###### (2)开启Debuggable属性

存在应用信息篡改泄露风险

**整改优先级：高**

**问题描述：**被测应用的AndroidManifest.xml文件中Debuggable属性值被设置为true，可以设置断点来控制程序的执行流程，在应用程序运行时修改其行为。

**检查方法和步骤：**

在AndroidManifest.xml中搜索Debuggable属性，检查是否被设置为true。

**整改建议：**将参数android: Debuggable属性设置为false，不能对应用进行调试。



#### 调试测试

手机日志查找敏感信息

adb logcat  >> d:\\1.txt  