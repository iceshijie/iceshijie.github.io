## sql语句语法汇总(1)

## 1. 表创建

```txt
CREATE TABLE <表名> 
（<列名> <数据类型>[ <列级完整性约束条件> ]      
[，<列名> <数据类型>[ <列级完整性约束条件>] ] 
……      
[，<表级完整性约束条件> ] 
 ）；
```

Txt

Copy

全屏

其中<>内的为必需内容。[]内的为可选内容。
列级完整性约束是对每个元组的字段值的约束，比如说非0，或者只能取男或取女等。
表级完整性约束则是对表的部分约束，例如主键，外键等。

### 1.1 数据类型

```txt
1)定长和变长字符串CHAR(n)    VARCHAR(n)
2)定长和变长二进制串 BIT(n)  BITVARING(n)
3)整型数   INT  SMALLINT
4)浮点数   FLOAT    DOUBLE  PRECISION
5)日期型   DATE  
6)时间型   TIME   
7)时标  TIMESTAMP 
```

Txt

Copy

全屏

### 1.2 常用完整性约束

```txt
主码约束：PRIMARY  KEY
唯一性约束：UNIQUE
非空值约束：NOT NULL
参照完整性约束
```

Txt

Copy

全屏

### 1.3 主码定义

```txt
1）在列出关系模式的属性时,在属性及其类型后加上保留字PRIMARY KEY；
2）在列出关系模式的所有属性后，再附加一个声明：
      PRIMARY KEY （<属性1>[，<属性2>，…]）
说明：如果关键字由多个属性构成，则必须使用第二种方法。
```

Txt

Copy

全屏

例子：

```sql
CREATE TABLE SC
     ( Sno CHAR(5) ,
  Cno CHAR(3) , 
  Grade   INT,
  Primary key (Sno, Cno));
```

SQL

Copy

全屏

### 1.4 外码定义

```txt
1）如果外部关键字只有一个属性，可以在它的属性名和类型后面直接用“REFERENCES”说明它参照了某个表的某些属性，其格式为：
   REFERENCES <表名>(<属性>)
2）在CREATE TABLE语句的属性列表后面增加一个或几个外部关键字说明，其格式为：
   FOREIGN KEY (<属性>) REFERENCES <表名>(<属性>)
```

Txt

Copy

全屏

例子：

```sql
CREATE  TABLE  SC
( Sno  CHAR(5)   REFERENCES S(Sno) ,
  Cno CHAR(3) REFERENCES C(Cno),
  Grade  INT,
  PRIMARY KEY (Sno,Cno));
```

SQL

Copy

全屏

```sql
CREATE  TABLE  SC
  ( SNO  CHAR(8),
     CNO CHAR(4),
     GRADE  SMALLINT,
     PRIMARY KEY (SNO,CNO),
     FOREIGN KEY (SNO)  REFERENCES S(SNO),
     FOREIGN KEY (CNO)  REFERENCES C(CNO));
```

SQL

Copy

全屏

## 2. 表修改

```txt
ALTER TABLE <表名>
[ ADD <新列名> <数据类型> [ 完整性约束 ] ]
[ DROP <列名>|<完整性约束名> ]
[ ALTER <列名> <数据类型> ]；

<表名>：要修改的基本表
ADD子句：增加新列和新的完整性约束条件
DROP子句：删除指定的列或完整性约束条件
ALTER子句：用于修改列名和数据类型
```

Txt

Copy

全屏

例子：

```sql
ALTER TABLE S ADD Scome DATE;//增加列
ALTER TABLE S Drop Scome;//需要注意的是，如果一个属性的列级约束为not null则不被允许删除。
ALTER TABLE S ALTER Sage SMALLINT;//修改数据类型
ALTER TABLE S DROP UNIQUE(Sname);//删除列级约束
```

SQL

Copy

全屏

```txt
DROP TABLE <表名>;//删除表
```

Txt

Copy

全屏

例子：

```sql
DROP TABLE S;
```

SQL

Copy

全屏

*补充*：

