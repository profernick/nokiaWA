from flask import Flask, render_template,redirect,url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64
import threading

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--headless=new')
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com/")

def login():
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))

    # this is the qr
    qr_elm = driver.find_element(By.TAG_NAME, 'canvas')
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", qr_elm)
    canvas_png = base64.b64decode(canvas_base64)

    # write qr png data to actual png
    with open("static/images/qrcode.png", "wb") as f:
        f.write(canvas_png)

app = Flask(__name__)
session = {"logged_in": False}

def check_login():
    if WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Chats']"))):
        print("hey it works")
        session["logged_in"] = True

@app.route("/login")
def hello_world():
    # by the time this is called its already fully loaded, thats why speed
    login()
    response = render_template('qr.html')
    threading.Thread(target=check_login).start()
    return response

@app.route("/logged-in")
def logged_in():
    if session.get("logged_in"):
        # continue this, instead of only displaying ur in, start displaying chats!
        return "<p>Ur in...</p>"
    return "<p>U aint in bro...</p>"

@app.route("/chats")
def chats():
    load_chats = driver.execute_script("window.Store = Object.assign({}, window.require('WAWebCollections'));")

    contacts = driver.execute_script("return window.Store.Chat.map(contacts => contacts.formattedTitle);")

    latest_msg = driver.execute_script("return window.Store.Chat._models.flatMap(chatd => window.Store.Chat.get(chatd.id._serialized).msgs._models.slice(-1).map(msg => msg.body));")

    return render_template("chats.html", contacts=contacts, latest=latest_msg)
