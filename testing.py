from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from win32com.client import Dispatch
import urllib.request
import requests
from screenshot import take_screenshot
import getDriver
import download_driver
import os
from pyjson import config, whconfig
import login
import eel
from meeting import Meeting


def attendance():
    print("meeting started ..")
    try:
        meet = Meeting()
    # login.do_login(meet.driver,headless=False)abdfghinop
        login.do_login(meet.driver)
        meet.enter(config.meeting_url)
        meet.open_sidebar()
        meet.close()
        eel.render(whconfig["meeting_data"])()
        print(whconfig["meeting_data"][0])
    except:
        meet.close()


# driver.close()
