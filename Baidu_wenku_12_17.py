from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sqlite3

browser = webdriver.Chrome()
# 指定最长等待时间为7s，超过则抛出异常
wait = WebDriverWait(browser, 7)
# 创建数据库
text_db = sqlite3.connect('D:/text.db')
#创建表的SQL语句
#sqlstr = "create table tx(page varchar(5) primary key, text varchar(3000))"
# 执行SQL语句
#text_db.execute(sqlstr)




def index_page(url,page):
    """
    提取文本信息
    """
    try:
        # 要爬取的网页地址
        browser.get(url)
        # 将网页移动到继续阅读的按钮附近，保证可以点击到按钮
        page_move = browser.find_elements_by_css_selector("#html-reader-go-more > div.banner-core-wrap.super-vip")
        browser.execute_script('arguments[0].scrollIntoView();', page_move[-1])  # 拖动到可见的元素去
        # 点击继续阅读，展开全部文本
        continue_read = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#html-reader-go-more div.banner-more-btn > span.moreBtn.goBtn')))
        continue_read.click()
        # 展开后等待3秒
        sleep(3)
        get_text(page)
    except TimeoutException:
        index_page(url,page)


def get_text(page):
    """
    提取节点内的文字
    """
    # 网页源代码
    html = browser.page_source
    # 初始化BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')
    # 移动页面
    try:
        move = browser.find_elements_by_css_selector('#pageNo-'+str(page))
        browser.execute_script('arguments[0].scrollIntoView();', move[-1])  # 拖动到可见的元素去
    #捕捉页码异常
    except IndexError:
        print('\n' + "未找到第"+str(page)+"页……")
        return False
    # 等待3秒
    sleep(3)
    #s用来储存每一页的文字
    s=''
    # 查找结点
    for div in soup.select('#reader-container-inner-1'):
        #每个div2代表一页
        for div2 in div.select('#pageNo-'+str(page)):
            for ie in div2.find_all(class_='ie-fix'):
                for p in ie.find_all(name='p'):
                    p.string.replace('\n', '')
                    p.string.replace('(', '\(')
                    p.string.replace(')', '\)')
                    p.string.replace("'", "\'")
                    p.string.replace('"','\"')
                    s+=p.string
                    #contents.insert(END, p.string.replace('\n', ''))
                #contents.insert(END, str(page) + ':\n' + '=' * 20)
        save_to_db(page,s)


def save_to_db(page,result):
    """
    保存至sqliteDB
    """

    try:
        cur = text_db.cursor()
        sqlstr = "INSERT INTO tx(page,text) VALUES(\'"+str(page)+"\',\'"+result+"\')"
        cur.execute(sqlstr)
        text_db.commit()
        print("数据录入完成")
    except Exception as e:
        print(e)
        print('录入失败')

def go(url):
    cur = text_db.cursor()
    cur.execute("DELETE FROM tx where 1 = 1")
    text_db.commit()
    print("数据删除完毕")
    for i in range(1, MAX_PAGE + 1):
        index_page(url, i)

def clear(contents):
    contents.delete('1.0', END)
    browser.close()

MAX_PAGE=10
def main():
    # 创建窗体
    top = Tk()
    # 标题
    top.title("百度文库文本获取")
    # 窗口大小
    top.geometry('750x500+500+200')
    # 多行文本框
    contents = ScrolledText()
    contents.pack(side=BOTTOM, expand=True, fill=BOTH)
    # 单行文本框
    url_text = Entry()
    url_text.pack(side=LEFT, expand=True, fill=X)
    url_text.insert(0, "<请将网址填写到此处>")
    # 三个按钮
    Button(text='爬取数据', command=lambda: go(url_text.get())).pack(side=LEFT)
    #Button(text='显示文本', command=lambda: getText()).pack(side=LEFT)
    Button(text='清空文本', command=lambda: clear(contents)).pack(side=LEFT)

    mainloop()
    




if __name__ == '__main__':
    main()



