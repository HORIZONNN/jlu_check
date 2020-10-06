from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from urllib.parse import urlencode
import re
import traceback
import sys
import time

XZC_URL = "http://www.xzc.cn/"


def change_dir_name(username, password, xzc_code, dir_name):

    xzc_dir_url = XZC_URL + xzc_code + "/add/2"

    try:

        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(browser, 20)

        ### 模拟一下登录过程，获取一下cookies
        browser.get(XZC_URL)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.start > a.btn-lg"))).click()

        # 弹窗操作部分：登录
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.form-group > input.form-control[name="email"]'))).send_keys(username)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.form-group > input.form-control[name="password"]'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.form-group > label.checlbox > input[NAME="cookietime"]'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.form-group > button[name="loginsubmit"]'))).click()

        # 确保已经完成登陆操作，cookies已经存在，创建文件夹的按钮已经显示出来
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.posts-date-right > a.btn')))


        ### 修改目录名称
        browser.get(xzc_dir_url)
        # 点击标题
        title = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.subject_text.edit-op > span.text")))
        time.sleep(2)
        title.click()
        time.sleep(2)
        # 输入标题
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.edit > input.form-control.input-lg"))).send_keys(dir_name)

        # 点击空白处，确保标题已修改
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body"))).click()
        # 点击下一步确认
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-green"))).click()
        return True
    except TimeoutException as e:
        time.sleep(60)
        return change_dir_name(username, password, xzc_code, dir_name)
    except NoSuchElementException as e:
        traceback.print_exc(e)
        print("Source code has been changed. Please edit this code to fit it and try again!")
        sys.exit()
    # finally:
    #     browser.close()


def upload_file(file_path, xzc_code, input1, input2):

    session = requests.Session()
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40",
        "Referer" : XZC_URL + xzc_code,
    }

    # index page
    result1 = session.get(XZC_URL + xzc_code, headers=headers)
    
    # preview picture page
    result2 = session.get(
        XZC_URL + "index.php?mod=attach&op=preview",
        headers=headers
    )

    # upload picture page
    params = {
        'op' : 'ajax',
        'do' : 'fileupload'
    }
    result3 = session.post(
        XZC_URL + '?' + urlencode(params), 
        headers=headers, 
        files={"files[]" : open(file_path, 'rb')}
    )

    # preview uploaded picture page
    img = result3.json().get('files')[0].get('data').get('img')
    result4 = session.get(XZC_URL + img, headers=headers)

    # submit page
    params = {
        'op' : 'fileupload'
    }
    formhash = re.search('formhash\"\s+value=\"(\w+)\"\s+/>', result1.text).group(1)
    aids = result3.json().get('files')[0].get('data').get('aid')
    file_names = result3.json().get('files')[0].get('data').get('filename')
    data = {
        'formhash' : formhash,
        'postsubmit' : 'true',
        'sid' : xzc_code,
        'cname' : input1,
        'uname' : input2,
        'aids[]' : aids,
        'filenames[]' : file_names
    }
    result5 = session.post(XZC_URL + '?' + urlencode(params), data=data, headers=headers)





