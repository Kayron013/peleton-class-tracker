from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import pprint
import os

PELETON_SCHEDULE_URL = 'https://studio.onepeloton.com/new-york/schedule'

pp = pprint.PrettyPrinter(indent=4)


def main(event, context):
    # ^- lambda arguments

    driver = get_web_driver()

    driver.get(PELETON_SCHEDULE_URL)
    print(driver.title)

    class_elements: list[WebElement] = WebDriverWait(driver=driver, timeout=10).until(lambda driver: driver.find_elements(By.CSS_SELECTOR, '[data-test-class=classCards]'))

    first_date = get_class_details(class_elements[0])['date']
    last_date = get_class_details(class_elements[-1])['date']
    print('{} classes from {} to {}'.format(len(class_elements), first_date, last_date))

    # mapping the elements to dicts takes some time, so filtering on the entire text content
    filtered_class_cards = list(filter(lambda x: 'CLASS FULL' not in x.text, class_elements))
    classes = [get_class_details(card) for card in filtered_class_cards]

    print('{} reservable classes'.format(len(classes)))
    pp.pprint(classes)


def get_web_driver():
    runtime_env = os.environ.get('RUNTIME_ENV')
    options = webdriver.ChromeOptions()

    if runtime_env == 'lambda':
        print('getting driver for lambda')
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')

        service = Service('/opt/chromedriver')
        return webdriver.Chrome(service=service, options=options)

    else:
        print('getting driver for local')
        options.binary_location = 'lib/chromedriver/headless-chromium'
        options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--single-process')
        # options.add_argument('--disable-dev-shm-usage')

        s=Service('lib/chromedriver/chromedriver')
        return webdriver.Chrome(service=s, options=options, desired_capabilities={"platform": "LINUX"})

        # return webdriver.Chrome('lib/chromedriver/chromedriver', options=options, desired_capabilities={'browserName': 'chrome', 'browserVersion': '62.0'})

    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=options)


def get_class_details(class_element: WebElement):
    status = class_element.find_element(By.CSS_SELECTOR, ':nth-child(4)').text
    is_reservable = status != 'CLASS FULL'

    return {
        'name': class_element.find_element(By.CSS_SELECTOR, '[data-test-id=className]').text,
        'instructor': {
            'name': class_element.find_element(By.CSS_SELECTOR, '[aria-label=Instructor]').text,
            'image': class_element.find_element(By.TAG_NAME, 'img').get_attribute('src')
        },
        'fitness_disciplines': class_element.find_element(By.CSS_SELECTOR, '[aria-label="Fitness Disciplines"]').get_attribute('data-test-info').split(','),
        'status': status,
        'time': class_element.find_element(By.CSS_SELECTOR, ':first-child').text,
        # need xpath to get to parent elements
        # class card becomes an <a/> nested in a <li/> when it's reservable, instead of just being the <li/>
        'date': class_element.find_element(By.XPATH, '../../../*[1]' if is_reservable else '../../*[1]').text,
        'reserve_link': class_element.get_attribute('href') if is_reservable else None
    }


if __name__ == '__main__':
    main(None, None)
