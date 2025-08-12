"""간단한 스파이더 테스트 - 로그 확인용"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.spiders.saramin_spider import SaraminSpider
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    settings = get_project_settings()
    settings.setmodule('scrapy_project.settings')
    
    # 로그 레벨을 INFO로 설정
    settings.set('LOG_LEVEL', 'INFO')
    
    process = CrawlerProcess(settings)
    process.crawl(SaraminSpider)
    
    logger.info("크롤링 프로세스 시작")
    process.start()
    logger.info("크롤링 프로세스 종료")
    
except Exception as e:
    logger.error(f"크롤링 중 오류 발생: {e}")
    import traceback
    traceback.print_exc()