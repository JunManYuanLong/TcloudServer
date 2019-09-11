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


