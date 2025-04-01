from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
import random
import os
from bs4 import BeautifulSoup




# 注册
def register(username, password):
    driver.find_element(By.LINK_TEXT, "注册").click()
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirm_password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)


# 登录
def login(username, password):
    # 点击登录
    time.sleep(random.randint(1,10)+5)
    driver.find_element(By.LINK_TEXT, "登录").click()
    # 刷新页面
    time.sleep(random.randint(1,10)+5)
    driver.refresh()
    # 切换到 iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "contentIframe"))  # 或 By.NAME
    )
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(5)
    # 填充username and password
    time.sleep(random.randint(1,10)+5)
    driver.find_element(By.NAME, "username").send_keys(username)
    time.sleep(random.randint(1,10))
    driver.find_element(By.NAME, "password").send_keys(password)
    # 使用 data-action 或 XPath 定位并点击登录按钮
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@data-action='login-submit']"))
    )
    time.sleep(random.randint(1,10)+5)
    submit_button.click()
    # 切回主页面
    time.sleep(random.randint(1,10)+5)
    driver.switch_to.default_content()
    time.sleep(random.randint(1,10)+5)


# 类别查找
def search_by_category(category):
    # 进入高级搜索页面
    time.sleep(random.randint(1,10)+5)
    driver.get("https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html")

    # 文件类型定位的Xpath(//*[@id="_view_1545095166000"]/div/div[1])
    # 裁定书定位的Xpath(//*[@id="j4_2_anchor"])
    # 选择文书类型为"裁定书"（需根据实际HTML调整XPath）
    dropdown_xpath = "//*[@id='_view_1545095166000']/div/div[1]"
    # dropdown_xpath = "//div[contains(@class, 'search-option')]//div[@class='ant-select-selection']"
    # option_xpath = "//li[contains(text(), '裁定书')]"
    option_xpath = "//*[@id='j4_2_anchor']"

    # 文件类型选择
    time.sleep(random.randint(1,10)+5)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath))).click()
    print("文件类型选择成功")
    # 裁定书选择
    time.sleep(random.randint(1,10)+5)
    flat_ture = False
    while not flat_ture:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, option_xpath))).click()
            flat_ture = True
        except Exception as e:
            print(e)
            driver.refresh()
    print("裁定书选择成功")

    # 输入类别关键词（如"民事"）
    # 输入框定位Xpath(//*[@id="_view_1545034775000"]/div/div[1]/div[2]/input)
    keyword_input = driver.find_element(By.XPATH, "//*[@id='_view_1545034775000']/div/div[1]/div[2]/input")
    # keyword_input = driver.find_element(By.XPATH, "//input[@placeholder='全文检索']")
    time.sleep(random.randint(1,10)+5)
    keyword_input.send_keys(category)
    time.sleep(random.randint(1,10)+5)
    print("{}关键词输入成功".format(category))

    # 提交搜索
    # //*[@id="_view_1545034775000"]/div/div[1]/div[3]
    time.sleep(random.randint(1,10)+5)
    driver.find_element(By.XPATH, "//*[@id='_view_1545034775000']/div/div[1]/div[3]").click()
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'item_table')))
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'result-item')))
    except Exception:
        print("在规定时间未加载出来")



