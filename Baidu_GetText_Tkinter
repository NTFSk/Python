from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def clear():
    contents.delete('1.0', END)

def getText(page,html):
    """
    提取文本信息
    """
    # 初始化BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')
    # 查找结点
    for div in soup.select('#reader-container-inner-1'):
        for div2 in div.select('#pageNo-'+str(page)):
            for ie in div2.find_all(class_='ie-fix'):
                for p in ie.find_all(name='p'):
                    contents.insert(END, p.string.replace('\n', ''))
                contents.insert(END,str(page) + ':\n' + '=' * 20)
                
MAX_PAGE = 10
def main():
    browser = webdriver.Chrome()
    # 指定最长等待时间为7s，超过则抛出异常
    wait = WebDriverWait(browser,7)
    #要爬取的网页地址
    url = url_text.get()
    browser.get(url)
    #将网页移动到继续阅读的按钮附近，保证可以点击到按钮
    page = browser.find_elements_by_css_selector("#html-reader-go-more > div.banner-core-wrap.super-vip")
    browser.execute_script('arguments[0].scrollIntoView();', page[-1]) #拖动到可见的元素去
    #点击继续阅读，展开全部文本
    continue_read = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#html-reader-go-more div.banner-more-btn > span.moreBtn.goBtn')))
    continue_read.click()
    #展开后等待3秒
    sleep(3)
    for i in range(1, MAX_PAGE + 1):
        #移动页面
        move = browser.find_elements_by_css_selector('#pageNo-'+str(i))
        browser.execute_script('arguments[0].scrollIntoView();', move[-1])  #拖动到可见的元素去
        #等待3秒
        sleep(3)
        # 网页源代码
        html = browser.page_source
        getText(i,html)


#创建窗体
top = Tk()
top.title("百度文库文本获取")
top.geometry('750x500+500+200')
#多行文本框
contents = ScrolledText()
contents.pack(side=BOTTOM, expand=True, fill=BOTH)
#单行文本框
url_text = Entry()
url_text.pack(side=LEFT, expand=True, fill=X)
url_text.insert(0, "<请将网址填写到此处>")
#两个按钮
Button(text='获取文本',command=main).pack(side=LEFT)
Button(text='清空文本', command=clear).pack(side=LEFT)
mainloop()

#学完多线程再来改善
