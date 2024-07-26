from TikTokDriver import TikTokDriver
import os
from time import sleep
from shutil import rmtree
import json

profile_dir = 'andrew_newman215'
# check if the profile directory exists
if os.path.exists(profile_dir):
    # if it exists, delete it
    rmtree(profile_dir)
    print(f"Directory '{profile_dir}' has been deleted.")
else:
    print(f"Directory '{profile_dir}' does not exist.")

input()
# load the driver
driver = TikTokDriver(use_virtual_display=False, browser="chrome",
                      profile_dir='andrew_newman215')

input("Continue?")
# login with email and pwd
driver.login("qazwu@ucdavis.edu", "1J45jp32l4@")
# collect data at FYP
driver.watch_for_you_page(1)
