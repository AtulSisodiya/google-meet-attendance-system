from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from screenshot import take_screenshot
import getDriver
import download_driver
import os
from pyjson import config, whconfig, write_data
from datetime import datetime

opt = Options()


opt.add_argument("--disable-infobars")
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_argument("--headless")
opt.add_argument("--mute-audio")
# opt.add_argument('--disable-dev-shm-usage')
opt.add_argument("--no-sandbox")
opt.add_argument("--disable-gpu")
opt.add_argument("--log-level=3")
# opt.add_argument('--allow-running-insecure-content')
# opt.add_argument('--ignore-certificate-errors')
opt.add_argument("--allow-insecure-localhost")
opt.add_argument("--disable-software-rasterizer")
opt.add_argument("--use-fake-device-for-media-stream")
opt.add_argument("--use-fake-ui-for-media-stream")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option(
    "prefs",
    {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 1,
    },
)


class Meeting:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(
                chrome_options=opt, executable_path=config.driver_location
            )
        except Exception as e:
            driver_loc = getDriver.driver_handler()
            self.driver = webdriver.Chrome(
                chrome_options=opt, executable_path=driver_loc
            )

    def enter(self, url):
        self.driver.get(url)
        self.driver.find_elements_by_css_selector(config.landing_page_btns)
        self.driver.implicitly_wait(20)
        print("waited loading page")
        element_present = EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, '[class="Sla0Yd"] [role="button"]:nth-of-type(1)')
        )
        WebDriverWait(self.driver, config.timeout).until(element_present)

        self.driver.execute_script(
            f"""document.querySelectorAll("{config.landing_page_btns}")[0].click()"""
        )
        sleep(1)
        self.driver.execute_script(
            f"""document.querySelectorAll("{config.landing_page_btns}")[1].click()"""
        )
        sleep(1)
        self.driver.execute_script(
            f"""document.querySelectorAll('[class="Sla0Yd"] [role="button"]:nth-of-type(1)')[0].click()"""
        )
        print("landing page button clicked")

    def open_sidebar(self):
        # main screen of meeting
        print("waiting to enter into meeting")
        self.driver.save_screenshot("enter.png")
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[class=NzPR9b] [role=button]:first-of-type")
        )
        WebDriverWait(self.driver, config.timeout).until(element_present)
        try:
            self.driver.execute_script(
                f"""Array(...document.querySelectorAll("audio")).forEach(ele=>{{ele.muted=true}})"""
            )
            self.driver.execute_script(
                f"""document.querySelectorAll("[class=NzPR9b] [role=button]:first-of-type")[0].click()"""
            )
        except:
            sleep(10)
            self.driver.execute_script(
                f"""document.querySelectorAll("{config.sidebar_btn}")[3].click()"""
            )

        print("Entered into Meeting..")

        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, config.tab_btn)
        )
        WebDriverWait(self.driver, config.timeout).until(element_present)
        self.driver.execute_script(
            f"""
        document.querySelectorAll("{config.tab_btn}")[0].click()"""
        )

        element_present = EC.visibility_of_element_located(
            (By.CSS_SELECTOR, config.tab_panel)
        )
        WebDriverWait(self.driver, config.timeout).until(element_present)
        add_data = self.driver.find_elements(By.CSS_SELECTOR, ".Dxboad")
        names = []
        self.driver.save_screenshot("people.png")
        sr, cl, sw = self.driver.execute_script(
            f"""
        let sr=document.querySelector("[role=tabpanel]").scrollHeight;
        let sw=document.querySelector("[role=tabpanel]").scrollWidth;
        let cl=document.querySelector("[role=tabpanel]").clientHeight;
        return [sr,cl,sw]
        """
        )
        self.driver.execute_script(
            f"""
        document.querySelector("[role=tabpanel]").scrollTo(0,0);
        """
        )
        count = 0
        while sr > (-cl):
            self.driver.save_screenshot(f"people{count}.png")
            add_data = self.driver.find_elements(By.CSS_SELECTOR, ".Dxboad")
            for i in add_data:
                names.append(i.text)
            print(names)
            count += 1
            add_data = self.driver.execute_script(
                f"""
            const data=[]
            document.querySelector("[role=tabpanel]").scrollTo(0,{count*cl});
            Array(...document.getElementsByClassName("Dxboad")).forEach(ele=>{{
            data.push(ele.textContent)
            return data}})
            """
            )
            sr -= cl
        print(names)
        names = set(names)
        print(names)
        names = list(names)
        names.sort()
        print(names)
        names.insert(0, datetime.now().strftime("%d-%m-%Y (%I:%M %p)"))
        whconfig["meeting_data"].append(names)
        write_data(whconfig)
        sidepanel = self.driver.find_element_by_css_selector(config.tab_panel)
        imagename = datetime.now().strftime("%d-%m-%Y (%I;%M %p)") + ".png"
        print(imagename)
        take_screenshot(
            self.driver,
            config.tab_panel,
            os.path.join(whconfig["image_location"], imagename),
        )
        sleep(3)

    def close(self):
        self.driver.close()
