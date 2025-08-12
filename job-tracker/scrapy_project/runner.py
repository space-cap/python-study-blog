from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.spiders.saramin_spider import SaraminSpider

def run_spider():
    """Scrapy 스파이더를 실행하는 함수"""
    settings = get_project_settings()
    settings.setmodule('scrapy_project.settings')
    
    process = CrawlerProcess(settings)
    process.crawl(SaraminSpider)
    process.start()