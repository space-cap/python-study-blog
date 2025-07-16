import json
import os
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, List

from opensearch_manager import YouthPolicyOpenSearchManager
from file_manager import YouthPolicyFileManager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youth_policy_opensearch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouthPolicyProcessor:
    """
    청년정책 데이터를 API에서 가져와 OpenSearch에 저장하는 통합 프로세서
    """
    
    def __init__(self, opensearch_host: str = "localhost", opensearch_port: int = 9200):
        """
        프로세서 초기화
        
        Args:
            opensearch_host: OpenSearch 호스트
            opensearch_port: OpenSearch 포트
        """
        self.opensearch_manager = YouthPolicyOpenSearchManager(opensearch_host, opensearch_port)
        self.file_manager = YouthPolicyFileManager()
        
    def setup_opensearch(self, reset_index: bool = False) -> bool:
        """
        OpenSearch 설정
        
        Args:
            reset_index: 인덱스 재생성 여부
            
        Returns:
            bool: 설정 성공 여부
        """
        try:
            # 인덱스 재생성 옵션
            if reset_index:
                logger.info("기존 인덱스 삭제 중...")
                self.opensearch_manager.opensearch.delete_index(
                    self.opensearch_manager.index_name
                )
            
            # 인덱스 설정
            if not self.opensearch_manager.setup_index():
                logger.error("OpenSearch 설정 실패")
                return False
            
            logger.info("OpenSearch 설정 완료")
            return True
            
        except Exception as e:
            logger.error(f"OpenSearch 설정 중 오류: {e}")
            return False
    
    def fetch_and_index_api_data(self, api_url: str, api_params: Dict[str, Any], 
                                max_pages: int = None) -> bool:
        """
        API에서 데이터를 가져와 OpenSearch에 직접 인덱싱
        
        Args:
            api_url: API URL
            api_params: API 파라미터
            max_pages: 최대 페이지 수
            
        Returns:
            bool: 전체 처리 성공 여부
        """
        try:
            logger.info("API 데이터 가져오기 및 인덱싱 시작")
            
            page_num = 1
            total_policies = 0
            
            while True:
                # 페이지별 파라미터 설정
                params = api_params.copy()
                params['pageNum'] = page_num
                
                logger.info(f"페이지 {page_num} 처리 중...")
                
                # API 데이터 가져오기
                api_data = self.file_manager.fetch_api_data(api_url, params)
                
                if not api_data:
                    logger.error(f"페이지 {page_num} 데이터 가져오기 실패")
                    break
                
                # 현재 페이지 정책 수 확인
                policies = api_data.get('result', {}).get('youthPolicyList', [])
                if not policies:
                    logger.info(f"페이지 {page_num}에 더 이상 데이터가 없음")
                    break
                
                # OpenSearch에 인덱싱
                if self.opensearch_manager.index_api_data(api_data):
                    total_policies += len(policies)
                    logger.info(f"페이지 {page_num} 인덱싱 완료: {len(policies)}건")
                else:
                    logger.error(f"페이지 {page_num} 인덱싱 실패")
                
                # 페이징 정보 확인
                pagging = api_data.get('result', {}).get('pagging', {})
                total_count = pagging.get('totCount', 0)
                page_size = pagging.get('pageSize', 100)
                
                # 마지막 페이지 확인
                if page_num * page_size >= total_count:
                    logger.info("모든 페이지 처리 완료")
                    break
                
                # 최대 페이지 수 확인
                if max_pages and page_num >= max_pages:
                    logger.info(f"최대 페이지 수 도달: {max_pages}")
                    break
                
                page_num += 1
            
            logger.info(f"API 데이터 인덱싱 완료: 총 {total_policies}건")
            return True
            
        except Exception as e:
            logger.error(f"API 데이터 인덱싱 중 오류: {e}")
            return False
    
    def index_file_data(self, file_path: str) -> bool:
        """
        파일에서 데이터를 읽어 OpenSearch에 인덱싱
        
        Args:
            file_path: 데이터 파일 경로
            
        Returns:
            bool: 인덱싱 성공 여부
        """
        try:
            logger.info(f"파일 데이터 인덱싱 시작: {file_path}")
            
            success = self.opensearch_manager.index_file_data(file_path)
            
            if success:
                logger.info(f"파일 데이터 인덱싱 완료: {file_path}")
            else:
                logger.error(f"파일 데이터 인덱싱 실패: {file_path}")
            
            return success
            
        except Exception as e:
            logger.error(f"파일 데이터 인덱싱 중 오류: {e}")
            return False
    
    def index_directory_files(self, directory_path: str) -> bool:
        """
        디렉토리 내 모든 파일을 인덱싱
        
        Args:
            directory_path: 디렉토리 경로
            
        Returns:
            bool: 전체 처리 성공 여부
        """
        try:
            if not os.path.exists(directory_path):
                logger.error(f"디렉토리가 존재하지 않습니다: {directory_path}")
                return False
            
            logger.info(f"디렉토리 파일 인덱싱 시작: {directory_path}")
            
            success_count = 0
            total_count = 0
            
            # 디렉토리 내 파일 처리
            for filename in os.listdir(directory_path):
                if filename.startswith('youthcenter-') and filename.endswith('.txt'):
                    file_path = os.path.join(directory_path, filename)
                    total_count += 1
                    
                    if self.index_file_data(file_path):
                        success_count += 1
                    else:
                        logger.error(f"파일 인덱싱 실패: {filename}")
            
            logger.info(f"디렉토리 파일 인덱싱 완료: {success_count}/{total_count}")
            return success_count == total_count
            
        except Exception as e:
            logger.error(f"디렉토리 파일 인덱싱 중 오류: {e}")
            return False
    
    def search_and_display_results(self, search_type: str, search_value: str, 
                                  size: int = 10) -> List[Dict[str, Any]]:
        """
        검색 실행 및 결과 표시
        
        Args:
            search_type: 검색 타입 (keyword, category, age, region)
            search_value: 검색 값
            size: 결과 개수
            
        Returns:
            List: 검색 결과
        """
        try:
            logger.info(f"검색 실행: {search_type} - {search_value}")
            
            results = []
            
            if search_type == 'keyword':
                results = self.opensearch_manager.search_by_keyword(search_value, size)
            elif search_type == 'category':
                results = self.opensearch_manager.search_by_category(search_value, size)
            elif search_type == 'age':
                # 연령대 형식: "20-30"
                try:
                    min_age, max_age = map(int, search_value.split('-'))
                    results = self.opensearch_manager.search_by_age_range(min_age, max_age, size)
                except ValueError:
                    logger.error("연령대 형식이 올바르지 않습니다. (예: 20-30)")
                    return []
            elif search_type == 'region':
                results = self.opensearch_manager.search_by_region(search_value, size)
            else:
                logger.error(f"지원하지 않는 검색 타입: {search_type}")
                return []
            
            # 결과 표시
            if results:
                logger.info(f"검색 결과: {len(results)}건")
                logger.info("-" * 80)
                
                for i, policy in enumerate(results, 1):
                    logger.info(f"{i:2d}. {policy.get('plcyNm', 'N/A')}")
                    logger.info(f"     분류: {policy.get('lclsfNm', 'N/A')} > {policy.get('mclsfNm', 'N/A')}")
                    logger.info(f"     기관: {policy.get('sprvsnInstCdNm', 'N/A')}")
                    logger.info(f"     연령: {policy.get('sprtTrgtMinAge', 'N/A')}~{policy.get('sprtTrgtMaxAge', 'N/A')}세")
                    logger.info(f"     등록일: {policy.get('frstRegDt', 'N/A')}")
                    logger.info("-" * 80)
            else:
                logger.info("검색 결과가 없습니다.")
            
            return results
            
        except Exception as e:
            logger.error(f"검색 및 결과 표시 중 오류: {e}")
            return []
    
    def show_statistics(self):
        """통계 정보 표시"""
        try:
            logger.info("통계 정보 조회 중...")
            
            stats = self.opensearch_manager.get_policy_statistics()
            
            if stats:
                logger.info("=" * 50)
                logger.info("정책 통계 정보")
                logger.info("=" * 50)
                logger.info(f"총 정책 수: {stats.get('total_policies', 0)}건")
                
                categories = stats.get('categories', {})
                if categories:
                    logger.info("\n카테고리별 정책 수:")
                    for category, count in categories.items():
                        logger.info(f"  - {category}: {count}건")
                
                logger.info("=" * 50)
            else:
                logger.warning("통계 정보를 가져올 수 없습니다.")
                
        except Exception as e:
            logger.error(f"통계 정보 표시 중 오류: {e}")

