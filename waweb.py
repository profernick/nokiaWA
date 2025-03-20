from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import base64

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

login()

app = Flask(__name__)
@app.route("/login")
def hello_world():
    return render_template('qr.html')
