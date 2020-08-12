# Instabot
An Instagram bot built using python and selenium. 
Do give a star! :star:

### How to run?
* Substitute your credentials to the empty strings held by **USERNAME** and **PASSWORD** constants in main.py.
* You may want to adjust **SPEED_FACTOR** in main.py according to your processor and internet speed.
  * Lesser speed factor: Faster execution, more easier to fail.
  * Greater speed factor: Slower execution, safer. 
* The project includes a chromedriver in resources folder. Follow the below steps if you want to use a different version or a different browser
  * Download the appropriate driver and extract exe file.
  * Replace chromedriver.exe with newly downloaded driver in resources folder.
  * Change **DRIVER** constant to appropriate path in main.py