```txt
可以在定义属性时增加保留字DEFAULT和一个合适的值。
例如：
      性别  CHAR（1） DEFAULT ‘男’；
      年龄  SMALLINT  DEFAULT 1；
修改默认值
   ALTER TABLE S ADD CONSTRAINT dd DEFAULT ‘男’ FOR sex; 
```

Txt

Copy

全屏

## 3. 表查询

```txt
SELECT [ALL|DISTINCT] <目标列表达式>
        [，<目标列表达式>] …
FROM <表名或视图名>[, <表名或视图名> ] …
[ WHERE <条件表达式> ]
[ GROUP BY <列名1> 
[ HAVING <条件表达式> ] ]
[ ORDER BY <列名2> [ ASC|DESC ] ]；
```

Txt

Copy

全屏

```txt
学生-课程数据库
学生表：S(Sno，Sname，Ssex，Sage，Sdept)
课程表：C(Cno，Cname，Cpno，Ccredit)
学生选课表：SC(Sno，Cno，Grade) 
```

Txt

Copy

全屏

### 3.1 单表查询

```sql
SELECT Sno，Sname FROM S；//查询所有的学生的学号和姓名。
```

SQL

Copy

全屏

```txt
SELECT子句的<目标列表达式>为表达式
算术表达式   //1+1
字符串常量   //'a'
函数      //avg()
列别名等    //Cno as 学号
```

Txt

Copy

全屏

```txt
DISTINCT    //不显示重复内容
ALL     //即使重复也会全部显示
```

Txt

Copy

全屏

例子：

```sql
SELECT DISTINCT Sno FROM SC;
SELECT ALL Sno FROM SC; //(默认 ALL)
```

SQL

Copy

全屏

在原来的基础上加上where子句。

#### 3.1 where子句中可能遇到的谓词：

```txt
比较          =,<>,>,>=,<,<=
算术运算        +  - *  /
确定范围        Between And ,
                Not Between And
确定集合        IN  , NOT IN
字符匹配        Like , Not Like
空值          IS NULL ,IS NOT NULL
多重条件        AND , OR
```

Txt

Copy

全屏

比较谓词：

```sql
SELECT Sname，Sage 
         FROM    S
         WHERE Sage < 20；
```

SQL

Copy

全屏

确定范围的谓词：

```sql
 SELECT Sname，Sdept，Sage
 FROM   S
 WHERE Sage BETWEEN 20 AND 23； 
```

SQL

Copy

全屏

确定集合的谓词：

```txt
使用谓词：IN <值表>,  NOT IN <值表>
  <值表>：用逗号分隔的一组取值
```

Txt

Copy

全屏

```sql
SELECT Sname，Ssex
FROM  S
WHERE Sdept IN ( 'IS'，'MA'，'CS' );
```

SQL

Copy

全屏

*在这里字符串匹配暂且不讲。因为我也莫得学*
涉及空值的谓词：

```txt
使用谓词 IS NULL 或 IS NOT NULL
 “IS NULL” 不能用 “= NULL” 代替
```

Txt

Copy

全屏

```sql
SELECT Sno，Cno
     FROM SC
     WHERE Grade IS NULL；//查询缺失成绩的学号和课程号
```

SQL

Copy

全屏

多重条件：

```txt
AND的优先级高于OR
可以用括号改变优先级
```

Txt

Copy

全屏

```sql
SELECT Sname，Ssex
FROM S
WHERE Sdept IN ( 'IS'，'MA'，'CS' );
可改写为：
SELECT Sname，Ssex
FROM   S
WHERE  Sdept= ' IS ' OR Sdept= ' MA' OR Sdept= ' CS '；
```

SQL

Copy

全屏

#### 3.1.2 对查询结果进行排序：

使用ORDER BY子句
可以按一个或多个属性列排序
升序：ASC；降序：DESC；缺省值为升序
当排序列含空值时
ASC：排序列为空值的元组最后显示
DESC：排序列为空值的元组最先显示

```sql
    SELECT Sno，Grade
    FROM  SC
    WHERE  Cno= ' 3 '
    ORDER BY Grade DESC//按照成绩排序，并且降序。
```

