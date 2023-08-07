from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

s = Service('./geckodriver.exe')
driver = webdriver.Firefox(service=s)
driver.implicitly_wait(5)
driver.set_window_size(1920, 1080)
driver.get('https://account.mail.ru')
elem = driver.find_element(By.NAME, 'username')
elem.send_keys('study.ai_172')
elem = driver.find_element(By.CLASS_NAME, 'base-0-2-87').click()
elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')
time.sleep(2)
elem = driver.find_element(By.XPATH, "//button[@type = 'submit']").click()

test = driver.find_element(By.XPATH, "//a[contains(@class, 'llc')]").get_attribute('href')

element = driver.find_element(By.XPATH, "//div[contains(@class, 'ReactVirtualized')]")
msg_refs = []
for i in range(70):
    msg = driver.find_elements(By.XPATH, "//a[contains(@class, 'llc')]")
    for m in msg:
        msg_refs.append(m.get_attribute('href'))

    time.sleep(2)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
    print(i)
    time.sleep(1)

msg_refs_set = set(msg_refs)

msg_information = []

for msg in msg_refs_set:
    msg_dict = {}
    driver.get(msg)
    wait = WebDriverWait(driver, 25)
    msg_source = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
    msg_sender = msg_source.find_element(By.XPATH, ".//span[@class='letter-contact']")
    msg_dict['author'] = f"{msg_sender.text} {msg_sender.get_attribute('title')}"
    msg_date = msg_source.find_element(By.XPATH, ".//div[@class = 'letter__date']")
    msg_dict["date"] = msg_date.text
    msg_thread = driver.find_element(By.XPATH, "//h2[@class = 'thread-subject']")
    msg_dict["thread"] = msg_thread.text
    msg_text = driver.find_element(By.XPATH, "//div[@class = 'letter-body']")
    msg_dict["text"] = msg_text.text
    msg_information.append(msg_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['messages']
mail_db = db.mail_db

for item in msg_information:
    try:
        mail_db.insert_one(item)
    except DuplicateKeyError:
        print(f'item  already exists')
