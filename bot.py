import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class InstaBot():

    # constructor
    def __init__(self):
        # default values
        self.followers = []
        self.following = []
        # open chrome instance with instagram url
        self.chrome = webdriver.Chrome(executable_path = 'resources/chromedriver.exe')
        self.chrome.get('https://www.instagram.com')
        # wait 3 secs for the page to load
        time.sleep(3)

    # authentication
    def authenticate(self, username, password):
        # get the input fields
        input_username = self.chrome.find_elements_by_css_selector('form input')[0]
        input_password = self.chrome.find_elements_by_css_selector('form input')[1]
        # fill the credentials
        input_username.send_keys(username)
        input_password.send_keys(password)
        # enter key = login button click
        input_password.send_keys(Keys.ENTER)
        # wait 3 secs for the page to load
        time.sleep(3)

    # open profile
    def open_profile(self):
        # find and toggle profile menu
        profile_link_toggle = self.chrome.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')
        profile_link_toggle.click()
        # sleep 1 sec
        time.sleep(1)
        # find and click profile link
        profile_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div')
        profile_link.click()
        # wait 3 secs for the page to load
        time.sleep(3)

    # get followers list
    def get_followers(self):
        # find, count and open followers list
        followers_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_count = int(self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
        followers_link.click()
        # sleep 1.5 sec
        time.sleep(3)
        # get container of followers
        followers_container = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # loop scroll and scrape followers' name
        count = 0
        while followers_count > count:
            displayed_followers = followers_container.find_elements_by_css_selector('li')
            # sometimes, the total and displayed followers number mismatch
            if count == len(displayed_followers):
                print('completed scraping with a count mismatch')
                break
            while count < len(displayed_followers):
                # details container
                follower_details = displayed_followers[count].text.split()
                follower = {}
                follower['username'] = follower_details[0]
                follower['following'] = False if follower_details[-1] == 'Follow' else True
                self.followers.append(follower)
                print(follower['username'])
                count += 1
            # show percent users scraped
            print('Followers Scraping Progress in percentage: %.2f' % (100 * count/followers_count))
            print('Followers scraped = ' + str(count) + '/' + str(followers_count))
            self.chrome.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_container)
            time.sleep(3)
            if count > 200: time.sleep(1)
        # find and click on close button
        close_button = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')
        close_button.click()

    # get following list
    def get_following(self):
        # find, count and open following list
        following_link = self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')
        following_count = int(self.chrome.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text)
        following_link.click()
        # sleep 1.5 sec
        time.sleep(3)
        # get container of followers
        following_container = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # loop scroll and scrape followings' name
        count = 0
        while following_count > count:
            displayed_following = following_container.find_elements_by_css_selector('li')
            # sometimes, the total and displayed followings number mismatch
            if count == len(displayed_following):
                print('finished scraping with a count mismatch')
                break
            while count < len(displayed_following):
                # details container
                following_details = displayed_following[count].text.split()
                self.following.append(following_details[0])
                print(following_details[0])
                count += 1
            print('Following Scraping progress in percentage: %.2f' % (100 * count/following_count))
            print('Following scraped = ' + str(count) + '/' + str(following_count))
            self.chrome.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_container)
            time.sleep(3)
            if count > 200: time.sleep(1)
        # find and click on close button
        close_button = self.chrome.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')
        close_button.click()

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