# Monkey 配置

> https://github.com/JunManYuanLong/monkey_tcloud

http://assets.processon.com/chart_image/5dccc8d9e4b048f2dc8c85d8.png

![](https://github.com/JunManYuanLong/monkey_tcloud/blob/master/doc/monkey_framework.png)

## Tcloud 配置

### local_config.py 配置以下几项

```python
# Jenkins url
CI_AUTO_MAN_JENKINS_URL = 'JenkinsURL 填写对应的本地路径'
# Jenkins Auth
CI_AUTO_MAN_JENKINS_AUTH = {
    "username": "用户名",
    "password": "密码"
}
# Jenkins job name
CI_AUTO_MAN_JENKINS_MONKEY_JOB = 'monkey_autotest'
# OSS report dir
CI_REPORT_FILE_ADRESS = ""
# JOBS url
CI_JOB_ADDRESS = f"{CI_AUTO_MAN_JENKINS_URL}/job"

```


## Jenkins 配置

### Jobs 配置

#### 新建 job ： ```monkey_autotest```

> 类型选择 Pipeline

> 然后选择参数化构建过程

| id | type | remark |
|----|----|----|
|PackageName | String type |运行的 android 包名 |
|DefaultAppActivity| String type | app 默认启动的 Activity |
|DeviceName| String type | 运行的设备的 device id (序列号)|
|RunTime| String type | 运行时间 单位分钟|
|AppDownloadUrl| String type | app 下载路径|
|PATH| String type | PATH|
|RunMod | String type | Monkey运行模式。 mix: 类monkey模式。70%控件解析随机点击，其余30%按原Monkey事件概率分布。支持android版本>=5  dfs: DFS深度遍历算法。支持android版本>=6 |
|MonkeyId| String type | tcloud 相关参数，定位 build id|
|TaskId| String type | tcloud 相关参数，定位 当前设备测试的 id |
|TcloudUrl| String type | tcloud 相关参数，api根 url |
|SystemDevice| Bool type | 是否是 系统设备，未使用 |
|InstallAppRequired| Bool type | 是否需要安装 App |
|LoginRequired| Bool type | 是否需要登录，未使用 |
|LoginUsername| String type | 登录用的用户名, 未使用|
|LoginPassword| String type | 登录用的密码，未使用|

#### 配置 pipeline

![](https://github.com/tsbxmw/monkey_tcloud/blob/master/doc/pipeline.png)

#### 注意，需要配置 Node 的 lable 为 ```stf``` 才可以使用对应的 pipeline 脚本

### Nodes 配置

#### 增加新的 node 用来运行 monkey 测试，这里使用的是 stf 所在机器，使用的 label 和 name 为 ```stf```

#### Node 所在设备配置

> 运行环境设置: 安装以下软件;注意：一定要使用 python3.7 及以上 版本

```shell script
git
adb
python3.7.3
```

> 获取 monkey 脚本

```shell
git clone https://github.com/tsbxmw/monkey_tcloud
```

> 进入目录 monkey_tcloud, 安装 module 依赖包

```shell script
cd monkey_tcloud
pip install -r requirement.txt
```

> 看到下面输出，认为已经安装成功

```shell script
pip install -r requirement.txt
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting requests
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/51/bd/23c926cd341ea6b7dd0b2a00aba99ae0f828be89d72b2190f27c11d4b7fb/requests-2.22.0-py2.py3-none-any.whl (57kB)
     |████████████████████████████████| 61kB 2.0MB/s
Collecting urllib3
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/e0/da/55f51ea951e1b7c63a579c09dd7db825bb730ec1fe9c0180fc77bfb31448/urllib3-1.25.6-py2.py3-none-any.whl (125kB)
     |████████████████████████████████| 133kB 3.3MB/s
Collecting python-jenkins
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/ab/22/7099a997bdbaa1105758b577c7c35705a68bda40226e8c0df2415245a081/python_jenkins-1.5.0-py2.py3-none-any.whl
Collecting prettytable
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/ef/30/4b0746848746ed5941f052479e7c23d2b56d174b82f4fd34a25e389831f5/prettytable-0.7.2.tar.bz2
Collecting oss2
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/37/7f/feca82c4a73dd2d22d65cfd3eb3b7f7e5b9c3b89bf7a574a1638b11f1b19/oss2-2.8.0.tar.gz (171kB)
     |████████████████████████████████| 174kB 6.4MB/s
Collecting argparse
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/f2/94/3af39d34be01a24a6e65433d19e107099374224905f1e0cc6bbe1fd22a2f/argparse-1.4.0-py2.py3-none-any.whl
Collecting chardet<3.1.0,>=3.0.2
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
     |████████████████████████████████| 143kB ...
Collecting idna<2.9,>=2.5
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl (58kB)
     |████████████████████████████████| 61kB 3.8MB/s
Collecting certifi>=2017.4.17
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/18/b0/8146a4f8dd402f60744fa380bc73ca47303cccf8b9190fd16a827281eac2/certifi-2019.9.11-py2.py3-none-any.whl (154kB)
     |████████████████████████████████| 163kB 6.8MB/s
Collecting six>=1.3.0
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Collecting pbr>=0.8.2
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/46/a4/d5c83831a3452713e4b4f126149bc4fbda170f7cb16a86a00ce57ce0e9ad/pbr-5.4.3-py2.py3-none-any.whl (110kB)
     |████████████████████████████████| 112kB 6.4MB/s
Collecting multi-key-dict
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/6d/97/2e9c47ca1bbde6f09cb18feb887d5102e8eacd82fbc397c77b221f27a2ab/multi_key_dict-2.0.3.tar.gz
Collecting crcmod>=1.7
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/6b/b0/e595ce2a2527e169c3bcd6c33d2473c1918e0b7f6826a043ca1245dd4e5b/crcmod-1.7.tar.gz
Collecting pycryptodome>=3.4.7
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/5c/cd/142130177b525c570229df0e2b3bd3cd2365b041dfee4685444d9bd477b1/pycryptodome-3.9.0-cp37-cp37m-win32.whl (10.1MB)
     |████████████████████████████████| 10.1MB 3.2MB/s
Collecting aliyun-python-sdk-kms>=2.4.1
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/d7/cd/a708ffe449138d8eb15a2018d31f131c4d38a5befc0668348620e1398e71/aliyun-python-sdk-kms-2.8.0.tar.gz
Collecting aliyun-python-sdk-core-v3>=2.5.5
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/3e/c9/c05affc50e393b79771f0731df4fb37bb34ef51c5b6e4ff02009dd390723/aliyun_python_sdk_core_v3-2.13.10-py3-none-any.whl (526kB)
     |████████████████████████████████| 532kB 6.4MB/s
Collecting aliyun-python-sdk-core>=2.11.5
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/15/ac/50f39b0c26433b4d7951a0b7461d6bf0709541bb82ce4f9e41a9df0d8492/aliyun_python_sdk_core-2.13.10-py3-none-any.whl (526kB)
     |████████████████████████████████| 532kB 6.4MB/s
Collecting jmespath<1.0.0,>=0.9.3
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/83/94/7179c3832a6d45b266ddb2aac329e101367fbdb11f425f13771d27f225bb/jmespath-0.9.4-py2.py3-none-any.whl
Building wheels for collected packages: prettytable, oss2, multi-key-dict, crcmod, aliyun-python-sdk-kms
  Building wheel for prettytable (setup.py) ... done
  Created wheel for prettytable: filename=prettytable-0.7.2-cp37-none-any.whl size=13706 sha256=c7c7f273ff96abe16bec57e1785f10925351135c23391641879a4a3ee0b9afc3
  Stored in directory: C:\Users\MengWei\AppData\Local\pip\Cache\wheels\00\cd\6a\278898c4aa48b8f3f30ccdbec499655637eef63b486d3f6bec
  Building wheel for oss2 (setup.py) ... done
  Created wheel for oss2: filename=oss2-2.8.0-cp37-none-any.whl size=79676 sha256=4d789c7325b888f9367fb55be2e642f8f851e210fbb2cbc2878f73919631c13c
  Stored in directory: C:\Users\MengWei\AppData\Local\pip\Cache\wheels\7c\49\1c\43ba7d1da4c2881aa74c9937b2ffba834493912a177d068ed3
  Building wheel for multi-key-dict (setup.py) ... done
  Created wheel for multi-key-dict: filename=multi_key_dict-2.0.3-cp37-none-any.whl size=9304 sha256=8683ae06205e6b2f9ce76afd975860bf4ac816751a4d1f0a2c6c36ac0654ac35
  Stored in directory: C:\Users\MengWei\AppData\Local\pip\Cache\wheels\e2\43\d7\6bdfc01fd1a346a7134f0048cc7a8c3f453ed2d0c0b11084e9
  Building wheel for crcmod (setup.py) ... done
  Created wheel for crcmod: filename=crcmod-1.7-cp37-cp37m-win32.whl size=24635 sha256=8a73279eb6625cd22f6e5570a76393c31fcff97b1a0e864b4da5a97a67439bda
  Stored in directory: C:\Users\MengWei\AppData\Local\pip\Cache\wheels\8b\8e\47\f5438529bcd5b472988aece2224377ba4772b2caf4d34dc151
  Building wheel for aliyun-python-sdk-kms (setup.py) ... done
  Created wheel for aliyun-python-sdk-kms: filename=aliyun_python_sdk_kms-2.8.0-cp37-none-any.whl size=30136 sha256=665096611e05feacd993420912fb4161cf2192d0107ba4477ef2eb27b0ac32a0
  Stored in directory: C:\Users\MengWei\AppData\Local\pip\Cache\wheels\b2\41\97\a44b04b7f277c55b610df0bdf479bb855c3b137cd4d96946f5
Successfully built prettytable oss2 multi-key-dict crcmod aliyun-python-sdk-kms
Installing collected packages: chardet, idna, urllib3, certifi, requests, six, pbr, multi-key-dict, python-jenkins, prettytable, crcmod, pycryptodome, jmespath, aliyun-python-sdk-core, aliyun-python-sdk-kms, aliyun-python-sdk-core-v
3, oss2, argparse
Successfully installed aliyun-python-sdk-core-2.13.10 aliyun-python-sdk-core-v3-2.13.10 aliyun-python-sdk-kms-2.8.0 argparse-1.4.0 certifi-2019.9.11 chardet-3.0.4 crcmod-1.7 idna-2.8 jmespath-0.9.4 multi-key-dict-2.0.3 oss2-2.8.0 pb
r-5.4.3 prettytable-0.7.2 pycryptodome-3.9.0 python-jenkins-1.5.0 requests-2.22.0 six-1.12.0 urllib3-1.25.6

```

> 测试脚本运行状况

```shell script
python -m automonkey run
```

> 可以看到一下输出的话，认为配置成功

```shell script

python -m automonkey run -h
usage: python -m automonkey run [-h] [--package-name PACKAGE_NAME]
                                [--device-name DEVICE_ID]
                                [--run-time RUN_TIME]
                                [--app-download-url APP_DOWNLOAD_URL]
                                [--run-mode RUN_MODE]
                                [--build-belong BUILD_BELONG]
                                [--install-app-required INSTALL_APP_REQUIRED]
                                [--system-device SYSTEM_DEVICE]
                                [--login-required LOGIN_REQUIRED]
                                [--login-username LOGIN_USERNAME]
                                [--login-password LOGIN_PASSWORD]
                                [--default-app-activity DEFAULT_APP_ACTIVITY]
                                [--task-id TASK_ID] [--monkey-id MONKEY_ID]
                                [--tcloud-url TCLOUD_URL]

optional arguments:
  -h, --help            show this help message and exit
  --package-name PACKAGE_NAME, -pn PACKAGE_NAME
  --device-name DEVICE_ID, -dn DEVICE_ID
  --run-time RUN_TIME, -rt RUN_TIME
  --app-download-url APP_DOWNLOAD_URL, -adu APP_DOWNLOAD_URL
  --run-mode RUN_MODE, -rm RUN_MODE
  --build-belong BUILD_BELONG, -bb BUILD_BELONG
  --install-app-required INSTALL_APP_REQUIRED, -iar INSTALL_APP_REQUIRED
  --system-device SYSTEM_DEVICE, -sd SYSTEM_DEVICE
  --login-required LOGIN_REQUIRED, -lr LOGIN_REQUIRED
  --login-username LOGIN_USERNAME, -lu LOGIN_USERNAME
  --login-password LOGIN_PASSWORD, -lp LOGIN_PASSWORD
  --default-app-activity DEFAULT_APP_ACTIVITY, -daa DEFAULT_APP_ACTIVITY
  --task-id TASK_ID, -tid TASK_ID
  --monkey-id MONKEY_ID, -mid MONKEY_ID
  --tcloud-url TCLOUD_URL, -turl TCLOUD_URL

```

