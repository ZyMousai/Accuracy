# Accuracy

**项目简介**：本项目是一个后台管理系统，涉及到权限管理，文档上传下载，部门管理，域名追踪等... 前端：vue，后端：fastapi，项目大致的图形结构如下。

**登陆界面**：![登录](D:\Accuracy项目文档\登录.png)

**主页面**：

![主页](D:\Accuracy项目文档\主页.png)

**功能介绍**：	

[^文档管理]: ：一个常用功能，可以上传和下载文档，也可以进行删除，可以放入到回收站，回收站设置了7天的定时删除功能。
[^账号管理]: ：一些常用的在生活工作中都可以使用到的模块，有对应的加密解密功能，修改账号信息等，非本后台管理系统的用户账号信息。
[^人员管理]: ：对于用户和角色以及部门的管理，一个角色可以对应多个用户，本后台管理系统需要在创建用户的时候绑定对应的角色，部门，不然无法进行功能的使用。
[^文员功能]: ：统计功能，查询功能，域名追踪等功能联合的模块
[^跟踪管理]: ：对于常用的域名等信息进行筛选过滤，返回数据。

**Docker部署**：

```linux
环境基于centos7，mysql版本5.7.37，所需要的环境包放在下面的requirements.txt.
后端部署：
centos7下安装docker：
一，卸载旧版本（如果之前安装过的话）
yum remove docker  docker-common docker-selinux docker-engine
二，安装Docker的详细步骤
2.1 安装需要的软件包， yum-util 提供yum-config-manager功能，另两个是devicemapper驱动依赖
yum install -y yum-utils device-mapper-persistent-data lvm2
2.2 设置一个yum源，下面两个都可用
yum-config-manager --add-repo http://download.docker.com/linux/centos/docker-ce.repo（中央仓库）

yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo（阿里仓库）

2.3 选择docker版本并安装
查看可用版本有哪些
yum list docker-ce --showduplicates | sort -r
选择一个版本并安装：yum install docker-ce-版本号
yum -y install docker-ce-18.03.1.ce
启动 Docker 并设置开机自启
systemctl start docker
systemctl enable docker

以上就是安装docker的全部，下面进入正式的后端部署教程：
首先后端的工程目录打包到linux的目录下，建议放在用户目录，请取名为app。
app应该包含了启动的main文件，对应的api目录，公共目录以及数据库模型，不过具体的目录结构根据自己的接口设计而定，只要主目录名为app即可。
现在，请转到你的项目目录，创建一个 Dockerfile ，名字不要打错了，里面应该包含如下内容
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

你现在应该有一个目录结构，如： 
.
├── app
│   └── main.py
└── Dockerfile

转到项目目录（在你的 Dockerfile 所在的位置，包含你的应用程序目录）。 
构建你的 FastAPI 映像：
docker build -t myimage .   
myimage为镜像名称，请自己定义，本项目为appv1

根据你的镜像运行容器： 
docker run -d --name mycontainer -p 80:80 myimage
命令的第一个80是本地端口，第二个80指向的是docker的80端口，本项目本地指向端口为8000
至此，后端接口部署完成。

前端项目部署：
首先本地构建nginx
sudo yum install -y nginx
1.启动 Nginx
systemctl start nginx
2.停止Nginx
systemctl stop nginx
3.重启Nginx
systemctl restart nginx
4.查看Nginx状态
systemctl status nginx
5.启用开机启动Nginx
systemctl enable nginx
6.禁用开机启动Nginx
systemctl disable nginx

在这里稍稍修改一下本地nginx的监听端口，因为本项目需要利用本地的80端口指向docker的80端口，而本地的nginx默认监听到80端口，因此需要进入/etc/nginx/nginx.conf文件进行修改，本项目修改到81端口。

上面的步骤操作完成之后，将前端的dist目录放到服务器上，也可以放到用户目录之下。
docker run -d --name vue-nginx -p 80:80 \
-v /root/nginx/nginx.conf:/etc/nginx/nginx.conf \
-v /root/nginx/logs:/var/log/nginx \
-v /root/dist:/usr/share/nginx \
-v /root/nginx/conf.d:/etc/nginx/conf.d \
--privileged=true \
--link appv1-fastapi:appv1-fastapi nginx

上述命令为前端启动命令，等下面的配置完成后再进行启动。

命令解析： --name 后指定的是后端容器的名称，80:80 就是 本地端口:docker端口，所以在上面的nginx配置要切换到其他端口， -v指的是本地和docker里的目录相互映射和同步，每一行 -v 对应的都是本地目录和docker里的目录，在本地的目录都要进行一个自建的过程，可以看到，本项目都是放在root目录之下，所有的目录都要有，在/root/nginx/conf.d下还需要新建一个文件，名为: default.conf 内容可以为空。 nginx.conf 里面需要存放内容，在这里写出来如下：

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
	log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$http_x_forwarded_for"';

	access_log  /var/log/nginx/access.log  main;

	sendfile        on;
	#tcp_nopush     on;

	keepalive_timeout  65;

	#gzip  on;

	include /etc/nginx/conf.d/*.conf;
	}
以上步骤操作完之后，进入容器中进行一些细节配置的修改,在 nginx下的conf.d文件中请修改server_name为你的网站域名， 反向代理的配置请添加：
        location /api/ {
                 proxy_pass http://ip:端口;
        }
进入容器命令： docker exec -it 容器名 /bin/bash
进入 /etc/nginx/conf.d/default.cnf ，进行上述内容修改，保存，退出。
以上所有配置完成之后，执行前端项目启动命令！
补充命令：
docker images：查看所有镜像
docker ps -a：查看所有的容器
docker logs -tf --tail=日志条数 容器id  : 查看指定数量的实时日志
docker logs 容器id : 查看容器的所有日志信息





```
**心跳功能调用方法示例**
```
import json
import requests
import binascii
from pyDes import des, CBC, PAD_PKCS5
# pip install pyDes==2.0.1
heartbeat_secret_key = 'Haian1!_'
def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    iv = heartbeat_secret_key
    k = des(heartbeat_secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)
data = json.dumps({"job_name": "绿色状态测试", "interval": 1})
encrypted_data = {"key": des_encrypt(data).decode('utf8')}
print(requests.post("http://127.0.0.1:8000/api/Clerk/heartbeat/v1/", json=encrypted_data).json())
```

