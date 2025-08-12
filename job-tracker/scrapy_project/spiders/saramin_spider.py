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
        target_url (str): 사용자가 입력한 크롤링 대상 URL
    """
    name = 'saramin'
    allowed_domains = ['saramin.co.kr']
    
    # 서버 부하 최소화를 위한 설정
    custom_settings = {
        'DOWNLOAD_DELAY': 2,                      # 요청 간 2초 지연
        'CONCURRENT_REQUESTS': 1,                 # 동시 요청 수 제한
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,      # 도메인별 동시 요청 수 제한
    }
    
    def __init__(self, target_url=None, *args, **kwargs):
        """스파이더 초기화
        
        Args:
            target_url (str, optional): 사용자가 입력한 크롤링 대상 URL
        """
        super(SaraminSpider, self).__init__(*args, **kwargs)
        self.target_url = target_url
    
    def start_requests(self):
        """초기 요청 URL들을 생성합니다.
        
        사용자가 입력한 URL이 있으면 해당 URL을 우선적으로 사용하고,
        없으면 기본 URL들을 사용합니다.
        
        Yields:
            scrapy.Request: 각 URL에 대한 Scrapy 요청 객체
        """
        # 사용자가 입력한 URL이 있는 경우 해당 URL 사용
        if self.target_url:
            self.logger.info(f"사용자 입력 URL로 크롤링 시작: {self.target_url}")
            # URL 종류에 따라 적절한 콜백 함수 선택
            if '/jobs/relay/view' in self.target_url or 'rec_idx=' in self.target_url:
                # 채용공고 상세 페이지
                yield scrapy.Request(url=self.target_url, callback=self.parse_job_detail)
            else:
                # 검색 결과 페이지
                yield scrapy.Request(url=self.target_url, callback=self.parse)
        else:
            # 기본 크롤링 대상 URL 목록
            urls = [
                # 직접 상세 페이지 URL
                'https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=51507890&view_type=search',
                # 개발자 관련 검색 URL들
                'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=개발자',
                'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프로그래머',
                'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=백엔드',
                'https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=프론트엔드',
            ]
            
            self.logger.info("기본 URL들로 크롤링 시작")
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
        
        개별 채용공고 상세 페이지에서 필요한 정보를 JSON 데이터와 CSS 셀렉터를 
        조합하여 추출하고 JobPostingItem 객체로 구성하여 반환합니다.
        
        Args:
            response (scrapy.http.Response): 채용공고 상세 페이지 응답
            
        Yields:
            JobPostingItem: 추출된 채용공고 정보가 담긴 아이템
        """
        import re
        import json
        
        item = JobPostingItem()
        
        # JSON 데이터에서 정보 추출 시도
        company_name = None
        job_title = None
        
        # 페이지 내 JSON 데이터에서 회사명과 제목 추출
        company_pattern = r'"company_nm":\s*"([^"]+)"'
        company_match = re.search(company_pattern, response.text)
        if company_match:
            # 유니코드 이스케이프 디코딩
            company_name = company_match.group(1).encode().decode('unicode_escape')
        
        title_pattern = r'"title":\s*"([^"]+)"'
        title_matches = re.findall(title_pattern, response.text)
        if title_matches:
            # 첫 번째 제목 사용 (보통 채용공고 제목)
            job_title = title_matches[0].encode().decode('unicode_escape')
        
        # JSON에서 추출 실패 시 CSS 셀렉터 대체 방법 사용
        if not company_name:
            company_name = (
                response.css('.company_nm a::text').get() or 
                response.css('.company_nm::text').get() or
                response.css('h1::text').get()
            )
        
        if not job_title:
            job_title = (
                response.css('.job_tit .job_title::text').get() or
                response.css('meta[property="og:title"]::attr(content)').get()
            )
        
        # 메타 태그에서 OG 제목 추출 (최후 수단)
        if not job_title:
            og_title = response.css('meta[property="og:title"]::attr(content)').get()
            if og_title and og_title != '사람인':
                job_title = og_title
        
        item['company_name'] = company_name
        item['job_title'] = job_title
        
        # 수집일을 시작일로 설정 (현재 날짜)
        item['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # 마감일 추출 및 정리 - 여러 방법 시도
        end_date_text = (
            response.css('.recruitment_summary .date::text').get() or
            response.css('.date::text').get() or
            response.css('[class*="date"]::text').get()
        )
        if end_date_text:
            item['end_date'] = end_date_text.strip()
        else:
            # JSON에서 마감일 추출 시도 
            closing_date_pattern = r'"closing_date":\s*"([^"]+)"'
            closing_match = re.search(closing_date_pattern, response.text)
            if closing_match:
                closing_date = closing_match.group(1)
                # 20250902 형태를 2025-09-02로 변환
                if len(closing_date) == 8 and closing_date.isdigit():
                    year = closing_date[:4]
                    month = closing_date[4:6]
                    day = closing_date[6:8]
                    item['end_date'] = f"{year}-{month}-{day}"
                else:
                    item['end_date'] = closing_date
            else:
                # 제목에서 D-xx 형태 추출
                d_pattern = r'D-(\d+)'
                d_match = re.search(d_pattern, job_title or '')
                if d_match:
                    item['end_date'] = f"D-{d_match.group(1)}"
        
        # 지원자 수 추출 - 여러 방법 시도
        applicant_text = (
            response.css('.apply_info .apply_total::text').get() or
            response.css('[class*="apply"]::text').get()
        )
        if applicant_text:
            try:
                item['applicant_count'] = int(''.join(filter(str.isdigit, applicant_text)))
            except ValueError:
                item['applicant_count'] = 0
        else:
            item['applicant_count'] = 0
        
        # 자격요건 추출 - 여러 방법 시도
        requirements_elements = (
            response.css('.job_requirements .qualification ul li::text').getall() or
            response.css('[class*="requirement"] li::text').getall() or
            response.css('[class*="qualification"] li::text').getall()
        )
        item['requirements'] = ' | '.join(requirements_elements) if requirements_elements else ''
        
        # 우대사항 추출 - 여러 방법 시도
        preferred_elements = (
            response.css('.job_requirements .preferential ul li::text').getall() or
            response.css('[class*="preferential"] li::text').getall() or
            response.css('[class*="preferred"] li::text').getall()
        )
        item['preferred_qualifications'] = ' | '.join(preferred_elements) if preferred_elements else ''
        
        # 근무지역 추출 - 여러 방법 시도
        location = (
            response.css('.recruitment_summary .work_place::text').get() or
            response.css('[class*="location"]::text').get() or
            response.css('[class*="work_place"]::text').get()
        )
        if location:
            item['location'] = location.strip()
        else:
            # JSON에서 주소 정보 추출 시도
            address_patterns = [
                r'"contact_address":\s*"([^"]+)"',
                r'"mcom_address":\s*"([^"]+)"', 
                r'"location":\s*"([^"]+)"'
            ]
            
            for pattern in address_patterns:
                location_match = re.search(pattern, response.text)
                if location_match:
                    try:
                        address = location_match.group(1).encode().decode('unicode_escape')
                        # 주소에서 지역명만 추출 (서울, 부산 등)
                        if address:
                            # 서울특별시 -> 서울, 부산광역시 -> 부산 등
                            location_simplified = address.split()[0].replace('특별시', '').replace('광역시', '').replace('시', '').replace('도', '')
                            item['location'] = location_simplified
                            break
                    except:
                        continue
        
        # 현재 페이지 URL을 소스 URL로 설정
        item['source_url'] = response.url
        
        # 디버그 정보 출력
        self.logger.info(f"추출된 정보 - 회사: {item['company_name']}, 제목: {item['job_title']}")
        
        # 필수 정보가 있는 경우만 아이템 반환
        if item['company_name'] or item['job_title']:
            yield item
        else:
            self.logger.warning(f"필수 정보 누락으로 아이템 생략: {response.url}")