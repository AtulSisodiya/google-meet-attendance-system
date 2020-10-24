from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from pyjson import config
import re


def do_login(driver, headless=True):
    driver.get("https://stackoverflow.com/users/signup")
    element = WebDriverWait(driver, 100).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, "//*[@id='openid-buttons']/button[1]")
        )
    )
    sleep(10)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    print("stackoverflow button clicked")
    driver.save_screenshot("google.png")
    authcheck = "oauth2" in driver.current_url
    print(authcheck, driver.current_url)
    if authcheck == True:
        element = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        sleep(10)
        print(driver.page_source)
        html = driver.execute_script(
            "return document.getElementsByTagName('body')[0].innerHTML"
        )
        print(html)
        driver.save_screenshot("google1.png")
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(config.email)
        driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        element_present = EC.element_to_be_clickable(
            (By.XPATH, '//input[@type="password"]')
        )
        WebDriverWait(driver, config.timeout).until(element_present)
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(
            config.password
        )
        driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        driver.save_screenshot("google2.png")

    if authcheck == False:
        element = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='Email']"))
        )
        driver.find_element(By.CSS_SELECTOR, "input[id='Email']").send_keys(
            config.email
        )
        driver.find_element(By.CSS_SELECTOR, "input[id='next']").click()
        print("email entered")

        driver.save_screenshot("google1.png")
        element_present = EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[id='password']")
        )
        WebDriverWait(driver, config.timeout).until(element_present)
        driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(
            config.password
        )
        driver.find_element(By.CSS_SELECTOR, "input[id='submit']").click()
        print("password entered")
        driver.save_screenshot("google2.png")

    element_present = EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[class='-logo js-gps-track']")
    )
    WebDriverWait(driver, config.timeout).until(element_present)
    return


# driver.get(redirect_url)
