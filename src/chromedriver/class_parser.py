import pickle
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import config


# driver = webdriver.Chrome(
#     executable_path="C:\\Users\\TRVL\\PycharmProjects\\TrainingBot\\src\\chromedriver\\chromedriver.exe")


class Parser:
    # __instance__ = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance__ is None:
    #         cls.__instance__ = super().__new__()
    #
    #     return cls.__instance__

    def __init__(self, path, username, password):
        self.path = path
        self.username = username
        self.password = password
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=self.option)
        self.cookies_file = 'cookies'

    def authorization(self, path, username, password):
        driver = self.driver
        username = self.username
        password = self.password
        login_page = config.login_page
        cookies_file = self.cookies_file

        try:

            driver.get(login_page)
            time.sleep(3)
            input_username = driver.find_element_by_id("loginUsername")
            time.sleep(2)
            input_username.send_keys(username)
            time.sleep(4)
            input_password = driver.find_element_by_id("loginPassword")
            time.sleep(3)
            input_password.send_keys(password)
            time.sleep(3)
            input_password.send_keys(Keys.ENTER)
            time.sleep(3)

            pickle.dump(driver.get_cookies(), open(cookies_file, 'wb'))

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(5)
            driver.close()
            driver.quit()

    def get_images(self, url):
        url = url
        driver = self.driver
        scroll_pause_time = 15
        count = 0
        cookies_file = self.cookies_file

        try:
            driver.get(url)
            # чтение и установка кукис
            cookies = pickle.load(open(cookies_file, "rb"))

            for cookie in cookies:
                driver.add_cookie(cookie)

            driver.refresh()

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while count != 2:

                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_pause_time)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                last_height = new_height

                count += 1
                print(count)

            soup = bs(driver.page_source, "html.parser")
            images = soup.find_all('img',
                                   class_='_2_tDEnGMLxpM6uOa2kaDB3 ImageBox-image media-element _1XWObl-3b9tPy64oaG6fax')

            img_list = []

            for image in images:
                image_url = image.get('src')
                img_list.append(image_url)

            return img_list



        except Exception as ex:
            print(ex)

        finally:
            time.sleep(5)
            driver.close()
            driver.quit()