SQL

Copy

全屏

#### 3.1.3 集函数

5类主要集函数：
计数
COUNT（[DISTINCT|ALL] *）
COUNT（[DISTINCT|ALL] <列名>）
计算总和
SUM（[DISTINCT|ALL] <列名>）
计算平均值
AVG（[DISTINCT|ALL] <列名>）
求最大值
MAX（[DISTINCT|ALL] <列名>
求最小值
MIN（[DISTINCT|ALL] <列名>

```sql
SELECT COUNT(*) FROM  S；    //查询学生总数
SELECT AVG(Grade) FROM SC WHERE Cno= ' 1 '； //查询成绩平均值。
```

SQL

Copy

全屏

#### 3.1.4 对查询结果分组

使用GROUP BY子句分组
细化集函数的作用对象
未对查询结果分组，集函数将作用于整个查询结果
对查询结果分组后，集函数将分别作用于每个组

```sql
     SELECT Cno，COUNT(Sno)
     FROM    SC
     GROUP BY Cno；  //按课程号分组，集函数会作用于每个组。
结果：
            Cno        COUNT(Sno)
            1             22
            2             34
            3             44
        4             33
            5             48
```

SQL

Copy

全屏

GROUP BY子句的作用对象是查询的中间结果表
分组方法：按指定的一列或多列值分组，值相等的为一组
使用GROUP BY子句后，SELECT子句的列名列表中只能出现分组属性和集函数

having子句做进一步筛选：

```txt
只有满足HAVING短语指定条件的组才输出
HAVING短语与WHERE子句的区别：作用对象不同
WHERE子句作用于基表或视图，从中选择满足条件的元组。
HAVING短语作用于组，从中选择满足条件的组。 
```

Txt

Copy

全屏

```sql
SELECT Sno
     FROM  SC
     GROUP BY Sno
     HAVING  COUNT(*) >3；   //查询选修了三门课程以上的学生的学号。
```

SQL

Copy

全屏

### 3.2 连接查询

涉及多个表的查询称为连接查询。
用来连接两个表的条件称为连接条件或者连接谓词。此处需要注意的是连接条件是放在where子句中的。

```txt
一般格式：
    [<表名1>.]<列名1>  <比较运算符>  [<表名2>.]<列名2>
```

Txt

Copy

全屏

```txt
SQL中连接查询的主要类型:
    广义笛卡尔积
    等值连接(含自然连接)
    非等值连接查询
    自身连接查询
    外连接查询
    复合条件连接查询
```

Txt

Copy

全屏

#### 3.2.1 广义笛卡尔积

不带谓词的连接。且很少使用。

```sql
SELECT  S.* ,  SC.*
         FROM     S, SC；
```

SQL

Copy

全屏

#### 3.2.2 等值连接以及非等值连接

```txt
连接运算符为 = 的连接操作
 [<表名1>.]<列名1>  =  [<表名2>.]<列名2>
任何子句中引用表1和表2中同名属性时，都必须加表名前缀。引用唯一属性名时可以加也可以省略表名前缀。 
```

Txt

Copy

全屏

反之就是非等值连接嘛！
至于自然连接：等值连接的一种特殊情况，把目标列中重复的属性列去掉。
例子：

```sql
   SELECT  S.Sno,Sname,Ssex,Sage,Sdept,Cno,Grade
    FROM     S,SC
    WHERE  S.Sno = SC.Sno；
```

SQL

Copy

全屏

#### 3.2.3 自身连接

一个表与其自己进行连接，称为表的自身连接；
需要给表起别名以示区别；
由于所有属性名都是同名属性，因此必须使用别名前缀。

```sql
SELECT  FIRST.Cno，SECOND.Cpno
      FROM  C as FIRST，C as SECOND
      WHERE FIRST.Cpno = SECOND.Cno； 
```

SQL

Copy

全屏

其中as就是起别名的操作。

#### 3.2.4 外连接

