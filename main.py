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
longwait = WebDriverWait(driver, 999999)


def get_steamId():
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[7]/div[1]/div/div[3]/a")))
    href_tag = driver.find_element(By.XPATH,"/html/body/div[1]/div[7]/div[1]/div/div[3]/a").get_attribute("href")
    steam_id = href_tag.split("https://steamcommunity.com/id/")[1].split("/")[0]
    return steam_id


def first_login():
    cookies = []
    driver.get("https://steamcommunity.com/login/home/?goto=login")
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input")))
    driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input").send_keys(environ.get("STEAM_USERNAME"))
    driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input").send_keys(environ.get("STEAM_PASSWORD"))
    driver.find_element(By.XPATH, "/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button").click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='acceptAllButton']")))
    print("Waiting for cookie popup..")
    driver.find_element(By.XPATH, "//*[@id='acceptAllButton']").click()
    print("CONFIRM YOUR LOGIN WITH YOUR PHONE!")
    longwait.until(EC.presence_of_element_located((By.XPATH, r"//*[@id='responsive_page_template_content']/div[1]/div[2]/div/div/div/div[3]/div[2]/a")))
    cookies.extend(driver.get_cookies())
    save_cookies("cookies.json", cookies)
    print("LOGGED IN!")


def change_pic_to(pic_path):
    driver.get(f"https://steamcommunity.com/id/{get_steamId()}/edit/avatar")
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[3]/div[2]/div/div[1]/div[3]/div[2]/input"))).send_keys(pic_path)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[3]/div[2]/div/div[2]/button[1]"))).click()
    

def change_name_to(name):
    driver.get(f"https://steamcommunity.com/id/{get_steamId()}/edit/info")
    driver.refresh()
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[3]/div[2]/form/div[3]/div[2]/div[1]/label/div[2]/input")))
    button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[3]/div[2]/form/div[7]/button[1]")))
    input_field.clear()
    input_field.send_keys(name)
    button.click()
   

if "cookies.json" not in os.listdir():
    first_login()


pics = [os.path.abspath("Pics/" + x) for x in os.listdir("Pics/")]
names = ["om♥", "Andrew Tate", "Top G","Elon Musk", "X Æ A-Xii", "OM :3", "Incel", "J E R I C H O"]


driver.get("https://steamcommunity.com")
add_cookies_from_file("cookies.json", driver)
driver.refresh()

name = ""

while True:
    name = random.choice([x for x in names if name != x])
    pic = random.choice(pics)
    change_name_to(name)
    change_pic_to(pic)
    print(f"Name Changed to: {name}")
    print(f"Pic Changed to: {pic}")
    sleep(80)

driver.quit()