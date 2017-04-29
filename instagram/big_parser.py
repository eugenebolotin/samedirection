# -*- coding: utf-8 -*-
from selenium import webdriver
from models import City
import time
import requests
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
chromedriver_path = '/Users/sp41mer/PycharmProjects/parcer/chromedriver'
ghostdriver_path = '/Users/sp41mer/HiGuys/imaged_cluster/instagram/phantomjs'
for city in City.select().where(City.id>11):
    print('Parsing city {} with ID = {}'.format(city.city,city.id))
    driver_for_page = webdriver.Chrome(chromedriver_path)
    # driver_for_page = webdriver.PhantomJS(ghostdriver_path)
    url = city.ig_link
    name_of_town = url.split('.com/')[1].split('/')[0]
    driver_for_page.get(url)
    driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    try:
        button_more = driver_for_page.find_element_by_css_selector('a._oidfu')
    except:
        print 'Couldnt find a._oidfu'
        button_more = None
        try:
            button_more = driver_for_page.find_element_by_xpath(u"//*[contains(text(), 'Загрузить еще')]")
        except:
            print 'Couldnt find by russian text'
            try:
                button_more = driver_for_page.find_element_by_xpath(u"//*[contains(text(), 'Load more')]")
            except:
                print 'Couldnt find by english text'
    if button_more:
        button_more.click()
        now_len = 0
        for i in range(0, 80):
            driver_for_page.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
            time.sleep(0.2)
            driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(0.2)
            driver_for_page.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
            time.sleep(0.2)
            driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(0.2)
            driver_for_page.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
            time.sleep(0.2)
            driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(0.2)
            rows_of_photos = driver_for_page.find_elements_by_css_selector('div._myci9')
            if (i*1.1-3) > 0: print('{} % done...'.format(i/2-3))
        rows_of_photos = driver_for_page.find_elements_by_css_selector('div._myci9')
        number = 0
        list_of_urls = []
        for row in rows_of_photos:
            if number > 1000:
                break
            else:
                photos = row.find_elements_by_css_selector('img._icyx7')
                for photo in photos:
                    list_of_urls.append(photo.get_attribute("src"))
                    number += 1
        with open('photos_all_json/{}.json'.format(city.city), 'w') as outfile:
            json.dump(list_of_urls, outfile, indent=4, sort_keys=True, separators=(',', ':'))

    driver_for_page.quit()