**requirements.txt**

```
aiomysql==0.0.22
aioredis==2.0.1
aiosqlite==0.17.0
anyio==3.4.0
APScheduler==3.8.1
asgiref==3.4.1
async-timeout==4.0.2
backports.zoneinfo==0.2.1
certifi==2021.10.8
charset-normalizer==2.0.10
click==8.0.3
colorama==0.4.4
ecdsa==0.17.0
et-xmlfile==1.1.0
fastapi==0.71.0
fastapi-amis-admin==0.0.15
fastapi-pagination==0.9.1
greenlet==1.1.2
h11==0.12.0
idna==3.3
install==1.3.5
Naked==0.1.31
numpy==1.22.1
openpyxl==3.0.9
pandas==1.3.5
pyasn1==0.4.8
pycryptodome==3.12.0
pydantic==1.8.2
pymongo==3.9.0
PyMySQL==0.9.3
python-dateutil==2.8.2
python-jose==3.3.0
python-multipart==0.0.5
pytz==2021.3
pytz-deprecation-shim==0.1.0.post0
PyYAML==6.0
requests==2.27.1
rsa==4.8
shellescape==3.8.1
six==1.16.0
sniffio==1.2.0
SQLAlchemy==1.4.29
sqlalchemy2-stubs==0.0.2a20
sqlmodel==0.0.6
starlette==0.17.1
typing-extensions==4.0.1
tzdata==2021.5
tzlocal==4.1
ujson==5.1.0
urllib3==1.26.8
uvicorn==0.16.0

```

