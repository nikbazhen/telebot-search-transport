from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from log import logger


def parser_avia(from_IATA: str, to_IATA: str, date: str, from_time: str, to_time: str) -> (bool, str):
    """Функция парсер"""
    logger.log_debug('Запуск функции-парсера parser_avia')
    user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/121.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/120.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/120.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/119.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/118.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/117.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/117.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/116.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/116.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
                               'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 6.3; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/115.0',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
                               ]
    result = []

    option = webdriver.FirefoxOptions()
    option.set_preference('dom.webdriver.enabled', False)
    option.set_preference('dom.webnotifications.enabled', False)
    option.set_preference('media.volume_scale', '0.0')
    option.set_preference('general.useragent.override', random.choice(user_agent_list))
    option.add_argument("--headless")

    browser = webdriver.Firefox(options=option)
    browser.get(f"https://рейсы.госбилет.рф/flights/{from_IATA}{date}{to_IATA}1")
    time.sleep(1)
    block_button = browser.find_elements(By.CSS_SELECTOR, 'label.label-block')
    block_button[2].click()
    block_button[3].click()
    time.sleep(2)
    block_tickets_information = browser.find_elements(By.CSS_SELECTOR, 'div.ticket')
    for i in block_tickets_information:
        result.append(i.text.split('\n'))
    browser.quit()
    for i in result:
        try:
            i.index('Купить')
            i.index(from_time)
            if i[-2][4:] == to_time:
                res = ''.join(x for x in i[i.index('Купить') + 1] if x.isdigit())
                return res
        except ValueError:
            pass
    else:
        return False
