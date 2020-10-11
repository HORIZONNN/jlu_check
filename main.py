import schedule
import argparse
import random
import traceback
import time
import pandas as pd

from my_main_config import *
from jlu import jlu_check, jlu_check_old
from xzc import change_dir_name, upload_file
from baidu import get_file_list
from weixin import send_text
from tecent import TecentDoc
import sys


if __name__ == "__main__":

    ### 获取运行参数，来确定要运行的功能
    parser = argparse.ArgumentParser()
    parser.add_argument('--replace', action='store_true', default=False,
                        help='clear check log in tecent document')
    parser.add_argument('--old', action='store_true', default=False,
                        help='run health check everyday')
    parser.add_argument('--change_dir', action='store_true', default=False, 
                        help='get a screenshot and upload it')
    parser.add_argument('--get_unchecked', action='store_true', default=False, 
                        help='get a list of unchecked students')
    parser.add_argument('--send_info', action='store_true', default=False, 
                        help='send info of checked status')
    parser.add_argument('--weixin', action='store_true', default=False, 
                        help='send unchecked students list to a weixin group')
    args = parser.parse_args()
    tecent = TecentDoc(TECENT_XLXS_URL, QQ_NUM, PWD)

    # 格式化打印信息，便于观察
    def info_print(info):
        print(time.strftime("%Y%m%d-%H:%M:%S", time.localtime()) + "*" * 30)
        print(info)
        print("*"*45 + "\n\n")

    ### 各部分功能的打包，便于在后面schedule中调用
    def check_and_confirm(i):
        result = jlu_check(JLU_USERNAME, JLU_PASSWORD, **JLU_INFO, nth=i, file_path=None)
        if result == "success":
            tecent.confirm(NAME_PART2)
        info_print("check : check success!")


    def check_and_upload(i):
        if args.old:
            abs_file_path = jlu_check_old(JLU_USERNAME, JLU_PASSWORD, SAVE_PATH)
        else:
            abs_file_path = jlu_check(JLU_USERNAME, JLU_PASSWORD, **JLU_INFO, nth=i, file_path=SAVE_PATH)
        if abs_file_path:
            assert SAVE_PATH != None
            upload_file(abs_file_path, XZC_CODE1, NAME_PART1, NAME_PART2)
        info_print("check : check success!")

    def change_dir_by_time(i):
        dir_name = time.strftime("%Y%m%d-{nth}".format(nth=i), time.localtime())
        result = "success"  if change_dir_name(XZC_USERNAME, XZC_PASSWORD, XZC_CODE1, dir_name) else "failed"
        info_print("change_dir : change dir name to {} {}!".format(dir_name, result))

    def get_unchecked_list(i):
        # dir_name = CLOUD_PATH + time.strftime("%Y%m%d-{nth}".format(nth=i), time.localtime())
        # file_list = get_file_list(ACCESS_TOKEN, dir_name)
        # assert file_list != None

        # text = ""
        # try:
        #     data = pd.read_excel(CHART_FILE_PATH)
        #     students_number = data['学号'].values
        #     students_name = data['姓名'].values
        #     # students_phone = data['手机号'].values
            
        #     for i in range(len(students_name)):

        #         def checked(number, name):
        #             for file_name in file_list:
        #                 if number in file_name and name in file_name  : return True
        #             return False

        #         if not checked(str(students_number[i]), students_name[i]):
        #             text += "\n{}:{}".format(students_number[i], students_name[i])
        # except FileNotFoundError as e:
        #     traceback.print_exc(e)
        #     info_print("get_unchecked : file not exists")
        # except KeyError as e:
        #     traceback.print_exc(e)
        #     info_print("get_unchecked : file format error!")
        # if len(text) == 0:
        #     info_print("get_unchecked : all students checked!")
        #     return
        # else:
        #     if args.weixin:
        #         send_text(CHATGROUP, text+"\n\n请上述同学打完卡在群里回复一下，谢谢！")
        #     else:
        #         info_print("get_unchecked : unchecked students list:\n" + text)
        #     info_print("get_unchecked : get list success!")
        unchecked_list = tecent.get_unchecked()
        send_text("软学二班通知群", "\n".join(unchecked_list))
        info_print("get_unchecked : get list success!")

    def send_checked_info():
        unchecked_list = tecent.get_unchecked()
        send_text("2019级软件硕士负责人群", "学三学四打卡差{}人".format(len(unchecked_list)))
        info_print("send_checked_info : send info success!")



    # # function test
    # check_and_confirm(4)
    # check_and_upload(2)
    # get_unchecked_list(4)
    # print(tecent.get_unchecked())
    # send_checked_info()
    # change_dir_by_time(2)
    # sys.exit()
    # for i in range(10):
    #     tecent.confirm(NAME_PART2)
    # sys.exit()
    # tecent_replace(TECENT_XLXS_URL)
    # time.sleep(3)
                

    if args.replace:
        for i in range(len(CLEAR_CHECKED_SCHEDULES)):
            schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CLEAR_CHECKED_SCHEDULES[i])).do(tecent.replace)
    if args.old:
        schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHECK_OLD_SCHEDULE)).do(check_and_upload, 1)
    else:
        for i in range(len(CHECK_SCHEDULES)):
            # schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHECK_SCHEDULES[i])).do(check_and_upload, i+1)
            schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHECK_SCHEDULES[i])).do(check_and_confirm, i+1)
    if args.change_dir:
        for i in range(len(CHANGE_DIR_SCHEDULES)):
            schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHANGE_DIR_SCHEDULES[i])).do(change_dir_by_time, i+1)
    if args.get_unchecked:
        for i in range(len(GET_UNCHECKED_SCHEDULES)):
            # schedule.every().day.at("{:0>2d}:{:0>2d}".format(*GET_UNCHECKED_SCHEDULES[i])).do(get_unchecked_list, int(i/2 + 1))
            schedule.every().day.at("{:0>2d}:{:0>2d}".format(*GET_UNCHECKED_SCHEDULES[i])).do(get_unchecked_list, int(i/2 + 1))
    if args.send_info:
        for i in range(len(SEND_INFO_SCHEDULES)):
            schedule.every().day.at("{:0>2d}:{:0>2d}".format(*SEND_INFO_SCHEDULES[i])).do(send_checked_info)
    
    
    while True:
        schedule.run_pending()
        time.sleep(30)
