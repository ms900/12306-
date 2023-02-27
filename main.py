import profile

from easyprocess.examples.cmd import python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


option = Options()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('user-data-dir=D:\python\profile')


# option.add_argument(“user-data-dir=C:\ Users\mashuan\AppData\Local\Programs\Python\Python36\Chrome” )


class Qiangpiao(object):

    def __init__(self):
        self.driver = webdriver.Chrome(options=option)
        self.driver.maximize_window()

        self.from_station = input('出发地：')
        self.to_station = input('目的地：')
        self.depart_time = input('出发日期：')
        self.passengers = input('乘客：').split(',')
        self.trains = input('车次：').split(',')
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def _login(self):
        self.driver.get(self.login_url)

        WebDriverWait(self.driver, 1000).until(
            EC.url_to_be(self.initmy_url)
        )
        print("登录成功")

    def _order_ticket(self):
        self.driver.get(self.search_url)

        #button = self.driver.find_element_by_id("qd_closeDefaultWarningWindowDialog_id")
        #button.click()

        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "fromStationText"), self.from_station)
        )
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.to_station)
        )
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time)
        )
        WebDriverWait(self.driver, 1000).until(
            EC.element_to_be_clickable((By.ID, "query_ticket"))
        )
        searchBtn = self.driver.find_element_by_id("query_ticket")
        searchBtn.click()

        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='queryLeftTable']/tr"))
        )
        tr_list = self.driver.find_elements_by_xpath("//*[@id='queryLeftTable']/tr[not(@datatran)]")
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[4]").text
                if left_ticket == "有" or left_ticket.isdigit:
                    print(train_number + "有票")
                    order_btn = tr.find_element_by_class_name("btn72")
                    order_btn.click()

                    WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.passenger_url))

                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.XPATH, ".//ul[@id= 'normal_passenger_id']/li"))
                    )
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()
                    submitBtn = self.driver.find_element_by_id("submitOrder_id")
                    submitBtn.click()

                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dhtmlx_wins_body_outer"))
                    )
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.ID, "qr_submit_id"))
                    )
                    confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                    confirmBtn.click()
                    while confirmBtn:
                        confirmBtn.click()
                        confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                    return

    def run(self):
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = Qiangpiao()
    spider.run()


