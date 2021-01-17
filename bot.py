import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class InstaBot():

    # constructor
    def __init__(self, driver_path, speed_factor):
        # default values
        self.followers = []
        self.following = []
        self.sf = speed_factor
        # open chrome instance with instagram url
        self.browser = webdriver.Chrome(executable_path = driver_path)
        self.browser.get('https://www.instagram.com')
        time.sleep(5 * self.sf)

    # authentication
    def authenticate(self, username, password):
        try: 
            # get the input fields
            input_username = self.browser.find_elements_by_css_selector('form input')[0]
            input_password = self.browser.find_elements_by_css_selector('form input')[1]
            # fill the credentials
            input_username.send_keys(username)
            input_password.send_keys(password)
            # enter key = login button click
            input_password.send_keys(Keys.ENTER)
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # wait 5 secs for the page to load
        time.sleep(5 * self.sf)        

    # open profile
    def open_profile(self):
        try:
            # find and toggle profile menu
            profile_link_toggle = self.browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')
            profile_link_toggle.click()
            # sleep 1 sec
            time.sleep(2 * self.sf)
            # find and click profile link
            profile_link = self.browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div')
            profile_link.click()
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # wait 5 secs for the page to load
        time.sleep(5 * self.sf)

    # get followers list
    def get_followers(self):
        print('\nOPENING FOLLOWERS')
        try: 
            # open followers list
            followers_link = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
            followers_count = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
            int(''.join([x for x in list(followers_count) if x.isdigit()]))
            print(followers_count)
            followers_link.click()
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # sleep 3 sec
        time.sleep(3 * self.sf)
        try:
            # get container of followers
            followers_container = self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
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
                self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_container)
                time.sleep(3 * self.sf)
                # increased load times as the list grows
                if count > 350: time.sleep(1 * self.sf)
                if count > 700: time.sleep(1 * self.sf)
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # take each follower and add it to self.followers
        print('SCRAPING ALL LOADED FOLLOWERS\n--------------------------')
        follower_list = followers_container.find_elements_by_css_selector('li')
        for follower in follower_list:
            data = follower.text.split()
            self.followers.append({'username': data[0], 'following': False if data[-1] == 'Follow' else True})
            print(data[0])
        # find and click on close button
        print('---------------\nCLOSING FOLLOWERS\n')
        close_button = self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button')
        close_button.click()
        # wait 2 secs for the list to close
        time.sleep(2 * self.sf)

    # get following list
    def get_following(self):
        # find, count and open following list
        print('\nOPENING FOLLOWING')
        try:
            following_link = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
            following_count = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
            following_count = int(''.join([x for x in list(following_count) if x.isdigit()]))
            following_link.click()
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # sleep 3 sec
        time.sleep(3 * self.sf)
        try:
            # get container of following
            following_container = self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
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
                self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', following_container)
                time.sleep(3 * self.sf)
                # increased load times as the list grows
                if count > 350: time.sleep(1 * self.sf)
                if count > 700: time.sleep(1 * self.sf)
        except:
            # quit if timed out
            self.browser.quit()
            exit(1)
        # take each following and add it to self.following
        print('SCRAPING ALL LOADED FOLLOWING\n----------------------------')
        following_list = following_container.find_elements_by_css_selector('li')
        for following in following_list:
            data = following.text.split()
            self.following.append(data[0])
            print(data[0])
        # find and click on close button
        print('-----------------\nCLOSING FOLLOWING\n')
        close_button = self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button')
        close_button.click()
        # wait 2 seconds for the list to close
        time.sleep(2 * self.sf)

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

    # close selenium driver
    def close(self):
        self.browser.quit()
        exit(0)