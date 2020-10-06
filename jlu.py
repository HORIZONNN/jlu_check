from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import sys
import time
import traceback
from urllib.parse import urlencode
import requests


# 模拟打卡相关部分
JLU_CHECK_URL = "https://ehall.jlu.edu.cn/jlu_portal/index" # 健康打卡系统登录页



def jlu_check(username, password, major, grade, campus, apartment, bedroom, master, nth, file_path=None):
    """
    username : 登录吉大系统的用户名
    password ： 登录吉大系统的密码
    file_path : 保存截图的根目录，如果为None则表示不截图
    major : 研究生每日打卡中的【专业】
    grade : 研究生每日打卡中的【年级】
    campus : 研究生每日打卡中的【校区】
    apartment : 研究生每日打卡中的【公寓楼名称】
    master : 研究生每日打卡中的【硕士/博士】，硕士为True，博士为False
    """
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(browser, 30)
        browser.get(JLU_CHECK_URL)

        #  login
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "login-submit"))).click()

        ### more
        # 更多服务
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".student-tabList > ul > li:nth-of-type(9) > a"))).click()

        ### check
        # 研究生每日打卡
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.alk-service-nav > h2.alk-service-nav-title > a[title="研究生每日打卡"]'))).click()

        # 我要办理
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.guide_title_center > input.bt_2[value='我要办理']"))).click()

        # close window
        handles = browser.window_handles
        for newhandle in handles:
            if newhandle != browser.current_window_handle:
                browser.close()
                browser.switch_to_window(newhandle)
                break

        # fill in
        major_input = wait.until(EC.visibility_of_element_located((By.ID, "V1_CTRL40")))
        major_input.clear()
        major_input.send_keys(major)
        Select(browser.find_element_by_id("V1_CTRL41")).select_by_visible_text(grade)
        Select(browser.find_element_by_id("V1_CTRL42")).select_by_visible_text(campus)
        Select(browser.find_element_by_id("V1_CTRL7")).select_by_visible_text(apartment)
        bedroom_input = wait.until(EC.presence_of_element_located((By.ID, "V1_CTRL8")))
        bedroom_input.clear()
        bedroom_input.send_keys(bedroom)
        if master:
            wait.until(EC.element_to_be_clickable((By.ID, "V1_CTRL44"))).click()
        else:
            wait.until(EC.element_to_be_clickable((By.ID, "V1_CTRL45"))).click()


        # 体温状态
        if nth != 4:
            css_code = {
                1 : "table.xdLayout > tbody > tr:nth-last-child(8) > td:nth-child(3) > div > div > input:nth-child(1)",
                2 : "table.xdLayout > tbody > tr:nth-last-child(6) > td:nth-child(3) > div > input:nth-child(1)",
                3 : "table.xdLayout > tbody > tr:nth-last-child(4) > td:nth-child(3) > div > div > input:nth-child(1)"
            }.get(nth)
            print(nth)
            agree_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_code)))
            agree_box.click()

        # 提交
        submit_bt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul#form_command_bar > li.command_button > a.command_button_content")))
        submit_bt.click()

        # dialog process
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dialog_footer > .dialog_button.default.fr"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dialog_footer > button.dialog_button.default.fr")))

        ### screenshot
        if file_path != None:
            body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "html")))
            time.sleep(2) # wait until the ok dialog display
            file_name = time.strftime("%Y%m%d-%H.png", time.localtime())
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            abs_file_path = os.path.join(os.path.abspath(file_path), file_name)
            body.screenshot(abs_file_path)
            return abs_file_path
        else:
            return "success"
        
    except TimeoutException:
        time.sleep(60*5)
        if time.localtime().tm_hour in [7, 11, 17, 21]:
            return jlu_check(username, password, major, grade, campus, apartment, bedroom, master, file_path)
        else:
            print("network problem! several tries all failed!")
    except NoSuchElementException:
        print("Source code has been changed. Please edit this code to fit it and try again!")
        sys.exit()
    except BaseException as e:
        traceback.print_exc(e)
        sys.exit()
    finally:
        browser.close()



def jlu_check_old(username, password, file_path=None):
    """
    username : 登录吉大系统的用户名
    password ： 登录吉大系统的密码
    file_path : 保存截图的根目录，如果为None则表示不截图
    """
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(browser, 20)
        browser.get(JLU_CHECK_URL)

        #  login
        user_input = wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        pw_input = wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        login_bt = wait.until(EC.element_to_be_clickable((By.ID, "login-submit"))).click()


        ### check
        # check
        check_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".student-tabList > ul > li:nth-of-type(5) > a")))
        check_link.click()
        # handle
        handle_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".guide_title_center > .bt_2")))
        handle_link.click()
        # fill in and configure
        handles = browser.window_handles
        for newhandle in handles:
            if newhandle != browser.current_window_handle:
                browser.close()
                browser.switch_to_window(newhandle)
                break

        # browser.switch_to_window(browser.window_handles[1])
        wait.until(EC.element_to_be_clickable((By.ID, "V1_CTRL82"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.command_button > a.command_button_content"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dialog_footer > .dialog_button.default.fr"))).click()
        success = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dialog_footer > button.dialog_button.default.fr")))

        if file_path != None:
            body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "html")))
            time.sleep(2) # wait until the ok dialog display
            file_name = time.strftime("%Y%m%d.png", time.localtime())
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            abs_file_path = os.path.join(os.path.abspath(file_path), file_name)
            body.screenshot(abs_file_path)
            return abs_file_path
        else:
            return None
        
    except TimeoutException:
        # print("Timeout! Please wait a minute and try again!")
        # return None
        time.sleep(60*30)
        return jlu_check_old(username, password, file_path)
    except NoSuchElementException as e:
        traceback.print_exc(e)
        print("Source code has been changed. Please edit this code to fit it and try again!")
        sys.exit()
    except BaseException as e:
        traceback.print_exc(e)
        sys.exit()
    finally:
        browser.close()

    