# 文本解析
def parse_documents(category, folder_name):
    # 等待结果加载
    time.sleep(random.randint(1,10)+5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "LM_list")))

    # 提取文书列表
    time.sleep(random.randint(1,10)+5)
    items = driver.find_elements(By.CLASS_NAME, "LM_list")
    print(items[0].text)
    print("---------------------------------------------------------")
    for item in items:
        try:
            global count0
            count0 += 1
            title = item.find_element(By.CLASS_NAME, "caseName").text
            link = item.find_element(By.CLASS_NAME, "caseName").get_attribute("href")
            print(f"标题: {title}\n链接: {link}\n")
            with open("{}.txt".format(category), "a+", encoding="utf-8") as f:
                f.write(str(count0))
                f.write(f"标题: {title}\n")  # `\n` 表示换行
            url = link
            # 第二阶段：访问目标URL
            time.sleep(random.randint(1,10)+5)
            driver.get(url)

            # 验证是否跳转成功
            if "index.html?docId" not in driver.current_url:
                print("检测到重定向，尝试强制跳转...")
                time.sleep(random.randint(1,10)+5)
                driver.get(url)

            # 智能等待内容加载
            time.sleep(random.randint(1,10)+5)

            content = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((
                    By.XPATH,'//*[@id="_view_1541573883000"]/div/div[1]/div[3]'
                    # '//div[contains(@class,"doc-body") or contains(@class,"content-text")]'
                ))
            )
            # 获取网页截图并保存为文件
            file_name = '{}.png'.format(category + str(count0))

            # 生成完整的文件路径
            screenshot_path = os.path.join(folder_name, file_name)

            # 获取页面宽度和高度
            driver.set_window_size(1800, 600)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            # print("width:", width, "height:", height)
            # 设置窗口大小
            driver.set_window_size(1800, height)

            # # 使用 JavaScript 去掉 .mask_box 的 background
            # script = """
            # document.querySelector('PDF_pox').style.background = 'none';
            # """
            # driver.execute_script(script)

            # 截取全屏截图
            driver.save_screenshot(screenshot_path)

            # 裁定书内容
            # print(content.text)
            with open("{}.txt".format(category), "a+", encoding="utf-8") as f:
                f.write(content.text+'\n\n\n')  # `\n` 表示换行
            time.sleep(random.randint(1,10)+5)

            # # 返回原来页面大小
            # time.sleep(random.randint(1, 10) + 5)
            # driver.set_window_size(1200, 800)

            driver.back()
        except Exception as e:
            driver.back()
            print(e)
            pass
# xpath = '//*[@id="_view_1541573883000"]/div/div[1]/div[3]'

# 示例使用
# username = "18061993705"

# Category = "民事"
# Category = "刑事"
# Category = "合同"
# Category = "利息"
# Category = "贷款"
# Category = "清偿"
# Category = "债权"
# Category = "处分"

# 主函数
def main(Category):
    # 记录开始时间
    start_time = time.time()
    # 注册
    # register(username, password)

    #登录信息
    username = "18862110056"
    # username = "18061993705"
    password = "Aa2483101195"

    # 登录
    login(username, password)

    # 类别锁定
    search_by_category(Category)
    # 文件创建
    with open("{}.txt".format(Category), "w", encoding="utf-8") as f:
        f.write(Category)

    # 定义截图文件夹名称
    Folder_name = Category+'裁定书截图'

    # 创建文件夹（如果不存在）
    os.makedirs(Folder_name, exist_ok=True)
    page_num = 20
    for i in range(page_num):
        # 内容解析
        time.sleep(random.randint(1,10))
        parse_documents(Category, Folder_name)
        print(str(i+1)+"/{}-------------------------------------------------------------".format(page_num))
        # nextPage = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='_view_1545184311000']/div[8]/a[8]")))
        nextPage = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, str(i+2))))
        time.sleep(random.randint(1,10))
        nextPage.click()


    # 记录结束时间
    end_time = time.time()

    # 计算运行时间
    elapsed_time = (end_time - start_time)/3600
    print(f"程序运行时间: {elapsed_time} 小时")

    #关闭浏览器
    driver.quit()

# 主程序
category_lst = ["民事", "刑事", "债权", "清偿", "合同", "利息", "贷款", "处分", "违约金", "返还"]
for cate_name in category_lst:
    if "{}.txt".format(cate_name) in os.listdir(r"E:\code\py\judicature\.venv"):
        pass
    else:
        count0 = 0
        # 初始化浏览器
        chrome_options = Options()
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)

        # 打开网站
        driver.get("https://wenshu.court.gov.cn/")
        # 隐式等待，最长时间为 10 秒
        driver.implicitly_wait(10)
        main(cate_name)