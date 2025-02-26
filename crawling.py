from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# Chrome Options 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691')

# ActionChains 초기화
act = ActionChains(driver)
lst = []  # 오디오 파일 URL 저장

# 페이지 순회 
for page_num in range(1, 24):
    try:
        # 각 페이지로 이동
        if page_num > 1:
            # 페이지 번호가 1보다 크면, 해당 페이지로 직접 이동
            page_url = f'https://www.fss.or.kr/fss/bbs/B0000207/list.do?menuNo=200691&pageIndex={page_num}'
            driver.get(page_url)
        
        # 현재 페이지 게시물 순회
        for i in range(1, 11):  # 최대 10개
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'#content > div.bd-list > table > tbody > tr:nth-child({i}) > td.title > a'))
                )
                act.click(element).perform()
                target_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div.bd-view > div > video'))
                )
                audio_url = target_element.get_attribute("src")
                lst.append(audio_url)  # URL 저장
                driver.back()  # 다시 목록 페이지로 돌아가기
            except Exception as e:
                print(f"Error for row {i}: {e}")

    except Exception as e:
        print(f"Error navigating to page {page_num}: {e}")

# 오디오 파일 다운로드
if not os.path.exists('downloads'):  # 다운로드 폴더 생성
    os.makedirs('downloads')

for idx, url in enumerate(lst, start=1):  # 리스트에 저장된 URL 순회
    try:
        response = requests.get(url)
        with open(f'C:/Users/DS/Desktop/22883/voicefishing/dataset/voice/fishing/imperson/aud_{idx}.mp3', 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# WebDriver 종료
driver.quit()
