# -*- coding: utf-8 -*-
import scrapy
from c_poem.items import CPoemItem
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class CpoemSpider(scrapy.Spider):
    name = 'cpoem'
    allowed_domains = ['gushiwen.cn']
    # start_urls = ['https://so.gushiwen.cn/gushi/tangshi.aspx', ]# 唐诗三百首
    #start_urls = ['https://so.gushiwen.cn/gushi/songsan.aspx', ]  # 宋词三百首
    start_urls = ['https://so.gushiwen.cn/shiwen/default_1Acde790aa3213A1.aspx' ]
    #https://www.jianshu.com/p/53af85a0ce18
    def __init__(self):
        chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        browser_path = r"C:\MKSProjects\Vision Test Environment\CANoe\Geely_GEEA2\Tools\myPython\chromedriver.exe"
        # desired_capabilities = DesiredCapabilities.CHROME
        # # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        # desired_capabilities["pageLoadStrategy"] = "none"
        self.browser = webdriver.Chrome(executable_path=browser_path,options=chrome_options)

    def parse(self, response):
        print("************************\n****************************")
        self.browser.get(response.url)
        self.browser.implicitly_wait(5)
        sons = self.browser.find_elements_by_xpath(".//div[@class='left']//div[@class='sons']")
        for son in sons:
            item = CPoemItem()
            item['poem_type'] = "宋词"
            item['poem_url'] = response.url

            title = son.find_element_by_xpath(".//div[@class = 'cont']//p//a//b").text
            item['poem_title'] = title

            source = son.find_elements_by_xpath(".//div[@class = 'cont']//p[@class = 'source']/a")
            author = [i.text.strip() for i in source]
            item['poem_author'] = '.'.join(author)

            contson = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']")
            body = [i.text.strip() for i in contson]
            item['poem_body'] = ''.join(body)

            yi_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'译')]")
            yi_button.click()
            time.sleep(0.2)

            yi = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            yi = [i.text.strip() for i in yi]
            item['poem_yi'] = ''.join(yi)
            yi_button.click()
            time.sleep(0.2)

            zhu_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'注')]")
            zhu_button.click()
            time.sleep(0.2)

            zhu = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            zhu = [i.text.strip() for i in zhu]
            item['poem_zhu'] = ''.join(zhu)
            zhu_button.click()
            time.sleep(0.2)

            shang_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'赏')]")
            shang_button.click()
            time.sleep(0.5)

            shang = son.find_elements_by_xpath(
                ".//div[@class = 'cont']//div[@class = 'contson']//div[@class = 'hr']/following-sibling::p[not(@style)]")
            shang = [i.text.strip() for i in shang]
            item['poem_shang'] = ''.join(shang)
            shang_button.click()
            time.sleep(0.5)
            yield item
