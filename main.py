from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import pprint

PELETON_SCHEDULE_URL = 'https://studio.onepeloton.com/new-york/schedule'

pp = pprint.PrettyPrinter(indent=4)


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(PELETON_SCHEDULE_URL)

    title = driver.title
    print(title)

    class_cards: list[WebElement] = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[data-test-class=classCards]'))

    (first_class, last_class) = (get_card_details(class_cards[0]), get_card_details(class_cards[-1]))
    print('{} classes from {} to {}'.format(len(class_cards), first_class['date'], last_class['date']))

    # mapping the elements to dicts takes some time, so filtering on the entire text content
    filtered_class_cards = list(filter(lambda x: 'CLASS FULL' not in x.text, class_cards))
    classes = [get_card_details(card) for card in filtered_class_cards]

    print('{} reservable classes'.format(len(classes)))
    pp.pprint(classes)


def get_card_details(class_card: WebElement):
    status = class_card.find_element(By.CSS_SELECTOR, ':nth-child(4)').text
    is_reservable = status != 'CLASS FULL'

    return {
        'name': class_card.find_element(By.CSS_SELECTOR, '[data-test-id=className]').text,
        'instructor': {
            'name': class_card.find_element(By.CSS_SELECTOR, '[aria-label=Instructor]').text,
            'image': class_card.find_element(By.TAG_NAME, 'img').get_attribute('src')
        },
        'fitness_disciplines': class_card.find_element(By.CSS_SELECTOR, '[aria-label="Fitness Disciplines"]').get_attribute('data-test-info').split(','),
        'status': status,
        'time': class_card.find_element(By.CSS_SELECTOR, ':first-child').text,
        # need xpath to get to parent elements
        # class card becomes an <a/> nested in a <li/> when it's reservable, instead of just being the <li/>
        'date': class_card.find_element(By.XPATH, '../../../*[1]' if is_reservable else '../../*[1]').text,
        'reserve_link': class_card.get_attribute('href') if is_reservable else None
    }


main()
