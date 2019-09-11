# Tcloud
感觉项目不错的点个star，项目持续更新，如有疑问可联系QQ群：839084842

前端传送门：https://github.com/bigbaser/Tcloud

线上demo地址：http://tcloud-demo.ywopt.com/#/login （账号：admin 密码：123456）

# 一、什么是Tcloud?

      Tcloud(Test Cloud)致力于打造云测平台，测试数据上云，移动终端云(云真机)。统一定制化的流程系统，管理执行者工作效率，任务到期提醒，方便快捷查看“我的”相关任务，使需求->开发->测试->验收->发布更高效。

# 二、为什么要开发Tcloud?

>		1. 目前使用的需求，issue管理工具非常之多，如jira，tapd，禅道等，商业软件的复杂度使用起来并没有所谓的那么方便，并且与公司的部分业务不太契合，因此自研Tcloud就成了趋势
>		2. 公司业务线多，一个测试可能同时承担几个项目的测试任务，Tcloud可同时统计人员在不同项目下的工作量，通过平台化的记录，统计工作产出
>		3. 初创业务项目还在为没有移动设备或机型不全而纠结，面临有限的经费和高昂的移动开发设备窘境，云真机上线了
>		4. 定制化项目产研流程，统计需求提出到上线各个环节的耗时，提高工程效率

# 三、Tcloud的应用
### 云真机
>        云真机平台的开发，让测试机更高效的被使用，当测试机器不在使用的时候，会作为共享机供给开发作为调试机
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/tcdevices.gif)

### 流程管理
>        在日常测试工作中，提测流程混乱，流程不清晰，测试过程中出现的问题无法统计，因此流程系统应运而生
>        流程系统包含发布系统，自动化集成，告警通知，邮件通知等功能
>        有了流程系统后，可直观看到流程的报表，流程资源，以及每个阶段的平均耗时，还有流程被打回或者异常终止的原因。
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/flow.gif)

### Dashboard
>        展示根据时间区间统计每个版本的issue数量，新增数量，打开数量的统计报表；
>        展示bug状态分布饼状图；
>        根据SOD算法，展示版本质量走势；
>        展示每个版本需求数量的统计报表；
>        展示每个版本任务数量的统计报表；
>        展示测试团队时间段内新增case和issue的统计报表；

### 看板
>        根据版本号查询缺陷和需求相关的看板，通过类teambition风格的展示，让人和容易接受，抽屉式的详情展示，让你的操作游刃有余。
>        友好的“我的问题”和“最近更新”入口能快速定位到目标，大大提高了工程效率。
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/dashboard.gif)

### 迭代管理
>        迭代管理模块，集成了迭代版本的管理，任务管理，缺陷管理，需求管理，其中任务包括多种类别。
>        任务可选择相应的测试用例，点击任务名可查看相应的任务报告以及用例执行情况。
>        缺陷的增删改查，并且做了针对相应角色的控制。
>        需求可对应迭代版本添加，需求价值能直观看出。
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/version.gif)

### 用例管理
>        支持二级目录的用例管理，用例可根据“步骤”“预期”傻瓜式创建，用例导入导出
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/case.png)

### 缺陷管理&需求管理
>        在迭代管理中已经初步看到了缺陷和需求的功能和界面展示，两个大的模块是使用比较频繁的，因此单独列出来，迭代管理中的缺陷和需求，更加匹配迭代版本，满足不一样的用户群

### 接口自动化
>        当前自动化开源工具满天飞的情况下，为了满足业务需求，让全民自动化起来，将接口自动化平台话，让更多的人能接触到自动化
>        在httprunner的基础上做了二次开发，展示效果如下
![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/interface.png)




# 四、安装介绍
#### 环境
python => 3.7
推荐使用pipenv管理python环境，安装Pipfile中的依赖包，注意版本问题
或者直接使用`pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple`安装依赖包，最好先新建一个虚拟环境`virtualenv`
可配置文件为local_config.py文件，这里的配置需要根据自己环境进行修改

#### 服务端口

| id | service name | port |
|:---- |:---- |:---- |
| 1 | auth | 9020 |  
| 2 | autotest	| 9022 |  
| 3 | extention | 9024 |  
| 4 | flow | 9026 |   
| 5 | interface	| 9028 |  
| 6 | message | 9030 |  
| 7 | project |	9032 |  
| 8 | public | 9034 |  
| 9 | tcdevices	| 9036 |  
| 10 | jobs	| 9038 |  
| 11 | ws	| 9040 |  



#### 服务间调用 

> trpc

- now : communicate with http request by ```requests```

```
    user_trpc = Trpc('auth')   # using with service name
    user_trpc.requests(method='get', path='/user')
``` 

#### 一、启动服务

以auth服务为例，切换到项目根目录，执行python -m apps.auth.run

建议可以使用supervisor管理多服务的启动
```shell
python -m apps.auth.run
```


##### 二、启动Kong

书写好`docker-compose.yml`文件后即可启动

```bash
$ sudo docker-compose up -d
```

首先需要migrations，把kong所需要的数据库文件写入到数据库中

```bash
$ sudo docker-compose run kong kong migrations bootstrap

# 这个版本是bootstrap，不同版本可能命令不同，最好在docker-compose.yml中写死版本
```


##### 三、配置Kong

输入http://ip:9000 进入kong_dashboard的界面，注册账号密码

```yml
username: admin
email   : admin@tcloud.com
password: 123456
```

#### 联系我们
欢迎扫描下方二维码关注我们

![image](http://tcloud-static.oss-cn-beijing.aliyuncs.com/tcloud_git/tc.jpg)

QQ群：839084842

