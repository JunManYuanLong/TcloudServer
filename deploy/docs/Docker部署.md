> 本部署文档适用于专注使用本平台的用户，将会把相关代码和依赖打包成docker镜像

### 1、搭建docker环境

**简介**

Docker 是一个开源的应用容器引擎，基于Go 语言并遵从Apache2.0协议开源。

Docker 可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。

容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）,更重要的是容器性能开销极低。

Docker 从 17.03 版本之后分为 CE（Community Edition: 社区版） 和 EE（Enterprise Edition: 企业版），我们用社区版就可以了。

  

![](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/WeWork%20Helper20190911110330.png)

以上是docker支持的平台，应该是廊括了主流的所有系统，macos和windows需要下载一个安装包，直接安装即可，

linux的话推荐手动根据官网提示进行安装，主要是熟悉操作以及学习这个主流的技术，或者使用脚本一键安装

```bash
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
......
# 如果您想将Docker用作非root用户，您现在应该考虑将您的用户添加到“docker”组，例如：
$ sudo usermod -aG docker <your-user>
```

安装完成后，启动docker(不同平台启动命令不同)

```bash
$ sudo systemctl start docker
$ sudo docker run --rm hello-world
```

可以看到

```bash
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

则说明安装成功

#### 安装docker-compose

官网有详细安装[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)  ，根据平台不同有不同的安装方式



### 2、部署项目

转到deploy目录下，拉取所有镜像

```
$ sudo docker-compose pull
```

然后修改`local_config.py`文件，
```
# 这里的账号密码是在docker-compose.yml中配置的，改成以下
SQLALCHEMY_DATABASE_URI = 'mysql://root:tc123456@mysql:3306/demo?charset=utf8'
```
再初始化kong的数据库（如果报错，再执行一次，成功的话会显示`Database is up-to-date`）

```
$ sudo docker-compose up -d kong_database
// 容器启动以后，数据库会本地挂载到 ./volumes/kong_database 里面
// 但由于权限问题，初始化数据库会失败，所以要先对该文件赋予权限
$ sudo chmod -R 777 ./volumes/kong_database
$ sudo docker-compose run --rm kong kong migrations bootstrap
```

然后启动所有项目

```
$ sudo docker-compose up -d
```

查看启动状态

```
$ sudo docker-compose ps
```

如果所有状态均为up，则运行正常，否则`sudo docker logs <name>`查看日志

打开konga(kong的管理页面，`http://localhost:9001`)，注册账号并登录，再新建连接，地址为`http://kong:8001`


![](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/kong-1.png)

成功后，进入SNAPSHOT页面，点击IMPORT FROM FILE，选择我们的`kong.json`文件，并进入DETAILS中RESTORE，全选导入，可能会出错，再执行一次即可，此时我们的网关服务已经运行完成，地址为`http://localhost:9000`
ps: 数据库初始化文件是init/init.sql，可以通过`sudo docker-compose down -v`再删除`volume/mysql`挂载目录之后，`sudo docker-compose up -d`来重新初始化数据库


### 3、部署前端

1、安装node环境

2、在前端项目根目录下`npm install`，稍等片刻安装依赖包

3、修改`config/dev.env.js`中的`BASE_URL`地址为上面的后端地址`http://localhost:9000`

4、运行`npm run dev`即可打开本项目