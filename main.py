from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

PELETON_SCHEDULE_URL = 'https://studio.onepeloton.com/new-york/schedule'


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(PELETON_SCHEDULE_URL)
    driver.implicitly_wait(1)

    title = driver.title
    class_cards = driver.find_elements(
        By.CSS_SELECTOR, '[data-test-class=classCards]')
    print(title)
    print(get_card_details(class_cards[0]))


def get_card_details(class_card: WebElement):
    return {
        'name': class_card.find_element(By.CSS_SELECTOR, '[data-test-id=className]').text,
        'instructor': {
            'name': class_card.find_element(By.CSS_SELECTOR, '[aria-label=Instructor]').text,
            'image': class_card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        },
        'fitness_disciplines': class_card.find_element(By.CSS_SELECTOR, '[aria-label="Fitness Disciplines"]').get_attribute('data-test-info').split(','),
        'status': class_card.find_element(By.CSS_SELECTOR, ':nth-child(4)').text,
        'time': class_card.find_element(By.CSS_SELECTOR, ':first-child').text,
        'date': class_card.find_element(By.XPATH, '../../*[1]').text
    }


main()