def main():
    """메인 실행 함수"""
    
    # 명령행 인수 파싱
    parser = argparse.ArgumentParser(description='청년정책 데이터 OpenSearch 관리')
    
    parser.add_argument('--mode', choices=['setup', 'api', 'file', 'directory', 'search', 'stats'], 
                       default='setup', help='실행 모드')
    parser.add_argument('--opensearch-host', default='localhost', help='OpenSearch 호스트')
    parser.add_argument('--opensearch-port', type=int, default=9200, help='OpenSearch 포트')
    parser.add_argument('--reset-index', action='store_true', help='인덱스 재생성')
    
    # API 관련 인수
    parser.add_argument('--api-url', default='https://www.youthcenter.go.kr/cmnFooter/testbed',
                       help='API URL')
    parser.add_argument('--api-key', default='testKey', help='API 키')
    parser.add_argument('--api-sn', default='86', help='API 일련번호')
    parser.add_argument('--page-size', type=int, default=100, help='페이지 크기')
    parser.add_argument('--max-pages', type=int, help='최대 페이지 수')
    
    # 파일 관련 인수
    parser.add_argument('--file-path', help='인덱싱할 파일 경로')
    parser.add_argument('--directory-path', default='youth_policy_data', help='인덱싱할 디렉토리 경로')
    
    # 검색 관련 인수
    parser.add_argument('--search-type', choices=['keyword', 'category', 'age', 'region'],
                       default='keyword', help='검색 타입')
    parser.add_argument('--search-value', help='검색 값')
    parser.add_argument('--search-size', type=int, default=10, help='검색 결과 개수')
    
    args = parser.parse_args()
    
    # 프로세서 초기화
    processor = YouthPolicyProcessor(args.opensearch_host, args.opensearch_port)
    
    try:
        if args.mode == 'setup':
            # OpenSearch 설정
            success = processor.setup_opensearch(args.reset_index)
            if success:
                logger.info("OpenSearch 설정 완료")
            else:
                logger.error("OpenSearch 설정 실패")
        
        elif args.mode == 'api':
            # API 데이터 인덱싱
            if not processor.setup_opensearch(args.reset_index):
                logger.error("OpenSearch 설정 실패")
                return
            
            api_params = {
                'apiKeyNm': args.api_key,
                'apiSn': args.api_sn,
                'pageSize': args.page_size
            }
            
            success = processor.fetch_and_index_api_data(
                args.api_url, api_params, args.max_pages
            )
            
            if success:
                logger.info("API 데이터 인덱싱 완료")
            else:
                logger.error("API 데이터 인덱싱 실패")
        
        elif args.mode == 'file':
            # 단일 파일 인덱싱
            if not args.file_path:
                logger.error("--file-path 인수가 필요합니다.")
                return
            
            if not processor.setup_opensearch():
                logger.error("OpenSearch 설정 실패")
                return
            
            success = processor.index_file_data(args.file_path)
            
            if success:
                logger.info("파일 데이터 인덱싱 완료")
            else:
                logger.error("파일 데이터 인덱싱 실패")
        
        elif args.mode == 'directory':
            # 디렉토리 파일 인덱싱
            if not processor.setup_opensearch():
                logger.error("OpenSearch 설정 실패")
                return
            
            success = processor.index_directory_files(args.directory_path)
            
            if success:
                logger.info("디렉토리 파일 인덱싱 완료")
            else:
                logger.error("디렉토리 파일 인덱싱 실패")
        
        elif args.mode == 'search':
            # 검색 실행
            if not args.search_value:
                logger.error("--search-value 인수가 필요합니다.")
                return
            
            results = processor.search_and_display_results(
                args.search_type, args.search_value, args.search_size
            )
            
            if results:
                logger.info("검색 완료")
            else:
                logger.info("검색 결과가 없습니다.")
        
        elif args.mode == 'stats':
            # 통계 정보 표시
            processor.show_statistics()
    
    except KeyboardInterrupt:
        logger.warning("사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
