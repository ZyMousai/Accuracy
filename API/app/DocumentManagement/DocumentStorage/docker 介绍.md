####docker 介绍

#####一、docker介绍

1.什么是docker？

- 使用容器让创建、部署、运行应用程序更简单的一个工具
- 让应用所需的库和依赖环境打包
- 有一点点像虚拟机

![what_is_docker - 副本](D:\整理文件\项目笔记\images\what_is_docker - 副本.png)

**3.docker vs vmware(or virtualbox)?**



![VM-vs-Docker-What-is-Docker-Container-Edureka-1](D:\整理文件\项目笔记\images\VM-vs-Docker-What-is-Docker-Container-Edureka-1.png)





![对比8](D:\整理文件\项目笔记\images\对比8.png)



容器：容器在Linux上*本地运行*，并与其他容器共享主机的内核。它运行一个离散进程，不占用任何其他可执行文件更多的内存，从而使其轻巧。

相比之下，**虚拟机**（VM）运行成熟的“来宾”操作系统，并通过虚拟机管理程序对主机资源进行*虚拟*访问。通常，VM会产生大量开销，超出了应用程序逻辑所消耗的开销。



#####一、docker安装  社区版本

<https://docs.docker.com/install/linux/docker-ce/ubuntu/>



```python
1,更新ubuntu的apt源索引

sudo apt-get update

2, 安装包允许apt通过HTTPS使用仓库
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
    
3, 添加Docker官方GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
4, 设置Docker稳定版仓 添加docker源
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
    
5, 添加仓库后，更新apt源索引
sudo apt-get update
```

6,安装最新版Docker CE（社区版）

```shell
sudo apt-get install docker-ce

7, 通过运行hello-world 映像来验证是否正确安装了Docker Engine-Community 。
sudo docker run hello-world    # 创建容器
```

```shell
8, 为了避免每次命令都输入sudo，可以设置用户权限，注意执行后须注销重新登录
sudo usermod -a -G docker $USER



```

##### 卸载Docker Engine-社区

+ 卸载Docker Engine-社区软件包：

  + ```
    sudo apt-get purge docker-ce
    ```

+ 主机上的映像，容器，卷或自定义配置文件不会自动删除。要删除所有图像，容器和卷：

  + ```
     sudo rm -rf /var/lib/docker
     ```
    ```

    ```



以下示例启动Redis容器并将其配置为始终重新启动，除非明确将其停止或重新启动Docker。

+ on-failure 如果容器由于错误而退出，请重新启动容器，该错误表示为非零退出代码。

```python
 docker run -dit --restart unless-stopped ubuntu
```

docker 查找镜像

```python
https://hub.docker.com/
```



镜像字段介绍

- **REPOSITORY：**表示镜像的仓库源
- **TAG：**镜像的标签
- **IMAGE ID：**镜像ID
- **CREATED：**镜像创建时间
- **SIZE：**镜像大小



安装ubuntu镜像

```python
docker search ubuntu   在仓库查找镜像

docker pull ubuntu   安装镜像

docker images      查看docker镜像

# 运行docker镜像
-name自定义容器名，-p指定端口映射，前者为虚拟机端口，后者为容器端口,成功后返回id
查看所有启动的容器(查看所有容器加 -a)
docker run -dti --name ubuntu_test -p 8088:8088 ubuntu   
    
查看容器信息  根据id
docker inspect id

#  /bin/bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell
进入 容器 ubuntu
docker exec -it d2 /bin/bash

# 查看版本
 cat /etc/issue

    
# 退出   
先按，ctrl+p
再按，ctrl+q
exit   会退出整个系统

# 制作docker镜像   1.0是版本号   ubuntu_test 是镜像名字
docker commit  fae ubuntu_demo:1.0  
    
# 打包镜像
docker save -o ubuntu_test1.tar ubuntu_test1:1.0
```



**docker 搜索** 

<https://hub.docker.com/>

```python
# Tomcat 服务器是一个免费的开放源代码的Web 应用服务器，属于轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。

docker search tomcat

# 安装  
docker pull tomcat

# 创建容器
docker run -dti --name tomcat_demo -p 8080:8080 tomcat

# 访问 
http://192.168.216.137:8080/
```



####docker启动与停止

```shell
# 启动docker
sudo service docker start

# 停止docker
sudo service docker stop

# 重启docker
sudo service docker restart

```

##### docker 镜像介绍

**Docker 把应用程序及其依赖，打包在 image 文件里面。**只有通过这个文件，才能生成 Docker 容器。image 文件可以看作是容器的模板。Docker 根据 image 文件生成容器的实例。同一个 image 文件，可以生成多个同时运行的容器实例。

image 是二进制文件。实际开发中，一个 image 文件往往通过继承另一个 image 文件，加上一些个性化设置而生成。举例来说，你可以在 Ubuntu 的 image 基础上，往里面加入 Apache 服务器，形成你的 image。

image 文件是通用的，一台机器的 image 文件拷贝到另一台机器，照样可以使用。一般来说，为了节省时间，我们应该尽量使用别人制作好的 image 文件，而不是自己制作。即使要定制，也应该基于别人的 image 文件进行加工，而不是从零开始制作。

为了方便共享，image 文件制作完成后，可以上传到网上的仓库。Docker 的官方仓库 [Docker Hub](https://hub.docker.com/) 是最重要、最常用的 image 仓库。此外，出售自己制作的 image 文件也是可以的。

**拉去镜像**

要想获取某个镜像，我们可以使用pull命令，从仓库中拉取镜像到本地，如

+ ```shell
  docker image pull library/hello-world

  由于 Docker 官方提供的 image 文件，都放在library组里面，所以它的是默认组，可以省略。因此，上面的命令可以写成下面这样。

  省略写法   docker image pull hello-world
  ```

**删除镜像**

```python
docker image rm 镜像名或镜像id


常用参数说明
```

- -i 表示以“交互模式”运行容器
- -t 表示容器启动后会进入其命令行。加入这两个参数后，容器创建就能登录进去。即 分配一个伪终端。
- --name 为创建的容器命名
- -v 表示目录映射关系(前者是宿主机目录，后者是映射到宿主机上的目录，即 宿主机目录:容器中目录)，可以使 用多个-v 做多个目录或文件映射。注意:最好做目录映射，在宿主机上做修改，然后 共享到容器上。
- -d 在run后面加上-d参数,则会创建一个守护式容器在后台运行(这样创建容器后不 会自动登录容器，如果只加-i -t 两个参数，创建后就会自动进去容器)。
- -p 表示端口映射，前者是宿主机端口，后者是容器内的映射端口。可以使用多个-p 做多个端口映射
- -e 为容器设置环境变量
- --network=host 表示将主机的网络环境映射到容器中，容器的网络与主机相同





**停止与启动容器**

```shell
# 停止一个已经在运行的容器
docker  stop 容器名或容器id

# 启动一个已经停止的容器
docker  start 容器名或容器id

# kill掉一个已经在运行的容器
docker container kill 容器名或容器id

# 查看容器
docker container ls -a
```



dockerfile

```python
Docker可以通过阅读Docker的指令来自动构建映像 Dockerfile。A Dockerfile是一个文本文档，其中包含用户可以在命令行上调用以组装图像的所有命令。使用docker build 用户可以创建自动构建，该构建连续执行多个命令行指令。
```







