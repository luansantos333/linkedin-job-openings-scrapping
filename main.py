import os

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def scrape_site():
    options = Options()

    options.binary_location = str(os.getenv("BROWSER_LOCATION"))
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
    web = webdriver.Chrome(service=service, options=options)
    web.get("https://www.glassdoor.com.br")
    wait = WebDriverWait(web, 10)
    try:
        google_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "colorCtaGoogle")))
        google_login.click()
        web.switch_to.window(web.window_handles[1])
        web.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(os.getenv("GOOGLE_EMAIL"))
        web.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
        password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        password.send_keys(os.getenv("GOOGLE_PASSWORD"))
        confirm = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button/div[3]')))
        actions = ActionChains(web)
        actions.move_to_element(confirm).click().perform()

        # web.execute("arguments[0].click();")

    except TimeoutException as e:
        print (e.msg)
    # finally:
        #web.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_site()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
