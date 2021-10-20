import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_argument("--headless")

chromedriver = '/home/misa/PycharmProjects/test_only/selen/chromedriver'


def crawl(tax_code):
    start_time = time.time()
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
    print('Xử lý 0 trong: ' + str(time.time() - start_time))
    driver.get("https://dangkyquamang.dkkd.gov.vn/inf/default.aspx")
    print('Xử lý 1 trong: ' + str(time.time() - start_time))
    input_box = driver.find_element_by_css_selector('#ctl00_FldSearch')

    input_box.send_keys(tax_code)
    auto_complete = driver.find_element_by_css_selector('body > ul')
    time.sleep(0.5)
    results = auto_complete.find_elements_by_tag_name('li')
    found = False
    if not results:
        input_box.send_keys(Keys.RETURN)
        table = driver.find_element_by_css_selector('#ctl00_C_UC_ENT_LIST1_CtlList')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            if not cells:
                continue
            if not cells[1].text == tax_code:
                continue
            cells[0].click()
            found = True
            break
    else:
        for result in results:
            a = result.find_element_by_css_selector('a')
            span = a.find_element_by_css_selector('span')
            text = span.get_attribute('innerHTML').split(';')[0].split(':')[-1].strip()
            if text == tax_code:
                found = True
                a.click()
                break
    if found:
        print('Xử lý 2 trong: ' + str(time.time() - start_time))
        name = driver.find_element_by_css_selector('#ctl00_C_NAMEFld').text or ''
        eng_name = driver.find_element_by_css_selector('#ctl00_C_NAME_FFld').text or ''
        short_name = driver.find_element_by_css_selector('#ctl00_C_SHORT_NAMEFld').text or ''
        active_status = driver.find_element_by_css_selector('#ctl00_C_STATUSNAMEFld').text or ''
        enterprise_type = driver.find_element_by_css_selector('#ctl00_C_ENTERPRISE_TYPEFld').text or ''
        founding_date = driver.find_element_by_css_selector('#ctl00_C_FOUNDING_DATE').text or ''
        owner = driver.find_element_by_css_selector('#ctl00_C_Tab1 > div:nth-child(8) > p:nth-child(1) > span.viewInput.viewSearch').text or ''
        address = driver.find_element_by_css_selector('#ctl00_C_HO_ADDRESS').text or ''
        print('Xử lý 3 trong: ' + str(time.time() - start_time))

        print('Mã số thuế: ' + tax_code)
        print('Tên doanh nghiệp: ' + name)
        print('Tên doanh nghiệp viết bằng tiếng nước ngoài: ' + eng_name)
        print('Tên doanh nghiệp viết tắt: ' + short_name)
        print('Tình trạng hoạt động: ' + active_status)
        print('Loại hình pháp lý: ' + enterprise_type)
        print('Ngày bắt đầu thành lập: ' + founding_date)
        print('Tên người đại diện theo pháp luật: ' + owner)
        print('Địa chỉ trụ sở chính: ' + address)
        print('###################################')
        print('Xử lý 4 trong: ' + str(time.time() - start_time))
        driver.close()


if __name__ == '__main__':
    tax_codes = ['0101243150', '0108623786', '0108627822', '0108628209', '0108618930']
    for code in tax_codes:
        crawl(code)