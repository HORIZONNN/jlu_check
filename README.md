# 太长不想看只想打卡系列

1. 按照**环境配置**装好环境。
2. 打开`main_config.py`文件并修改其中的`JLU_USERNAME`、`JLU_PASSWORD`和`JLU_INFO`为自己的校园网账号、校园网密码和校园网打卡信息。
3. 在本机器上登录自己的QQ号以实现腾讯文档能够快速登录。
4. 在命令行中运行`python main.py`即可自动每天四次定时打卡。



# 环境配置

* 环境要求

  * Windows 10（weixin.py中用到了pywin32的库，如果不需要这部分，删掉之后可以适用于其他平台
  * python 3.6（比较推荐的python版本，小问题比较少）
  
* Anaconda

  1. 安装[Anaconda](https://www.anaconda.com/products/individual)。因为安装包比较大，所以就没放安装包，需要自行去官网下载安装。

  2. 创建python环境：打开Anaconda Promopt，运行以下命令

     ```
     conda create -n <your_env_name> python=3.6
     ```

     其中<your_env_name>是自己要创建的python环境名称

* Chrome

  1. 安装Chrome浏览器
  2. 对应chrome版本下载[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home)，并将其放到对应python环境的Scripts文件夹下。

* python库

  * 如果安装了Anaconda，打开Anaconda Promopt，运行以下命令

    ```
    conda activate <your_env_name>
    conda install requests -y
    conda install selenium -y
    conda install schedule -c jholdom -y
    conda install pandas -y
    conda install xlrd -y
    conda install pywin32 -y
    ```


  * 如果没有安装Anaconda，则可以通过pip安装

    ```
    pip install requests
    pip install selenium
    pip install schedule
    pip install pandas
    pip install xlrd
    pip install pywin32
    ```
    
    

  

# 程序简要介绍

* 功能实现

  * 自动打卡（一天四次以及旧版一天一次的打卡均可以）
  * 定时修改打卡目录名称（与XZC第三方应用有关）
  * 获取未打卡的学生列表（需要配合XZC第三方应用以及百度网盘来实现）
  * 将未打卡学生列表发到微信群

* 程序结构

  ```shell
  main.py # 程序入口
  main_config.py # 本程序的一些参数配置，也是唯一需要个人改动的内容
  jlu.py # 打卡功能的实现
  xzc.py # 打卡截图上传以及打卡目录修改
  baidu.py # 获取百度云盘特定目录中的全部文件名
  weixin.py # 微信消息发送
  tecent.py # 腾讯文档相关操作，包括打卡标记和清除打卡标记
  ```






# 程序使用



* 程序参数

  * 无参数：定时执行新版一天四次的打卡
  * --old：定时执行旧版一天一次的打卡
  * --change_dir：定时修改XZC的目录名称，保证每次打卡上传的截图都单独有一个文件夹
  * --get_unchecked：获取未打卡的学生列表（需要XZC上传截图以及百度云开发者账户）
  * --weixin：将未打卡的学生列表发送到特定微信群
  * --replace：清除腾讯文档中每天的打卡标记

* 打卡需求

  1. 修改`main_config.py`文件中以下参数

     ```python
     ### 健康打卡相关部分
     JLU_USERNAME = "liutd19" # 校园网用户名
     JLU_PASSWORD = "liutiedan123456" # 校园网密码
     # 截图部分
     # SAVE_PATH = os.path.join(os.path.abspath('.'), "check_screenshot") # 默认截图保存页面
     SAVE_PATH = None # 设为None则表示不保存截图
     # 打卡页面所要填写的信息，信息不要写错
     JLU_INFO = {
         'major' : "软件工程",         # 专业
         'grade' : "2019",            # 年级
         'campus' : "中心校区",        # 校区
         'apartment' : '南苑8公寓',    # 公寓楼号码
         'bedroom' : '777',           # 寝室号
         'master' : True              # True表示为硕士，False表示为博士
     }
     ```

     若是旧版打卡，仅需要修改`JLU_USERNAME`和`JLU_PASSWORD`。若是新版打卡，还需要修改`JLU_INFO`参数为打卡页面中所填写的信息
     若是有截图并上传到XZC链接的需求，则需要指定`SAVE_PATH`为截图文件保存路径，并且设置如下参数

     ```python
     # 当上传文件时所要填的文件名，这里就用学号和姓名来命名了
     NAME_PART1 = "2019111111" # 学号
     NAME_PART2 = "刘铁蛋" # 姓名
     # 通用参数
     # 假如我的XZC的URL链接是http://www.xzc.cn/x877ZRj111
     XZC_CODE1 = "x877ZRj111" # XZC链接中的代码标识，可以有多个，但是我的main.py中修改dir和上传所用的是同一个所以就只写了一个
     ```

     其中`NAME_PART1`和`NAME_PART2`是上传到云端的文件名。`XZC_CODE1`即是上传文件的XZC链接中的代码标识

     若有在腾讯文档中标记已打卡的需求，则需要指定`TECENT_XLXS_URL`参数为在线文档的url地址，同时在同一台机器上登录自己的QQ号来实现腾讯文档快速登录。

  2. 运行程序
     如果是新版打卡直接运行

     ```
     python main.py
     ```

     如果是旧版打卡需要加上`--old`参数

     ```shell
     python main.py --old
     ```

* 修改目录

  1. 需要修改`main_config.py`文件中如下参数

     ```python
     # 用户名和密码只有在change_dir_name()中会用到
     XZC_USERNAME = "157891011@qq.com" # 用户名
     XZC_PASSWORD = "liutiedan" # 密码
     
     XZC_CODE1 = "x811ZRj111" # XZC链接中的代码标识，可以有多个，但是我的main.py中修改dir和上传所用的是同一个所以就只写了一个
     ```

     其中`XZC_USERNAME`和`XZC_PASSWORD`为XZC的用户名和密码。`XZC_CODE1`为所要修改的XZC链接的代码标识

  2. 运行程序

     ```shell
     python main.py --change_dir
     ```

* 获取未打卡的学生列表

  1. 需要修改`main_config.py`文件中如下参数

     ```python
     ### get unchecked list 相关参数
     ACCESS_TOKEN = "121.493aab17d5f21111111111111111111111111111111DNktFCDPDiFaIQj020maXiwY7BVr5.k2__Pg" # 百度云的token，这样才能获取上传到百度云的文件列表
     CLOUD_PATH = '/apps/DzzCloud/' # XZC目录
     CHART_FILE_PATH = os.path.join(os.path.abspath('.'), '打卡.xlsx') # 当前程序目录下需要有一个【打卡.xlsx】记录所有打卡学生的姓名和学号
     CHATGROUP = "软学二班通知群" # 所要发送的微信群名称
     ```

     其中ACCESS_TOKEN为申请到的百度云应用开发的access_token，相关链接如下所示

     * [百度开发者注册](https://pan.baidu.com/union/apply)
     * [百度网盘开发技术文档](https://pan.baidu.com/union/document/entrance)
     * [Authorization Code获取指南](http://developer.baidu.com/wiki/index.php?title=docs/oauth/authorization)

     `CLOUD_PATH`为XZC的应用路径，不需要修改

     `CHART_FILE_PATH`为所需打卡的学生excel表格，需要有两列，分别为`学号`和`姓名`

     如果有将未打卡学生列表发送到指定微信群的需求，还需要设置`CHATGROUP`为指定微信群名称，并在程序运行前打开指定微信群。

  2. 程序运行

     ```shell
     python main.py --get_unchecked # 如果要发到微信上还需要再加--weixin参数
     ```

     





