from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import Tag, BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options

class KeyCrawler() : 
    def OPEN_BROWSER(self, url):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.22 Safari/537.36")
        options.add_argument('--start-fullscreen')
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path="/data01/skc/apix/voucher/chromedriver", options=options)
        #driver = webdriver.Chrome(executable_path="./voucher/chromedriver.exe", options=options)
        driver.get(url)
        tmp = KeyCrawler.GET_KEYWORD(driver)
        driver.quit()
        return tmp
        #return KeyCrawler.GET_KEYWORD(driver)
    
    def GET_KEYWORD(driver):
        content_html = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR , 'div.ndSf3d.eDrqsc.ttg1Pb.j7vNaf.Pz9Pcd.a8arzf'))).get_attribute('innerHTML')
        content = bs( content_html, 'html.parser')
        keyword_list = content.findAll("a")

        list = []
        for idx, keyword in enumerate(keyword_list) :
            list.append(keyword['aria-label'])

        return list
