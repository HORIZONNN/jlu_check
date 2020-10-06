import os
import random

### 健康打卡相关部分
JLU_USERNAME = "liutd19" # 校园网用户名
JLU_PASSWORD = "liutiedan123456" # 校园网密码
# 截图部分
# SAVE_PATH = os.path.join(os.path.abspath('.'), "check_screenshot") # 默认截图保存页面
SAVE_PATH = None # 设为None则表示不保存截图
# 打卡页面所要填写的信息，信息不要写错
JLU_INFO = {
    'major' : "软件工程", # 专业
    'grade' : "2019", # 年级
    'campus' : "中心校区", # 校区
    'apartment' : '南苑8公寓', # 公寓楼号码
    'bedroom' : '777', # 寝室号
    'master' : True # True表示为硕士，False表示为博士
}

### 腾讯文档相关参数
TECENT_XLXS_URL = "https://docs.qq.com/sheet/DRElJcW5BdWZVVmZs?tab=BB08J2"


### XZC相关部分
# 用户名和密码只有在change_dir_name()中会用到
XZC_USERNAME = "157891011@qq.com" # 用户名
XZC_PASSWORD = "liutiedan" # 密码
# 当上传文件时所要填的文件名，这里就用学号和姓名来命名了
NAME_PART1 = "2019542063" # 学号
NAME_PART2 = "刘铁蛋" # 姓名
# 通用参数
# 假如我的XZC的URL链接是http://www.xzc.cn/x811ZRj111
XZC_CODE1 = "x811ZRj111" # XZC链接中的代码标识，可以有多个，但是我的main.py中修改dir和上传所用的是同一个所以就只写了一个


### get unchecked list 相关参数
ACCESS_TOKEN = "121.493aab17d5f111111111111111111111111111111aYDNktFCDPDiFaIQj020maXiwY7BVr5.k2__Pg" # 百度云的token，这样才能获取上传到百度云的文件列表
CLOUD_PATH = '/apps/DzzCloud/' # XZC目录
CHART_FILE_PATH = os.path.join(os.path.abspath('.'), '打卡.xlsx') # 当前程序目录下需要有一个【打卡.xlsx】记录所有打卡学生的姓名和学号
CHATGROUP = "软学二班通知群" # 所要发送的微信群


### schedules
# 研究生每日打卡（一天四次）的时间表
minute = random.randint(1, 20)
CHECK_SCHEDULES = [
    (7, minute),
    (11, minute),
    (17, minute),
    (21, minute)
]
# 研究生每日打卡（一天一次）的时间表
CHECK_OLD_SCHEDULE = (7, minute)
# 修改XZC目录名称的时间表
CLEAR_CHECKED_SCHEDULES = CHANGE_DIR_SCHEDULES = [
    (6, 30),
    (11, 30),
    (16, 30),
    (20, 30)
]
# 获取未打卡同学名单的时间表
GET_UNCHECKED_SCHEDULES = [
    (7, 30),
    (11, 30),
    (17, 30),
    (21, 30)
]