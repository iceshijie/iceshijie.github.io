## cookie JWT

JWK

pip install PyJWT

例如ueyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ

### JWT的构成

第一部分我们称它为头部（header)

第二部分我们称其为载荷（payload)

第三部分是签证（signature)

#只能对pyhton字典类型进行加密 第一个参数为需要加密的数据 第二个参数为密钥 第三个参数为加密算法

### jwt加密

encoded_jwt = jwt.encode({'name':'你好'},'secret_key',algorithm='HS256')

print(encoded_jwt)

#加密后是一个二进制的数据

#结果eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiXHU0ZjYwXHU1OTdkIn0.V3flV6UF3Hz0bCqzRTEs_1G46OAOuEM-ku22F14RJL4'

### jwt解密

解密 第一个参数为需要解密的数据 第二个参数为密钥（密钥输入错误会报错） 第三个参数为所用的加密算法

de_code = jwt.decode(encoded_jwt,'secret_key',algorithms=['HS256'])

print(de_code)

u#结果> {'name':'你好'}



密文： eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.ZgXr0npDUDvB9Pg1Q9T8leLYj2qbEFFR1kwfjGXHQPE

进行base64解码

{"alg":"HS256","typ":"JWT"}.{"username":"test"fQ.fëÒzCP;Áôø5CÔüâØjQQÖLeÇQPE

的到加密的类型和用户名haed  **uy8qz-!kru%\*2h7$q&veq=y_r1abu-xd_219y%phex!@4hv62+**



python jwt解密即可

de_code = jwt.decode(encoded_jwt,'secret_key',algorithms=['HS256'])

 