import time

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


сover_letter = 'Добрый день! Меня зовут Ольга и меня очень заинтересовала вакансия Аналитика в Вашей компании. Есть опыт проведения как бизнес-, так и системного анализа в ИТ-компаниях и ИТ-подразделениях, как для внешних, так и для внутренних клиентов. Участвовала в качестве аналитика в разработке витрин данных, отчетности как клиентской, так и регуляторной, ИТ-продукта - приложения для сдачи банковской отчетности, микросервисов, используемых в проектах ИИ в инфраструктуре Подмосковья, финансовой отчетности для руководства в компании, специализирующейся на программе лояльности. Кроме этого исполняла роли аналитика CRM, аналитика клиентского опыта, процессного аналитика. В разделе О себе моего резюме есть ссылка на сайт бизнес-карточку, перейдя по которой можно посмотреть все проекты, в которых я участвовала в качестве аналитика, с какими СУБД работала. Совокупный опыт работы в бизнес-анализе более 3 лет, общий стаж более 13 лет, предметная область - банковская деятельность, инвестиции, финансы. Владею приложениями- графическими редакторами для моделирования процессов, в том числе в нотации BPMN 2.0, могу отрисовать макет интерфейса в Figma, пишу запросы на SQL. Работала по методологии Agile с ведением бизнес-документации в вики-системе Confluence. Ориентирована на продукт и на результат, заинтересована в постоянном совершенствовании навыков. Зарплатные ожидания зависят от политики компании, достойным для фуллстек аналитика считаю вознаграждение, релевантное опыту и загрузке, в пределах 200-250 тыс. рублей. Буду благодарна за обратную связь. И буду рада стать частью Вашей команды!'


def find_element(driver: WebDriver, by: str = By.ID, value: str | None = None):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None

def auth(driver: WebDriver, username: str, password: str):
    print("Провожу авторизацию...")
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

def get_links(driver: WebDriver):
    print("Начинаю сбор вакансий...")
    page = 1
    links = []

    while True:
        page = page + 1
        cards = driver.find_elements(By.XPATH, "//div[starts-with(@data-qa, 'vacancy-serp__vacancy')]")

        for card in cards:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
            try:
                title = card.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]')

                links.append(title.get_attribute('href'))
            except NoSuchElementException:
                continue

        try:
            next_page = find_element(driver, By.XPATH, f'//a[@data-qa="number-pages-{page} "]')
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_page)
            time.sleep(5)
            next_page.click()
        except WebDriverException as e:
            print("Вакансии просмотрены, начинаю оставлять отклики")
            break

        time.sleep(5)

    return links

def apply_to_job(driver, job_url):
    try:
        # Переход по ссылке на вакансию
        driver.get(job_url)
        time.sleep(3)  # Задержка для загрузки страницы

        # Нажимаем кнопку "Откликнуться"
        apply_button = driver.find_element(By.XPATH, '//a[@data-qa="vacancy-response-link-top"]')
        apply_button.click()
        time.sleep(2)  # Ожидание для открытия модалки или перехода на другую страницу

        # Проверка первого сценария: модальное окно с textarea
        try:
            modal_textarea = driver.find_element(By.TAG_NAME, 'textarea')
            modal_textarea.send_keys(сover_letter)
            submit_button = driver.find_element(By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')
            submit_button.click()
            print("Отклик отправлен через модальное окно.")
            return
        except:
            pass

        # Проверка второго сценария: скролл вниз для появления textarea
        try:
            time.sleep(3)  # Ожидание для подгрузки
            show_textarea_button = driver.find_element(By.XPATH, '//button[@data-qa="vacancy-response-letter-toggle"]')
            show_textarea_button.click()
            time.sleep(1)  # Задержка для отображения textarea
            page_textarea = driver.find_element(By.TAG_NAME, 'textarea')
            page_textarea.send_keys(сover_letter)
            submit_button = driver.find_element(By.XPATH, '//button[@data-qa="vacancy-response-letter-submit"]')
            submit_button.click()
            print("Отклик отправлен после скролла вниз.")
            return
        except:
            pass

        # Третий сценарий: переход на другую страницу
        print("Пропускаем вакансию. Требуется дополнительный ввод.")

    except Exception as e:
        print(f"Пропускаем вакансию из-за ошибки или отклик на вакансию уже был отправлен: {e}")

def main():
    url = input("Введите ссылку с фильтрами: ")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    login_button_element = find_element(driver, By.XPATH, '//a[@data-qa="login"]')

    if login_button_element:
        login_button_element.click()
        auth(driver, username, password)

    links = get_links(driver)

    for link in links:
        apply_to_job(driver, link)

    driver.quit()

if __name__ == '__main__':
    try:
        main()

        input("Нажмите Enter чтоб закрыть")
    except KeyboardInterrupt:
        pass

# /applicant/vacancy_response?vacancyId=108619916&employerId=561525&hhtmFrom=vacancy_search_list
# /applicant/vacancy_response?vacancyId=108449101&employerId=205152&hhtmFrom=vacancy_search_list
# /applicant/vacancy_response?vacancyId=109230802&employerId=6147000&hhtmFrom=vacancy_search_list
# /applicant/vacancy_response?vacancyId=110425206&employerId=2795591&hhtmFrom=vacancy_search_list

# data-qa="vacancy-serp__vacancy_response"
# https://hh.ru/search/vacancy?text=фронтенд+разработчик&salary=15000&ored_clusters=true&only_with_salary=true&area=1&page=0&searchSessionId=4931e3c7-0041-443f-bac3-c062649becaa
# 79960492309
# Nasasal00

# data-qa="vacancy-response-popup-form-letter-input"