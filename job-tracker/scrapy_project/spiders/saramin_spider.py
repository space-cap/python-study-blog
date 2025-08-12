"""Saramin(사람인) 웹사이트 채용공고 크롤링 스파이더.

사람인 웹사이트에서 채용공고 정보를 크롤링하여 데이터베이스에 저장하는
Scrapy 스파이더입니다.

주요 기능:
- 사람인 검색 결과 페이지 크롤링
- 개별 채용공고 상세 정보 추출
- 지연 설정으로 서버 부하 최소화
"""

import scrapy
from datetime import datetime
from scrapy_project.items import JobPostingItem

class SaraminSpider(scrapy.Spider):
    """사람인 채용공고 크롤링 스파이더.
    
    사람인 웹사이트에서 개발자 관련 채용공고를 크롤링합니다.
    서버 부하를 최소화하기 위해 단일 요청 및 지연 설정을 사용합니다.
    
    Attributes:
        name (str): 스파이더 이름
        allowed_domains (list): 허용된 도메인 목록
        custom_settings (dict): 스파이더 전용 설정
    """
    name = 'saramin'
    allowed_domains = ['saramin.co.kr']
    
    # 서버 부하 최소화를 위한 설정
    custom_settings = {
        'DOWNLOAD_DELAY': 2,                      # 요청 간 2초 지연
        'CONCURRENT_REQUESTS': 1,                 # 동시 요청 수 제한
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,      # 도메인별 동시 요청 수 제한
    }
    
    def start_requests(self):
        """초기 요청 URL들을 생성합니다.
        
        대상 URL들을 두 종류로 분류하여 처리합니다:
        1. 직접 상세 페이지
        2. 검색 결과 페이지 (개발자 관련 키워드)
        
        Yields:
            scrapy.Request: 각 URL에 대한 Scrapy 요청 객체
        """
        # 크롤링 대상 URL 목록
        urls = [
            # 직접 상세 페이지 URL
            'https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=51507890&view_type=search',
            # 개발자 관련 검색 URL들
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=개발자',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프로그래머',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=백엔드',
            'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프론트엔드',
        ]
        
        # 첫 번째 URL은 상세 페이지이므로 직접 parse_job_detail로 전달
        yield scrapy.Request(url=urls[0], callback=self.parse_job_detail)
        
        # 나머지 URL들은 검색 결과 페이지이므로 parse로 전달
        for url in urls[1:]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """검색 결과 페이지에서 개별 채용공고 링크를 추출합니다.
        
        검색 결과 페이지에서 채용공고 목록을 찾고,
        각 공고의 상세 페이지 URL을 추출하여 상세 정보를 수집합니다.
        
        Args:
            response (scrapy.http.Response): 검색 결과 페이지 응답
            
        Yields:
            scrapy.Request: 각 채용공고 상세 페이지에 대한 요청
        """
        # CSS 셀렉터로 채용공고 목록에서 링크 추출
        job_links = response.css('.item_recruit .job_tit a::attr(href)').getall()
        
        # 테스트 및 서버 부하 고려로 10개만 수집
        for link in job_links[:10]:
            # 상대 URL을 절대 URL로 변환
            full_url = response.urljoin(link)
            # 상세 페이지 크롤링 요청 생성
            yield scrapy.Request(url=full_url, callback=self.parse_job_detail)

    def parse_job_detail(self, response):
        """채용공고 상세 페이지에서 정보를 추출합니다.
        
        개별 채용공고 상세 페이지에서 필요한 정보를 CSS 셀렉터로 추출하고
JobPostingItem 객체로 구성하여 반환합니다.
        
        Args:
            response (scrapy.http.Response): 채용공고 상세 페이지 응답
            
        Yields:
            JobPostingItem: 추출된 채용공고 정보가 담긴 아이템
        """
        item = JobPostingItem()
        
        # 기업명 추출 (링크가 있는 경우와 없는 경우 모두 처리)
        item['company_name'] = (
            response.css('.company_nm a::text').get() or 
            response.css('.company_nm::text').get()
        )
        
        # 채용공고 제목 추출
        item['job_title'] = response.css('.job_tit .job_title::text').get()
        
        # 수집일을 시작일로 설정 (현재 날짜)
        item['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # 마감일 추출 및 정리
        end_date_text = response.css('.recruitment_summary .date::text').get()
        if end_date_text:
            item['end_date'] = end_date_text.strip()
        
        # 지원자 수 추출 (숫자만 추출하여 정수로 변환)
        applicant_text = response.css('.apply_info .apply_total::text').get()
        if applicant_text:
            try:
                # 텍스트에서 숫자만 추출하여 정수로 변환
                item['applicant_count'] = int(''.join(filter(str.isdigit, applicant_text)))
            except ValueError:
                item['applicant_count'] = 0
        else:
            item['applicant_count'] = 0
        
        # 자격요건 목록 추출 및 문자열로 결합
        requirements_elements = response.css('.job_requirements .qualification ul li::text').getall()
        item['requirements'] = ' | '.join(requirements_elements) if requirements_elements else ''
        
        # 우대사항 목록 추출 및 문자열로 결합
        preferred_elements = response.css('.job_requirements .preferential ul li::text').getall()
        item['preferred_qualifications'] = ' | '.join(preferred_elements) if preferred_elements else ''
        
        # 근무지역 추출 및 공백 제거
        location = response.css('.recruitment_summary .work_place::text').get()
        item['location'] = location.strip() if location else ''
        
        # 현재 페이지 URL을 소스 URL로 설정
        item['source_url'] = response.url
        
        # 추출된 아이템 반환
        yield item