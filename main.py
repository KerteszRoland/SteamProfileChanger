from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import os
from os import environ
from dotenv import load_dotenv
import random


load_dotenv()


def save_cookies(cookies_file, cookies):
    with open(cookies_file, "w") as f:
        json.dump(cookies, f)


def add_cookies_from_file(cookies_file, driver):
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            if cookie["domain"] in driver.current_url.split("/")[2]:
                driver.add_cookie(cookie)


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-crash-reporter")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-in-process-stack-traces")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--output=/dev/null")
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)


def first_login():
    cookies = []
    driver.get("https://steamcommunity.com/login")
    driver.find_element(By.ID, "input_username").send_keys(environ.get("STEAM_USERNAME"))
    driver.find_element(By.ID, "input_password").send_keys(environ.get("STEAM_PASSWORD"))
    driver.find_element(By.XPATH, "//*[@id=\"login_btn_signin\"]/button").click()
    wait.until(EC.presence_of_element_located((By.ID, "twofactorcode_entry")))
    print("Type your 2FA code: ", end=" ")
    code_2fa = input()
    driver.find_element(By.ID, "twofactorcode_entry").send_keys(code_2fa)
    driver.find_element(By.XPATH, "//*[@id='login_twofactorauth_buttonset_entercode']/div[1]").click()
    cookies.extend(driver.get_cookies())
    wait.until(EC.presence_of_element_located((By.XPATH, r"//*[@id='global_actions']/a"))).click()
    cookies.extend(driver.get_cookies())
    save_cookies("cookies.json", cookies)


def change_pic_to(pic_path):
    driver.get("https://steamcommunity.com/id/user/edit/avatar")
    add_cookies_from_file("cookies.json", driver)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/div/div[1]/div[3]/div[2]/input"))).send_keys(pic_path)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/div/div[2]/button[1]"))).click()
    

def change_name_to(name):
    driver.get("https://steamcommunity.com/id/user/edit/info")
    add_cookies_from_file("cookies.json", driver)
    driver.refresh()
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/form/div[3]/div[2]/div[1]/label/div[2]/input")))
    button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/form/div[7]/button[1]")))
    input_field.clear()
    input_field.send_keys(name)
    button.click()
   

if "cookies.json" not in os.listdir():
    first_login()


pics = [os.path.abspath("Pics/" + x) for x in os.listdir("Pics/")]
names = ["Joe Biden", "Gordon Ramsy", "Simple", "Lecsi <3", "kennyS", "Happy holidays <3!", "Elon Musk the 2nd", "X Æ A-Xii", "OM"]


while True:
    name_index = random.randrange(0, len(names))
    pic_index = random.randrange(0, len(pics))
    change_name_to(names[name_index])
    print(f"Name Changed to: {names[name_index]}")
    change_pic_to(pics[pic_index])
    print(f"Pic Changed to: {pics[pic_index]}")
    sleep(120)

driver.quit()