# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import json
#
#
# with open('codes_Rus_RZD.json', 'w', encoding='utf-8') as file_RZD:
#     with open(os.path.join('codes_Russian_Railroads.json'), 'r', encoding='utf-8') as file_RZD_read:
#         dict_RZD = json.load(file_RZD_read)
#         count = 0
#         codes = {}
#         data_dict = {}
#         codes['data'] = [data_dict]
#         for i_dict in dict_RZD['data'][0]:
#             try:
#                 count += 1
#                 print(count)
#                 option = webdriver.FirefoxOptions()
#                 option.add_argument("--headless")
#                 browser = webdriver.Firefox(options=option)
#                 browser.get('http://osm.sbin.ru/esr/railways')
#                 element = browser.find_element(By.XPATH, '/html/body/form/input[1]')
#                 element.send_keys(dict_RZD['data'][0][i_dict])
#                 click = browser.find_element(By.XPATH, '/html/body/form/input[2]')
#                 click.click()
#                 result = browser.find_element(By.XPATH, '/html/body/table/tbody')
#                 res_list = result.text.split('\n')
#                 for i in res_list:
#                     if i.startswith('Название (Яндекс.Расписания):'):
#                         data_dict[i[32:]] = dict_RZD['data'][0][i_dict]
#                 browser.quit()
#             except:
#                 browser.quit()
#         json.dump(codes, file_RZD, ensure_ascii=False, indent=4)
# !!!!!!!!!!!!!!!!! Данный парсер больше не используется, так как он был нужен чтобы создать json файл, с именами станций "Яндекс.расписания" и с кодами станций "Экспресс-3"!!!!!!!!!!!!!!!!!!