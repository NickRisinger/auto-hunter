import time
from xmlrpc.client import Boolean

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


def find_element(driver: WebDriver, by: str = By.ID, value: str | None = None):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None

def auth(driver: WebDriver, username: str, password: str):
    print("Начинаю авторизацию...\n")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//form[@data-qa="account-signup"]'))
    )
    auth_form_element = find_element(driver, By.XPATH, '//form[@data-qa="account-signup"]')
    auth_form_element.find_element(By.CSS_SELECTOR, 'a[data-qa="expand-login-by-password"]').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="login-input-username"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[data-qa="login-input-password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[data-qa="account-login-submit"]').click()
    time.sleep(5)

def main():
    driver = webdriver.Chrome()
    driver.get("https://hh.ru/search/vacancy?customDomain=1&area=1&search_field=name&search_field=company_name&search_field=description&text=аналитик&enable_snippets=false&salary=15000&only_with_salary=true")

    login_button_element = find_element(driver, By.XPATH, '//a[@data-qa="login"]')

    if login_button_element:
        login_button_element.click()
        auth(driver, "79960492309", "Nasasal00")


    while True:
        cards = driver.find_elements(By.XPATH, "//div[starts-with(@data-qa, 'vacancy-serp__vacancy')]")

        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]')
            print(f'({title.get_attribute("href")} - {title.text})')

        next_button_element = find_element(driver, By.XPATH, '//a[@data-qa="number-pages-next"]')

        if next_button_element:
            time.sleep(20)
            break

        next_button_element.click()


    driver.quit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass