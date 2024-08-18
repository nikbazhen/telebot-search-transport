from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from log import logger


def parser_train(from_RZD: str, to_RZD: str, date: str, from_time: str, to_time: str) -> (bool, str):
    """Функция парсер"""
    logger.log_debug('Запуск функции-парсера parser_train')
    try:
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
        browser.get(f'https://www.tutu.ru/poezda/rasp_d.php?nnst1={from_RZD}&nnst2={to_RZD}&date={date}')
        time.sleep(2)
        tickets = browser.find_elements(By.CLASS_NAME, '_151K-8IAD-lVBcM9v84fje')
        for i in tickets:
            result.append(i.text.split('\n'))
        browser.quit()
        for i in result:
            try:
                i.index(from_time)
                i.index(to_time)
                res = ''.join(x for x in i[i.index('Маршрут') + 5] if x.isdigit())
                return res
            except ValueError:
                pass
    except Exception:
        return False