外连接与普通连接的区别
普通连接操作只输出满足连接条件的元组
外连接操作以指定表为连接主体，将主体表中不满足连接条件的元组一并输出
即一个表中有2条记录，另一个表中有1条记录。连接后的总表为两条记录。缺失的部分空着。

```txt
左外连接
LEFT (OUTER) JOIN <表名> ON <条件>;
右外连接
RIGHT (OUTER) JOIN <表名> ON <条件>;
全外连接
FULL (OUTER) JOIN <表名> ON <条件>;
```

Txt

Copy

全屏

```sql
SELECT  S.Sno, Sname, Ssex, Sage, Sdept, Cno，Grade
      FROM  S  LEFT (OUTER) JOIN  SC
      ON S.Sno = SC.Sno； 
```

SQL

Copy

全屏

#### 3.2.5 复合条件连接

WHERE子句中含多个连接条件时，称为复合条件连接

```sql
SELECT S.Sno, S.Sname
FROM    S, SC
WHERE S.Sno = SC.Sno AND   /* 连接谓词*/
        SC.Cno= ' 2 ' AND     /* 其他限定条件 */
        SC.Grade > 90；       /* 其他限定条件 */
```

SQL

Copy

全屏

### 3.3 集合查询

标准SQL直接支持的集合操作种类
并操作(UNION)

一般商用数据库支持的集合操作种类
并操作(UNION)
交操作(INTERSECT)
差操作(EXCEPT)

所以这里暂且只讲并操作，即联合查询。

```txt
    <查询块>
     UNION
    <查询块>
参加UNION操作的各结果表的列数必须相同；对应项的数据类型也必须相同
```

Txt

Copy

全屏

例子：

```sql
        (SELECT *
         FROM S
         WHERE Sdept= 'CS')
        UNION
        (SELECT *
         FROM S
         WHERE Sage<=19)；
```

SQL

Copy

全屏

### 3.3 嵌套查询

一个SELECT-FROM-WHERE语句称为一个查询块
将一个查询块嵌套在另一个查询块的WHERE子句或HAVING短语的条件中的查询称为嵌套查询

```sql
        SELECT Sno
        FROM SC
        WHERE Cno=' 1 ' AND Sno IN
                               (SELECT Sno
                                FROM SC
                                WHERE Cno=' 2 ')；
```

SQL

Copy

全屏

**嵌套查询又分为：**
不相关子查询
子查询的查询条件不依赖于父查询
相关子查询
子查询的查询条件依赖于父查询

**不相关子查询：**
是由里向外逐层处理。即每个子查询在
上一级查询处理之前求解，子查询的结果
用于建立其父查询的查找条件。
**相关子查询：**
首先取外层查询中表的第一个元组，根据它与内层查询相关的属性值处理内层查询，若WHERE子句返回值为真，则取此元组放入结果表；
然后再取外层表的下一个元组；
重复这一过程，直至外层表全部检查完为止

例子：

```sql
   SELECT Sno，Sname，Sdept
    FROM S
    WHERE Sdept  IN
          (SELECT Sdept
           FROM S
           WHERE Sname= ‘ 刘晨 ’)；

     SELECT Sno，Sname，Sdept
     FROM    S
     WHERE Sdept   =
           ( SELECT Sdept
            FROM    S
            WHERE Sname= ' 刘晨 ')；
```

SQL

Copy

全屏

```txt
需要配合使用比较运算符
> ANY    大于子查询结果中的某个值       
 > ALL  大于子查询结果中的所有值
< ANY    小于子查询结果中的某个值    
< ALL    小于子查询结果中的所有值
>= ANY  大于等于子查询结果中的某个值    
>= ALL  大于等于子查询结果中的所有值
<= ANY  小于等于子查询结果中的某个值    
<= ALL  小于等于子查询结果中的所有值
= ANY    等于子查询结果中的某个值        
=ALL      等于子查询结果中的所有值（通常无实际意义）
!=（或<>）ANY   不等于子查询结果中的某个值
!=（或<>）ALL    不等于子查询结果中的任何一个值
```

Txt

Copy

全屏

例子：

