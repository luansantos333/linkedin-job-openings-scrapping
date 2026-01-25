import os
import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_site():
    options = Options()

    options.binary_location = str(os.getenv("BROWSER_LOCATION"))
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(r'user-data-dir=' + os.getenv("PROFILE_DATA_DIR"))
    options.add_experimental_option("detach", True)
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))

    web = webdriver.Chrome(service=service, options=options)

    web.get("https://www.glassdoor.com.br")
    wait = WebDriverWait(web, 10)

    all_jobs = []
    list_functions = ['Python', 'Java', 'Suporte Técnico', 'Redes', 'Infraestrutura', 'DevOps', 'SRE', 'Desenvolvedor',
                      'Desenvolvedora']
    try:
        ## VALIDATES WEATHER THE USER IS LOGGED IN
        time.sleep(1)
        home_page_google_login_btn = web.find_elements(By.XPATH,
                                                       '//*[@id="InlineLoginModule"]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div/button')

        if not len(home_page_google_login_btn) == 0:
            google_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "colorCtaGoogle")))
            google_login.click()
            web.switch_to.window(web.window_handles[1])
            ## VERIFY IF THERE IS NOT A GOOGLE ACCOUNT ALREADY LOGGED
            if not web.find_element(By.XPATH,
                                    '//*[@id="yDmH0d"]/c-wiz/main/div[2]/div/div/div[1]/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[2]'):
                web.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(os.getenv("GOOGLE_EMAIL"))
                web.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
                password = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
                password.send_keys(os.getenv("GOOGLE_PASSWORD"))
                confirm = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button/div[3]')))
                actions = ActionChains(web)
                actions.move_to_element(confirm).click().perform()
            else:
                web.find_element(By.CLASS_NAME, "yAlK0b").click()
                wait._timeout = 5
                ## IF NO CONFIRMATION DIALOG SHOWS UP
                if not wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/main/div[3]/div/div/div[2]/div/div/button'))):
                    web.switch_to.window(web.window_handles[0])
                    wait._timeout = 10
                    ## LOGIN BUTTON GLASSDOOR
                    login_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="AuthPromptModalContainer"]/div/div/dialog/div[2]/div[2]/div/div/button')))
                    login_btn.click()
                    # IF GLASSDOOR ASK FOR CONFIRMATION
                    time.sleep(1)
                    if not len(web.window_handles) == 1:
                        web.switch_to.window(web.window_handles[1])
                        web.find_element(By.ID, 'onetrust-accept-btn-handler').click()
                        form = web.find_element(By.ID, 'emailform')
                        form.find_element(By.TAG_NAME, 'button').click()
                        web.find_element(By.ID, 'googleContainer').click()
                    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ji8JI0ibjBNKYy6dBuvi')))
                    count = 1000
                    for i in range(1, 10):
                        jobs = web.find_elements(By.CLASS_NAME, "JobCard_jobCardLeftContent__cHcGe")
                        for job in jobs:
                            job_title = job.find_elements(By.TAG_NAME, 'a')[0].text
                            if any(keyword.lower() in job_title.lower() for keyword in list_functions):
                                job_info = {"vaga": job_title,
                                            "link": job.find_elements(By.TAG_NAME, "a")[1].get_attribute("href")}
                                all_jobs.append(job_info)

                        web.execute_script(f"window.scrollTo(0,{count});")
                        time.sleep(2)
                        count = count * i
                else:
                    actions = ActionChains(web)
                    confirm = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/main/div[3]/div/div/div[2]/div/div/button')))
                    actions.move_to_element(confirm).click().perform()
                    web.switch_to.window(web.window_handles[0])
                    login_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="AuthPromptModalContainer"]/div/div/dialog/div[2]/div[2]/div/div/button')))
                    login_btn.click()
                    # IF GLASSDOOR ASK FOR CONFIRMATION
                    time.sleep(1)
                    if not len(web.window_handles) == 1:
                        web.switch_to.window(web.window_handles[1])
                        web.find_element(By.ID, 'onetrust-accept-btn-handler').click()
                        form = web.find_element(By.ID, 'emailform')
                        form.find_element(By.TAG_NAME, 'button').click()
                        web.find_element(By.ID, 'googleContainer').click()
                    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ji8JI0ibjBNKYy6dBuvi')))
                    count = 1000
                    for i in range(1, 10):
                        jobs = web.find_elements(By.CLASS_NAME, "JobCard_jobCardLeftContent__cHcGe")
                        for job in jobs:
                            job_title = job.find_elements(By.TAG_NAME, 'a')[0].text
                            if any(keyword.lower() in job_title.lower() for keyword in list_functions):
                                job_info = {"vaga": job_title,
                                            "link": job.find_elements(By.TAG_NAME, "a")[1].get_attribute("href")}
                                all_jobs.append(job_info)

                        web.execute_script(f"window.scrollTo(0,{count});")
                        time.sleep(2)
                        count = count * i
        else:
            ## EXECUTE IF USER IS LOGGED IN
            count = 1000
            for i in range(1, 10):
                jobs = web.find_elements(By.CLASS_NAME, "JobCard_jobCardLeftContent__cHcGe")
                for job in jobs:
                    job_title = job.find_elements(By.TAG_NAME, 'a')[0].text
                    if any(keyword.lower() in job_title.lower() for keyword in list_functions):
                        job_info = {"vaga": job_title,
                                    "link": job.find_elements(By.TAG_NAME, "a")[1].get_attribute("href")}
                        all_jobs.append(job_info)

                web.execute_script(f"window.scrollTo(0,{count});")
                time.sleep(2)
                count = count * i


    except TimeoutException as e:
        print(e.msg)
    finally:
        print("--------------------------------\n\n")

    jobs_tuple = {tuple(sorted(d.items(), reverse=True)) for d in all_jobs}
    for job in jobs_tuple:
        print(job)

    web.close()


if __name__ == '__main__':
    scrape_site()
