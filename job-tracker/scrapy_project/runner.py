import asyncio
import threading
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy_project.spiders.saramin_spider import SaraminSpider
from twisted.internet import reactor

def run_spider():
    """FastAPI와 호환되는 방식으로 Scrapy 스파이더를 실행하는 함수"""
    def _run_spider():
        """별도 스레드에서 스파이더를 실행"""
        try:
            settings = get_project_settings()
            settings.setmodule('scrapy_project.settings')
            
            runner = CrawlerRunner(settings)
            deferred = runner.crawl(SaraminSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run(installSignalHandlers=False)
        except Exception as e:
            print(f"크롤링 실행 중 오류: {e}")
    
    # 별도 스레드에서 크롤링 실행
    spider_thread = threading.Thread(target=_run_spider)
    spider_thread.daemon = True
    spider_thread.start()