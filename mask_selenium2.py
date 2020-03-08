from selenium import webdriver
import winsound
from time import sleep
from datetime import datetime


delay = 10

def log(*args):
    print(datetime.now().strftime('%H:%M:%S'), *args)


def file_log(to_write):
    with open(logPath, 'a') as f:
        f.write(datetime.now().strftime('%m월 %d일 %H:%M:%S') + '\n' + to_write + '\n\n')


driverPath = 'C:/Users/LEE/Scripts/Python/Projects/YoutubeDownloader/chromedriver_win32/chromedriver.exe'
baseURL = 'http://www.welkeepsmall.com/shop/shopbrandCA.html?type=X&xcode=023'
logPath = 'C:/Users/LEE/Desktop/입고기록.txt'


c_op = webdriver.ChromeOptions()
#c_op.add_argument('headless')
#c_op.add_argument('--disable-gpu')
#c_op.add_argument('lang=ko_KR')

driver = webdriver.Chrome(driverPath, chrome_options=c_op)
driver.get(baseURL)
driver.implicitly_wait(1)

print(' ')

for i in range(100000):
    sold = True
    log('-----', i + 1, '번째 시도 -------')
    driver.implicitly_wait(1)
    try:
        t = driver.find_elements_by_class_name('info')
    except:
        print('403 forbidden (서버 오류)')
        continue
    log('페이지 정보 가져오기...')
    for e in t:
        try:
            p = e.find_element_by_class_name('soldout')
            if p.text.rstrip() != 'SOLD OUT':
                winsound.Beep(440, 1000)
        except:
            try:
                if e.find_element_by_class_name('dsc').text.find('소') != -1:
                    beep = True
                print(' ')
                print('\n', e.find_element_by_class_name('dsc').text)
                log('재입고됨!!!!\n')
                file_log(e.find_element_by_class_name('dsc').text)
            except:
                pass
            if beep:
                beep = False
                winsound.Beep(660, 1000)
                sleep(1)
                winsound.Beep(660, 1000)
                sleep(1)
                winsound.Beep(660, 1000)
            sold = False
    if sold:
        log(len(t), '개 품목 전체 품절')
    log('새로고침까지', delay, '초 기다리기...\n')
    sleep(delay)
    driver.refresh()
    driver.implicitly_wait(1)


winsound.Beep(440, 5000)
