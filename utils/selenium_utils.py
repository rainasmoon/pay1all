# -*- coding: utf-8 -*
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

test_url_1 = 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=58d2347f9b31410588c47ce29351c7be'


def get_source(aurl):
    options = Options()
    options.add_argument('-headless')  # 无头参数
    driver = Firefox(executable_path='../lib/geckodriver', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
#     driver = Firefox(executable_path='../lib/geckodriver.exe', options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径

    wait = WebDriverWait(driver, timeout=10)
    driver.get(aurl)
    page_source = driver.page_source
    driver.quit()
    return page_source


if __name__ == "__main__":
    print(get_source(test_url_1))
