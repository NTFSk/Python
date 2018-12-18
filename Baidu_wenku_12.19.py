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

#browser = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
# 指定最长等待时间为7s，超过则抛出异常
wait = WebDriverWait(browser, 7)
# 创建数据库
text_db = sqlite3.connect('D:/text.db')
#创建表的SQL语句
#sqlstr = "create table tx(page varchar(5) primary key, text varchar(3000))"
# 执行SQL语句
#text_db.execute(sqlstr)

MAX_PAGE=10
def go(url,contents):
    """
    清空数据库
    用循环控制页码的改变
    """
    #先清空数据库
    cur = text_db.cursor()
    cur.execute("DELETE FROM tx where 1 = 1")
    text_db.commit()
    #print("数据库已清空")
    contents.insert(END, "数据库已清空\n")
    page_expand(url,contents)
    for page in range(1, MAX_PAGE + 1):
        index_page(page,contents)

#页面跳转及展开
def page_expand(url, contents):
    #跳转到要爬取的网页
    contents.insert(END,"正在进入目标页面,请耐心等待……\n")
    browser.get(url)
    # 将网页移动到继续阅读的按钮附近，保证可以点击到按钮
    page_move = browser.find_elements_by_css_selector("#html-reader-go-more > div.banner-core-wrap.super-vip")
    browser.execute_script('arguments[0].scrollIntoView();', page_move[-1])  # 拖动到可见的元素去
    # 点击继续阅读，展开全部文本
    continue_read = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#html-reader-go-more div.banner-more-btn > span.moreBtn.goBtn')))
    continue_read.click()
    # 展开后等待3秒
    sleep(3)


def index_page(page,contents):
    """
    根据参数page，移动到新页面的位置
    网页移动(改变页码)后，执行获取文档代码
    """
    try:
        #页面移动
        move = browser.find_elements_by_css_selector('#pageNo-'+str(page))
        browser.execute_script('arguments[0].scrollIntoView();', move[-1])  # 拖动到可见的元素去
        #移动后等待2秒
        sleep(2)
        get_text(page,contents)
    except Exception as e:
        print(e)
        return FALSE


def get_text(page,contents):
    """
    提取节点内的文字，执行存入数据库代码
    """
    # 网页源代码
    html = browser.page_source
    # 初始化BeautifulSoup对象
    soup = BeautifulSoup(html, 'lxml')

    #s用来临时保存每一页的文字
    contents.insert(END,"正在爬取第"+str(page)+"页...\n")
    s=''
    # 查找结点
    for div in soup.select('#reader-container-inner-1'):
        #每个div2代表一页
        for div2 in div.select('#pageNo-'+str(page)):
            for ie in div2.find_all(class_='ie-fix'):
                for p in ie.find_all(name='p'):
                    p.string.replace('\n', '')
                    #p.string.replace('(', '\(')
                    #p.string.replace(')', '\)')
                    p.string.replace("'", "\'")
                    p.string.replace('"', '\"')
                    s+=p.string
        #存入数据库
        save_to_db(page,s,contents)
        sleep(1)


def save_to_db(page,result,contents):
    """
    保存至sqliteDB
    """
    try:
        cur = text_db.cursor()
        sqlstr = "INSERT INTO tx(page,text) VALUES(\'"+str(page)+"\',\'"+result+"\')"
        cur.execute(sqlstr)
        text_db.commit()
        #print("数据录入完成")
        contents.insert(END,"第"+str(page)+"页数据录入完成...\n")
    except IndexError:
        #print(e)
        #print('录入失败')
        contents.insert(END, "页码错误，录入失败\n")


def get_from_db(contents):
    """
    遍历表，输出表中的所有数据
    """
    cur = text_db.cursor()
    s = cur.execute("select * from tx")
    for row in s:
        contents.insert(END, "\n第" + row[0] + "页:" + "=" * 20 + '\n')
        contents.insert(END, row[1])
        


def clear(contents):
    contents.delete('1.0', END)


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
    Button(text='爬取数据', command=lambda: go(url_text.get(),contents)).pack(side=LEFT)
    Button(text='显示文本', command=lambda: get_from_db(contents)).pack(side=LEFT)
    Button(text='清空文本', command=lambda: clear(contents)).pack(side=LEFT)
    mainloop()
    




if __name__ == '__main__':
    main()