```sql
    SELECT Sname，Sage
    FROM    S
    WHERE Sage < ANY (SELECT  Sage
                                  FROM    S
                                  WHERE Sdept= ' IS ')
                                    AND Sdept <> ' IS ' ;
```

SQL

Copy

全屏

带有EXISTS谓词的子查询：
\1. EXISTS谓词
存在量词
带有EXISTS谓词的子查询不返回任何数据，只产生逻辑真值“true”或逻辑假值“false”。
若内层查询结果非空，则返回真值
若内层查询结果为空，则返回假值
\2. NOT EXISTS谓词
若内层查询结果非空，则返回假值
若内层查询结果为空，则返回真值
由EXISTS引出的子查询，其目标列表达式通常都用* ，因为带EXISTS的子查询只返回真值或假值，给出列名无实际意义

```sql
     SELECT Sname
        FROM S
        WHERE EXISTS    /*相关子查询*/
           (SELECT *
            FROM SC
            WHERE Sno=S.Sno AND Cno=‘1’)
```

SQL

Copy

全屏

***重点：除运算\***

[![img](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_f5fbf3b70b3bba63ced5a0d89abed848.jpg)](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_f5fbf3b70b3bba63ced5a0d89abed848.jpg)

[![img](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_c9a6cf0b47cbd36a7854a58a1503653d.jpg)](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_c9a6cf0b47cbd36a7854a58a1503653d.jpg)

[![img](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_49387eab407d2af304d1a9a2b76a1ab7.jpg)](https://www.3rsh1.cool/wp-content/uploads/2020/04/wp_editor_md_49387eab407d2af304d1a9a2b76a1ab7.jpg)

## 4. 表更新

### 4.1 插入数据

```txt
将新元组插入表中。
INSERT
INTO <表名> [(<属性列1>[，<属性列2 >…)]
VALUES (<常量1> [，<常量2>]    …           )
```

Txt

Copy

全屏

例子：

```sql
    INSERT
     INTO S
     VALUES ('95020', '计14-5', '陈冬', '男', 18, 'IS');

     INSERT
      INTO  Deptage(Sdept，Avgage)
              SELECT  Sdept，AVG(Sage)
              FROM  S
              GROUP BY Sdept；
```

SQL

Copy

全屏

上述是插入的两个不同的值，一个是我们给出的另外一个是子查询得到的。

### 4.2 修改数据

```txt
修改指定表中满足WHERE子句条件的元组
   UPDATE  <表名>
    SET  <列名>=<表达式>[，<列名>=<表达式>]…
    [WHERE <条件>]；
```

Txt

Copy

全屏

**三种修改方式：**
修改某一个元组的值
修改多个元组的值
带子查询的修改语句

**修改一个元组的值：**

```sql
         UPDATE  S
         SET Sage=22
         WHERE  Sno=' 95001 '； 
```

SQL

Copy

全屏

**修改多个元组的值：**

```sql
         UPDATE S
         SET Sage= Sage+1；
```

SQL

Copy

全屏

**带子查询的修改语句：**

```sql
        UPDATE SC
        SET  Grade=0
        WHERE  'CS'=
              (SELETE Sdept
               FROM  S
               WHERE  S.Sno = SC.Sno)；
```

SQL

Copy

全屏

**小总结**
\1. SET子句
指定修改方式
要修改的列
修改后取值
\2. WHERE子句
指定要修改的元组
缺省表示要修改表中的所有元组
**拓展**
DBMS在执行修改语句时会检查修改操作是否破坏表上已定义的:
完整性规则
实体完整性
主码不允许修改
用户定义的完整性
NOT NULL约束
UNIQUE约束
值域约束

### 4.3 删除数据

```txt
       DELETE
       FROM     <表名>
       [WHERE <条件>]；
功能:
删除指定表中满足WHERE子句条件的元组
WHERE子句:
指定要删除的元组
缺省表示要修改表中的所有元组
```

Txt

Copy

全屏

例子：

```sql
        DELETE
        FROM SC
        WHERE  'CS'=
            (SELETE Sdept
             FROM S
             WHERE S.Sno=SC.Sno)
```