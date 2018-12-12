from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep

browser = webdriver.Chrome()
# 指定最长等待时间为5s，超过则抛出异常
wait = WebDriverWait(browser, 5)
#要爬取的网页地址
url = 'https://wenku.baidu.com/view/43b2727e0342a8956bec0975f46527d3250ca676.html'
browser.get(url)
#将网页移动到继续阅读的按钮附近，保证可以点击到按钮
page = browser.find_elements_by_css_selector("#html-reader-go-more > div.banner-core-wrap.super-vip")
browser.execute_script('arguments[0].scrollIntoView();', page[-1]) #拖动到可见的元素去
#点击继续阅读，展开全部文本
continue_read = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#html-reader-go-more div.banner-more-btn > span.moreBtn.goBtn')))
continue_read.click()
#展开后等待3秒
sleep(3)


def getText(page):
    """
    提取文本信息
    """
    # 网页源代码
    html = browser.page_source
     # 初始化BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')
    # 查找结点
    for div in soup.select('#reader-container-inner-1'):
        for div2 in div.select('#pageNo-'+str(page)):
            for ie in div2.find_all(class_='ie-fix'):
                for p in ie.find_all(name='p'):
                    print(p.string.replace('\n', ''), end='')
                print(str(page) + ':\n' + '=' * 20)
                
MAX_PAGE = 10
def main():
    for i in range(1, MAX_PAGE + 1):
        #输入页码
        #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.reader-tools-bar-wrap.tools-bar-small.tools-bar-smaller > div > div.reader-tools-bar-center.clearfix > div.center > div.centerLeft > div > input')))
        #input.clear()
        #input.send_keys(i)
              
        #移动页面
        move = browser.find_elements_by_css_selector('#pageNo-'+str(i))
        browser.execute_script('arguments[0].scrollIntoView();', move[-1]) #拖动到可见的元素去
        sleep(1)
        #pyautogui.press('enter')
        sleep(2)
        getText(i)

main()
