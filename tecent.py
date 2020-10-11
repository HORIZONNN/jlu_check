from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import re


class TecentDoc(object):

    def __init__(self, url, qq_num, pwd):
        super().__init__()
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser,20)

        self.browser.get(url)

        self.wait.until(EC.element_to_be_clickable((By.ID, "header-login-btn"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#id-login-tabs > div.qq"))).click()
        self.browser.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "login_frame"))))
        self.wait.until(EC.element_to_be_clickable((By.ID, "switcher_plogin"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "u"))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(qq_num)
        self.wait.until(EC.presence_of_element_located((By.ID, "p"))).send_keys(pwd)
        self.wait.until(EC.element_to_be_clickable((By.ID, "login_button"))).click()
        # try:
        #     self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.img_out_focus"))).click()
        # except TimeoutException:
        #     self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.img_out"))).click()
        time.sleep(2)
        self.browser.switch_to.parent_frame()
        time.sleep(2)

        self.editor = self.wait.until(EC.presence_of_element_located((By.ID, "alloy-simple-text-editor")))
    
    def confirm(self, name):

        ActionChains(self.browser).key_down(Keys.CONTROL).key_down('f').perform()
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located((By.ID, "search-panel-input"))).send_keys(name)
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dui-modal-mask.dui-modal-mask-visible > div > div.dui-modal-close"))).click()

        self.browser.find_element_by_id('alloy-simple-text-editor').send_keys(Keys.TAB)

        self.editor.click()
        self.editor.send_keys("已打")
        self.editor.send_keys(Keys.ENTER)
        time.sleep(3)

    def replace(self):

        ActionChains(self.browser).key_down(Keys.CONTROL).key_down('f').perform()
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-replace-tab-wrap > li:nth-child(2)"))).click()

        self.wait.until(EC.presence_of_element_located((By.ID, "replace-panel-search-input"))).send_keys("已打")
        self.wait.until(EC.presence_of_element_located((By.ID, "replace-panel-replace-input"))).send_keys("")

        replace = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.replace-button-wrap.search-button-wrap > div.button-group-wrap > button:nth-child(4) > div.dui-button-container")))
        time.sleep(2)
        replace.click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dui-modal-footer > button.dui-button.dui-modal-footer-ok.dui-button-type-primary.dui-button-size-default > div"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dui-modal-mask.dui-modal-mask-visible > div > div.dui-modal-close"))).click()
        time.sleep(5)

    def get_unchecked(self):

        ActionChains(self.browser).key_down(Keys.CONTROL).key_down('f').perform()
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located((By.ID, "search-panel-input"))).send_keys("打卡记录")
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dui-modal-mask.dui-modal-mask-visible > div > div.dui-modal-close"))).click()

        unchecked_names = []

        end = False
        while not end:
            self.editor.send_keys(Keys.ENTER)
            if "已打" not in self.editor.get_attribute("innerHTML"):
                self.editor.send_keys(Keys.SHIFT, Keys.TAB)
                result = re.search("[\u4e00-\u9fa5]+", self.editor.get_attribute("innerHTML"))
                if result == None:
                    end = True
                else:
                    unchecked_names.append(result.group(0))
                self.editor.send_keys(Keys.TAB)

        return unchecked_names



        




