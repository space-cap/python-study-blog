"""스파이더를 직접 실행해서 크롤링이 작동하는지 테스트"""

from scrapy_project.runner import run_spider
import time

print("크롤링 시작...")
run_spider()
print("크롤링 요청 완료. 잠시 대기 중...")

# 크롤링이 완료될 시간을 기다림
time.sleep(10)
print("대기 완료.")