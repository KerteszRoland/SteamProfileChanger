from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import sys
from os import environ
from dotenv import load_dotenv
import requests
from tkinter import *
from tkinter import messagebox, simpledialog
from subprocess import CREATE_NO_WINDOW


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
chrome_options.add_argument("--resolution=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-crash-reporter")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-in-process-stack-traces")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
service = Service(executable_path=ChromeDriverManager().install())
service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=service, options=chrome_options)


def first_login():
    driver.get("https://steamcommunity.com/login")
    driver.find_element(By.ID, "input_username").send_keys(environ.get("STEAM_USERNAME"))
    driver.find_element(By.ID, "input_password").send_keys(environ.get("STEAM_PASSWORD"))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "rejectAllButton"))).click()
    driver.find_element(By.XPATH, "//*[@id=\"login_btn_signin\"]/button").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "twofactorcode_entry")))
    code_2fa = simpledialog.askstring("Input", "Steam Guard code:", parent=root)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "twofactorcode_entry"))).send_keys(code_2fa)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#login_twofactorauth_buttonset_entercode > div.auth_button.leftbtn"))).click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "profile_avatar_frame")))
    save_cookies("cookies.json", driver.get_cookies())
    
    
def change_pic_to(pic_path):
    driver.get("https://steamcommunity.com/id/user/edit/avatar")
    add_cookies_from_file("cookies.json", driver)
    driver.refresh()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/div/div[1]/div[3]/div[2]/input"))).send_keys(pic_path)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/div/div[2]/button[1]"))).click()
    

def change_name_to(name):
    driver.get("https://steamcommunity.com/id/user/edit/info")
    add_cookies_from_file("cookies.json", driver)
    driver.refresh()
    input_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/form/div[3]/div[2]/div[1]/label/div[2]/input")))
    button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='application_root']/div[2]/div[2]/form/div[7]/button[1]")))
    input_field.clear()
    input_field.send_keys(name)
    button.click()
   

def get_profile_name_and_pic(link):
    driver.get(link)
    display_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "actual_persona_name"))).text
        
    pic_element = driver.find_element(By.CLASS_NAME, 'playerAvatarAutoSizeInner').find_elements(By.TAG_NAME, "img")[-1]
    pic = pic_element.get_attribute("src")
    return display_name, pic


def copy_profile():
    copy_link = entry.get()
    entry.delete(0, END)
    name, pic = get_profile_name_and_pic(copy_link)
    change_name_to(name)
    media = requests.get(pic)
    with open("temp.jpg", "wb") as file:
        file.write(media.content)
    change_pic_to(os.path.abspath("temp.jpg"))
    

root = Tk()
if "cookies.json" not in os.listdir():
    first_login()
entry = Entry(root, width=50)
entry.pack()
myButton = Button(root, text="Copy profile", command=copy_profile)
myButton.pack()
root.mainloop()
driver.quit()
