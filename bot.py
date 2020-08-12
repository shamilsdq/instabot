import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class InstaBot():

    # constructor
    def __init__(self, username, password, speed_factor):
        # default values
        self.followers = []
        self.following = []
        self.__username = username
        self.__password = password
        self.sf = speed_factor
        # open chrome instance with instagram url
        self.chrome = webdriver.Chrome(executable_path = 'resources/chromedriver.exe')
        self.chrome.get('https://www.instagram.com')
        # wait 3 secs for the page to load
        time.sleep(3 * self.sf)

    # authentication
    def authenticate(self):
        # get the input fields
        input_username = self.chrome.find_elements_by_css_selector('form input')[0]
        input_password = self.chrome.find_elements_by_css_selector('form input')[1]
        # fill the credentials
        input_username.send_keys(self.__username)
        input_password.send_keys(self.__password)
        # enter key = login button click
        input_password.send_keys(Keys.ENTER)
        # wait 3 secs for the page to load
        time.sleep(3 * self.sf)

    # open profile
    def open_profile(self):
        # find and toggle profile menu
        profile_link_toggle = self.chrome.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')
        profile_link_toggle.click()
        # sleep 1 sec
        time.sleep(1 * self.sf)
        # find and click profile link
        profile_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div')
        profile_link.click()
        # wait 3 secs for the page to load
        time.sleep(3 * self.sf)

    # get followers list
    def get_followers(self):
        # find, count and open followers list
        print('\nOPENING FOLLOWERS')
        followers_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_count = int(self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
        followers_link.click()
        # sleep 3 sec
        time.sleep(3 * self.sf)
        # get container of followers
        followers_container = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # loop scroll till all followers are lazy-loaded
        print('LAZY-LOADING ALL FOLLOWERS')
        count = 0
        while True:
            new_count = len(followers_container.find_elements_by_css_selector('li'))
            if new_count <= count:
                if new_count != followers_count: print('COMPLETED SCRAPING FOLLOWERS WITH COUNT MISMATCH')
                else: print('COMPLETED SCRAPING FOLLOWERS LIST SUCCESSFULLY')
                break
            count = new_count
            self.chrome.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_container)
            time.sleep(3 * self.sf)
            # increased load times as the list grows
            if count > 350: time.sleep(1 * self.sf)
            if count > 700: time.sleep(1 * self.sf)
        # take each follower and add it to self.followers
        print('SCRAPING ALL LOADED FOLLOWERS\n--------------------------')
        follower_list = followers_container.find_elements_by_css_selector('li')
        for follower in follower_list:
            data = follower.text.split()
            self.followers.append({'username': data[0], 'following': False if data[-1] == 'Follow' else True})
            print(data[0])
        # find and click on close button
        print('---------------\nCLOSING FOLLOWERS\n')
        close_button = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')
        close_button.click()
        time.sleep(1 * self.sf)

    # get following list
    def get_following(self):
        # find, count and open following list
        print('\nOPENING FOLLOWING')
        following_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
        following_count = int(self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
        following_link.click()
        # sleep 3 sec
        time.sleep(3 * self.sf)
        # get container of following
        following_container = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # loop scroll till all following are lazy-loaded
        print('LAZY LOADING ALL FOLLOWING')
        count = 0
        while True:
            new_count = len(following_container.find_elements_by_css_selector('li'))
            if new_count <= count:
                if new_count != following_count: print('COMPLETED SCRAPING FOLLOWING WITH COUNT MISMATCH ({new_count}/{following_count})')
                else: print('COMPLETED SCRAPING FOLLOWING SUCCESSFULLY ({new_count}/{following_count})')
                break
            count = new_count
            self.chrome.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', following_container)
            time.sleep(3 * self.sf)
            # increased load times as the list grows
            if count > 350: time.sleep(1 * self.sf)
            if count > 700: time.sleep(1 * self.sf)
        # take each following and add it to self.following
        print('SCRAPING ALL LOADED FOLLOWING\n----------------------------')
        following_list = following_container.find_elements_by_css_selector('li')
        for following in following_list:
            data = following.text.split()
            self.following.append(data[0])
            print(data[0])
        # find and click on close button
        print('-----------------\nCLOSING FOLLOWING\n')
        close_button = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')
        close_button.click()
        time.sleep(1 * self.sf)

    # get following who don't follow back
    def get_following_only(self):
        result = []
        for x in self.following:
            flag = False
            for y in self.followers:
                if x == y['username']:
                    flag = True
                    break
            if flag == False:
                result.append(x)
        return result

    # get followers who aren't followed back
    def get_follower_only(self):
        # check following status in each of followers
        result = [x['username'] for x in self.followers if x['following'] == False]
        return result