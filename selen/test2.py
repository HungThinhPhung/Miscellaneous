import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
chrome_options = Options()
# chrome_options.add_argument("--headless")
url = 'https://support.na.sage.com/selfservice/viewdocument.do?noCount=true&externalId=60390&sliceId=1&noCount=true&isLoadPublishedVer=&docType=kc&docTypeID=DT_Article&stateId=4183&cmd=displayKC&dialogID=197243&ViewedDocsListHelper=com.kanisa.apps.common.BaseViewedDocsListHelperImpl&openedFromSearchResults=true'
chromedriver = '/home/misa/PycharmProjects/test_only/selen/chromedriver'
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
driver.get(url)
print()