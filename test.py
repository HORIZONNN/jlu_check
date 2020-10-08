import schedule

import time

from main_config import *
from jlu import jlu_check


def info_print(info):
    print(time.strftime("%Y%m%d-%H:%M:%S", time.localtime()) + "*" * 30)
    print(info)
    print("*"*45 + "\n\n")

def check_and_confirm(i):
    result = jlu_check(JLU_USERNAME, JLU_PASSWORD, **JLU_INFO, nth=i, file_path=None)
    if result == "success":
        info_print("check : check success!")

for i in range(len(CHECK_SCHEDULES)):
    schedule.every().day.at("{:0>2d}:{:0>2d}".format(*CHECK_SCHEDULES[i])).do(check_and_confirm, i+1)

while True:
    schedule.run_pending()
    time.sleep(30)
