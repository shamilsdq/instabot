from bot import InstaBot


# credentials
USERNAME = ''
PASSWORD = ''

# create an instabot instance
bot = InstaBot()

# login and navigate to profile page
bot.authenticate(USERNAME, PASSWORD)
bot.open_profile()

# get followers and followings details
bot.get_following()
bot.get_followers()

# get followers we don't follow back
for user in bot.get_following_only():
    print(user)