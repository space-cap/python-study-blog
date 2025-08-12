import scrapy
from datetime import datetime
from scrapy_project.items import JobPostingItem

class SaraminSpider(scrapy.Spider):
    name = 'saramin'
    allowed_domains = ['saramin.co.kr']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }
    
    def start_requests(self):
        # 목표 URL 및 추가 검색 URL들
        urls = [
            'https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=51507890&view_type=search',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=개발자',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프로그래머',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=백엔드',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프론트엔드',
        ]
        
        # 첫 번째 URL은 직접 상세 페이지로 처리
        yield scrapy.Request(url=urls[0], callback=self.parse_job_detail)
        
        # 나머지는 검색 결과 페이지로 처리
        for url in urls[1:]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 채용공고 목록에서 개별 공고 링크 추출
        job_links = response.css('.item_recruit .job_tit a::attr(href)').getall()
        
        for link in job_links[:10]:  # 테스트용으로 10개만 수집
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_job_detail)

    def parse_job_detail(self, response):
        item = JobPostingItem()
        
        # 기업명
        item['company_name'] = response.css('.company_nm a::text').get() or response.css('.company_nm::text').get()
        
        # 채용제목  
        item['job_title'] = response.css('.job_tit .job_title::text').get()
        
        # 시작일 (수집일)
        item['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # 마감일 추출
        end_date_text = response.css('.recruitment_summary .date::text').get()
        if end_date_text:
            item['end_date'] = end_date_text.strip()
        
        # 지원자수 (있는 경우)
        applicant_text = response.css('.apply_info .apply_total::text').get()
        if applicant_text:
            try:
                item['applicant_count'] = int(''.join(filter(str.isdigit, applicant_text)))
            except:
                item['applicant_count'] = 0
        else:
            item['applicant_count'] = 0
        
        # 자격요건
        requirements_elements = response.css('.job_requirements .qualification ul li::text').getall()
        item['requirements'] = ' | '.join(requirements_elements) if requirements_elements else ''
        
        # 우대사항
        preferred_elements = response.css('.job_requirements .preferential ul li::text').getall()
        item['preferred_qualifications'] = ' | '.join(preferred_elements) if preferred_elements else ''
        
        # 근무지역
        location = response.css('.recruitment_summary .work_place::text').get()
        item['location'] = location.strip() if location else ''
        
        # 현재 URL
        item['source_url'] = response.url
        
        yield item