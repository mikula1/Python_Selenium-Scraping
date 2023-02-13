import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from logging_helper import logger
import  sys

with webdriver.Chrome(
    service=ChService('../drivers/chromedriver_v109.exe'),
    options=webdriver.ChromeOptions()
) as driver:

    #initiating driver with the given url
    driver.get("https://en.cvbankas.lt")
    logger.info(f"Initiating website and waiting for response")
    assert "CVbankas.lt" in driver.title
    logger.debug("scraper initiated")


    #expand browser window
    driver.maximize_window()
    logger.info("window resized")

    #cookie accept
    accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_button.click()
    logger.info("Cookies accepted")

    #type email
    email_field = driver.find_element(By.ID, "login_email")
    email_field.send_keys(email)

    #type password > enter
    password_field = driver.find_element(By.ID, "login_password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)

    logger.info("login succesfull")

    #go to main page by clicking logo
    button = driver.find_element(By.ID, "project_logo_img")
    button.click()

    #work area dropdown multiselect menu
    button1 = driver.find_element(By.CSS_SELECTOR, "div.filter_work_area_c > div > div > div.input_v4_multiselect_output_c.input_v4.input_v4_dropdown.js_input_v4_multiselect_output")
    button1.click()

    # work area dropdown multiselect IT field
    button2 = driver.find_element(By.CSS_SELECTOR, ".input_v4_multiselect_list > .input_v4_checkbox_label:nth-child(9) > .input_v4_checkbox_label_text")
    button2.click()

    #button filter click
    button3 = driver.find_element(By.ID,"main_filter_submit")
    button3.click()

    #time needed to load the page
    logger.info("loading...")
    time.sleep(2)


    #gathering jobs
    jobs = driver.find_elements(By.CSS_SELECTOR, ".list_h3")
    logger.info(f"Job ads found {len(jobs)}")

    #gathering salaries
    salaries = driver.find_elements(By.CSS_SELECTOR, "div.list_cell.jobadlist_list_cell_salary")

    #gathering urls
    urls_list = driver.find_elements(By.CSS_SELECTOR, "a.list_a")
    urls = [url.get_attribute("href") for url in urls_list]

    class JobTitlePayLink:
        def __init__(self, title, pay, link):
            self.title = title
            self.pay = pay
            self.link = link


    class Job(JobTitlePayLink):
        def __init__(self, title, pay, link, location):
            super().__init__(title, pay, link)
            self.location = location


    def average(num_list):
        return sum(num_list)/len(num_list)


    job_list = []
    lost = 0

    #itterating through (jobs,salaries,urls)
    for job, salary, url in zip(jobs, salaries, urls):
        #if ad doesn't contain a value we skip it and mark it as lost data
        if salary.text == "":
            lost = lost + 1
            continue
        #splitting when there are more than one value
        salary_value = salary.find_element(By.CSS_SELECTOR, "span.salary_amount").text.split("-")
        if len(salary_value)>1:
            salary_value = average(list(map(int, salary_value)))
        else:
            try:
                salary_value = int(salary_value[0].split(" ")[1])
            except IndexError:
                logger.warning("skipped salary")
        #assign job text, salary value, url of the job ad to class JobTitlePayLink
        job_list.append(JobTitlePayLink(job.text, salary_value, url))

    #printing and logging how many of the job ads ve lost because of no salary
    sys.stderr.write(f"Job ads lost: {lost}\n")
    logger.error(f"Job ads lost {lost}")

    Job_list = []
    # visit pages, get cities
    for job in job_list:
        driver.get(job.link)
        cities = driver.find_elements(By.CSS_SELECTOR, "span > a > span")
        city_list = []
        for city in cities:
            city_list.append(city.text)
        Job_list.append(Job(job.title,job.pay,job.link,city_list))
        time.sleep(1)

    #print Job objects in dictionary format
    for Job in Job_list:
        logger.info("Finished! Displaying what I gathered")
        print(Job.__dict__)

    time.sleep(10)
    driver.close()
