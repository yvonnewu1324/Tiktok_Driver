from socket import timeout
import undetected_chromedriver as uc
from selenium.webdriver import ChromeOptions, Firefox, FirefoxOptions, FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from time import sleep
import random
import pyktok as pyk
import csv


class TikTokDriver:

    def __init__(self, browser='chrome', profile_dir=None, use_virtual_display=False, headless=False, verbose=False):

        if use_virtual_display:
            display = Display(size=(1920, 1080))
            display.start()

        if browser == 'chrome':
            self.driver = self.__init_chrome(profile_dir, headless)
        elif browser == 'firefox':
            self.driver = self.__init_firefox(profile_dir, headless)
        else:
            raise Exception("Invalid browser", browser)

        self.driver.set_page_load_timeout(30)
        self.verbose = verbose

    def close(self):
        self.driver.close()

    def search_and_watch(self, query, num=10, duration=30):
        # go to homepage and type in search query
        self.goto_homepage()

        # type in search query
        self.driver.find_element(
            By.XPATH, '//input[@name="q"]').send_keys(query)
        self.driver.find_element(
            By.XPATH, '//input[@name="q"]').send_keys(Keys.ENTER)

        # click on top result
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@data-e2e="search_top-item"]'))
        )
        self.driver.find_element(
            By.XPATH, '//div[@data-e2e="search_top-item"]').click()

        for i in range(num):
            print("Watching %s / %s video..." % (i, num))

            # watch for some time
            self.__random_duration

            # like and follow
            try:
                self.__log("Failed. Clicking via Javascript...")
                self.driver.find_element(
                    By.XPATH, '//span[@data-e2e="browse-like-icon"]').click()
                self.save_screenshot(f"{query}_like_video_{i}.png")
            except:
                try:
                    # try to click the element using javascript
                    self.__log("Failed. Clicking via Javascript...")
                    element = self.driver.find_element(
                        By.XPATH, '//span[@data-e2e="browse-like-icon"]')

                    # execute javascript to click the element
                    self.driver.execute_script(
                        "arguments[0].click();", element)
                except:
                    # js click failed, just open the video url
                    self.__log("Failed...")
                pass
            try:
                self.driver.find_element(
                    By.XPATH, '//div[@data-e2e="browse-follow"]').click()
                self.save_screenshot(f"{query}_follow_video_{i}.png")
            except:
                pass

            # scroll to next video
            self.__random_sleep()
            self.driver.find_element(
                By.XPATH, '//button[@data-e2e="arrow-right"]').click()

        # # load video search results
        # self.driver.get('https://tiktok.com/search/video?q=%s' % quote_plus(query))

        # sleep(3)

        # # scroll page to load more results
        # for _ in range(scroll_times):
        #     el = self.driver.find_element(By.XPATH, '//button[text()="Load more"]')
        #     if el is not None:
        #         el.click()
        #     sleep(1)

        # results = []
        # sleep(0.5)

        # # collect video-like tags from homepage
        # videos = self.driver.find_elements(By.TAG_NAME, 'a')

        # # identify actual videos from tags
        # for video in videos:
        #     href = video.get_attribute('href')
        #     if href is not None and re.match(r'https://www.tiktok.com/@.*?/video/[0-9]+', href) is not None:
        #         try:
        #             desc = video.find_element(By.TAG_NAME, 'img').get_attribute('alt')
        #             results.append(Short(video, href, desc))
        #         except:
        #             pass
        # return results

    def watch_for_you_page(self, num=10):
        # go to For You page
        self.goto_homepage()
        self.__random_sleep()
        self.driver.find_element(
            By.XPATH, '//span[text()="For You"]').click()
        # click on top result
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@data-e2e="feed-video"]'))
        )
        self.driver.find_element(
            By.XPATH, '//div[@data-e2e="feed-video"]').click()
        for i in range(num):
            print("Watching %s / %s video..." % (i, num))

            # watch for some time
            self.__random_duration()
            # self.save_screenshot(f"ss_foryou_{i}.png")
            print(self.driver.current_url)
            self.collect_metadata_by_url(self.driver.current_url)
            self.save_url_to_csv(self.driver.current_url, 'urls.csv')
            # scroll to next video
            self.__random_sleep()
            self.driver.find_element(
                By.XPATH, '//button[@data-e2e="arrow-right"]').click()

    def collect_metadata_by_url(self, url):
        # browser specification may or may not be necessary depending on your local settings
        pyk.specify_browser('chrome')
        pyk.save_tiktok(url,
                        False,
                        'tiktok_data.csv',
                        'chrome')
        import csv

    def save_url_to_csv(slef, url, csv_file):
        # append the URL to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url])
        print(f"URL '{url}' has been added to {csv_file}")

    def login(self, email, password):
        # open homepage
        self.goto_homepage()
        # start login work flow
        # click on login button
        try:
            self.driver.find_element(
                By.XPATH, '//button[text()="Log in"]').click()
        except:
            pass
        self.__random_sleep()
        # use phone / email / username button
        self.driver.find_element(
            By.XPATH, '//div[text()="Use phone / email / username"]').click()
        # sleep(5)
        self.__random_sleep()
        # log in with email / username
        self.driver.find_element(
            By.XPATH, '//a[text()="Log in with email or username"]').click()
        self.__random_sleep()
        # fill in username and password
        self.driver.find_element(
            By.XPATH, '//input[@name="username"]').send_keys(email)
        self.__random_sleep()
        self.driver.find_element(
            By.XPATH, '//input[@placeholder="Password"]').send_keys(password)
        self.__random_sleep()
        self.driver.find_element(
            By.XPATH, '//button[@type="submit" and text()="Log in"]').click()
        self.__random_sleep()
        # handle captcha by clicking manually
        sleep(30)

    def goto_homepage(self):
        self.driver.get('https://www.tiktok.com')

    def save_screenshot(self, filename):
        return self.driver.save_screenshot(filename)

    # helper methods
    def __random_sleep(self):
        sleep(random.uniform(5, 10))

    def __random_duration(self):
        sleep(random.uniform(2, 5))

    def __log(self, message):
        if self.verbose:
            print(message)

    def __init_chrome(self, profile_dir, headless):
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        if profile_dir is not None:
            options.add_argument('--user-data-dir=%s' % profile_dir)
        if headless:
            options.add_argument('--headless')
        return uc.Chrome(executable_path='./chromedriver', options=options)

    def __init_firefox(self, profile_dir, headless):
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if profile_dir is not None:
            pass
        if headless:
            options.add_argument('--headless')
        return Firefox(options=options)
