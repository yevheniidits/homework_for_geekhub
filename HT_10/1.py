'''
За допомогою Selenium зайти на сайт ОЛХ, ввести в пошук будь-який запит,
дочекатись отримання результатів і зберегти скріншот сторінки.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# target url
url = 'https://www.olx.ua/'
# what you want to search on website
search_input = 'cort x5'

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(executable_path='chromedriver', options=options)
# set window size depending on your screen resolution
driver.set_window_size(1366, 700)

driver.get(url)
try:
    timeout = 30
    wait = WebDriverWait(driver, timeout)
    search_field = wait.until(EC.visibility_of_element_located((By.ID, 'headerSearch')))
    search_field.send_keys(search_input)
    search_field.send_keys(Keys.ENTER)
    # waiting for next page
    target_page = wait.until(EC.visibility_of_element_located((By.ID, 'search-text')))
    # (optional) scroll page down
    driver.execute_script("window.scrollTo(0, 2000)")
    # make screenshot of web-page
    driver.save_screenshot('screenshot.png')

except Exception as error:
    print(error)
finally:
    driver.quit()
