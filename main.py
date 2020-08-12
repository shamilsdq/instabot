from bot import InstaBot


# credentials
USERNAME = ''
PASSWORD = ''
SPEED_FACTOR = 1

# create an instabot instance
bot = InstaBot(USERNAME, PASSWORD, SPEED_FACTOR)

# login and navigate to profile page
bot.authenticate()
bot.open_profile()

# get followers and followings details
bot.get_followers()
bot.get_following()

# get following who don't follow us back
print('\n\nNOT FOLLOWING YOU BACK\n---------------------')
for user in bot.get_following_only():
    print(user)

# get followers we don't follow back
print('\n\nNOT FOLLOWING THEM BACK\n--------------------')
for user in bot.get_follower_only():
    print(user)