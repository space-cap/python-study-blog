import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('opensearch_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OpenSearchManager:
    """
    OpenSearch 클러스터와 상호작용하는 클래스
    청년정책 데이터를 OpenSearch에 저장하고 검색하는 기능 제공
    """
    
    def __init__(self, host: str = "localhost", port: int = 9200, 
                 username: str = None, password: str = None):
        """
        OpenSearch 매니저 초기화
        
        Args:
            host: OpenSearch 호스트
            port: OpenSearch 포트
            username: 사용자명 (보안 설정 시)
            password: 비밀번호 (보안 설정 시)
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        
        # 인증 설정 (필요시)
        # if username and password:
        #    self.session.auth = (username, password)
        
        # 기본 헤더 설정
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 통계 정보 초기화
        self.stats = {
            'total_indexed': 0,
            'total_updated': 0,
            'total_failed': 0,
            'start_time': None,
            'end_time': None
        }
    
    def check_connection(self) -> bool:
        """
        OpenSearch 연결 상태 확인
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                cluster_info = response.json()
                logger.info(f"OpenSearch 연결 성공: {cluster_info.get('version', {}).get('number', 'Unknown')}")
                return True
            else:
                logger.error(f"OpenSearch 연결 실패: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"OpenSearch 연결 오류: {e}")
            return False
    
    def create_index(self, index_name: str, mapping_file: str = None) -> bool:
        """
        인덱스 생성
        
        Args:
            index_name: 생성할 인덱스명
            mapping_file: 매핑 정의 파일 경로
            
        Returns:
            bool: 생성 성공 여부
        """
        try:
            # 인덱스 존재 확인
            if self.index_exists(index_name):
                logger.info(f"인덱스 '{index_name}'이 이미 존재합니다.")
                return True
            
            # 매핑 정의 로드
            mapping_data = {}
            if mapping_file:
                try:
                    with open(mapping_file, 'r', encoding='utf-8') as f:
                        mapping_data = json.load(f)
                except FileNotFoundError:
                    logger.warning(f"매핑 파일을 찾을 수 없습니다: {mapping_file}")
                except json.JSONDecodeError as e:
                    logger.error(f"매핑 파일 JSON 파싱 오류: {e}")
                    return False
            
            # 인덱스 생성
            response = self.session.put(
                f"{self.base_url}/{index_name}",
                json=mapping_data
            )
            
            if response.status_code == 200:
                logger.info(f"인덱스 '{index_name}' 생성 완료")
                return True
            else:
                logger.error(f"인덱스 생성 실패: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"인덱스 생성 중 오류: {e}")
            return False
    
    def index_exists(self, index_name: str) -> bool:
        """
        인덱스 존재 여부 확인
        
        Args:
            index_name: 확인할 인덱스명
            
        Returns:
            bool: 존재 여부
        """
        try:
            response = self.session.head(f"{self.base_url}/{index_name}")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"인덱스 존재 확인 중 오류: {e}")
            return False
    
    def delete_index(self, index_name: str) -> bool:
        """
        인덱스 삭제
        
        Args:
            index_name: 삭제할 인덱스명
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            if not self.index_exists(index_name):
                logger.warning(f"인덱스 '{index_name}'이 존재하지 않습니다.")
                return True
            
            response = self.session.delete(f"{self.base_url}/{index_name}")
            
            if response.status_code == 200:
                logger.info(f"인덱스 '{index_name}' 삭제 완료")
                return True
            else:
                logger.error(f"인덱스 삭제 실패: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"인덱스 삭제 중 오류: {e}")
            return False
    
    def process_policy_data(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        정책 데이터를 OpenSearch에 저장하기 위해 전처리
        
        Args:
            policy_data: 원본 정책 데이터
            
        Returns:
            Dict: 전처리된 데이터
        """
        processed_data = policy_data.copy()
        
        # 숫자 필드 처리
        numeric_fields = {
            'sprtSclCnt': 'sprtSclCnt',
            'sprtTrgtMinAge': 'sprtTrgtMinAge', 
            'sprtTrgtMaxAge': 'sprtTrgtMaxAge',
            'earnMinAmt': 'earnMinAmt',
            'earnMaxAmt': 'earnMaxAmt',
            'inqCnt': 'inqCnt'
        }
        
        for field, processed_field in numeric_fields.items():
            value = policy_data.get(field, '0')
            if value and str(value).strip():
                try:
                    processed_data[processed_field] = int(value)
                except ValueError:
                    processed_data[processed_field] = 0
            else:
                processed_data[processed_field] = 0
        
        # 날짜 필드 처리
        date_fields = ['bizPrdBgngYmd', 'bizPrdEndYmd']
        for field in date_fields:
            value = policy_data.get(field, '').strip()
            if value and value != '        ':  # 8칸 공백 체크
                try:
                    # YYYYMMDD 형식을 YYYY-MM-DD로 변환
                    if len(value) == 8 and value.isdigit():
                        formatted_date = f"{value[:4]}-{value[4:6]}-{value[6:8]}"
                        processed_data[field] = formatted_date
                    else:
                        processed_data[field] = value
                except ValueError:
                    processed_data[field] = None
            else:
                processed_data[field] = None
        
        # 콤마로 구분된 코드 필드를 배열로 변환
        code_fields = {
            'zipCd': 'zipCodes',
            'plcyMajorCd': 'majorCodes',
            'jobCd': 'jobCodes',
            'schoolCd': 'schoolCodes'
        }
        
        for original_field, array_field in code_fields.items():
            value = policy_data.get(original_field, '')
            if value and value.strip():
                # 콤마로 분리하여 배열 생성
                codes = [code.strip() for code in value.split(',') if code.strip()]
                processed_data[array_field] = codes
            else:
                processed_data[array_field] = []
        
        # 메타데이터 추가
        processed_data['indexed_at'] = datetime.now().isoformat()
        processed_data['data_source'] = 'youth_policy_api'
        
        # 빈 문자열을 null로 변환
        for key, value in processed_data.items():
            if isinstance(value, str) and value.strip() == '':
                processed_data[key] = None
        
        return processed_data
    
    def index_policy_document(self, index_name: str, policy_data: Dict[str, Any]) -> bool:
        """
        단일 정책 문서를 인덱스에 저장
        
        Args:
            index_name: 인덱스명
            policy_data: 정책 데이터
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            # 데이터 전처리
            processed_data = self.process_policy_data(policy_data)
            
            # 문서 ID는 정책 번호 사용
            doc_id = processed_data.get('plcyNo')
            if not doc_id:
                logger.error("정책 번호(plcyNo)가 없습니다.")
                return False
            
            # 문서 인덱싱
            response = self.session.put(
                f"{self.base_url}/{index_name}/_doc/{doc_id}",
                json=processed_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                action = result.get('result', 'unknown')
                
                if action == 'created':
                    self.stats['total_indexed'] += 1
                    logger.debug(f"문서 생성: {doc_id}")
                elif action == 'updated':
                    self.stats['total_updated'] += 1
                    logger.debug(f"문서 업데이트: {doc_id}")
                
                return True
            else:
                logger.error(f"문서 인덱싱 실패: {response.status_code} - {response.text}")
                self.stats['total_failed'] += 1
                return False
                
        except Exception as e:
            logger.error(f"문서 인덱싱 중 오류: {e}")
            self.stats['total_failed'] += 1
            return False
    
    def bulk_index_policies(self, index_name: str, policies: List[Dict[str, Any]]) -> bool:
        """
        여러 정책을 한 번에 인덱싱 (벌크 인덱싱)
        
        Args:
            index_name: 인덱스명
            policies: 정책 데이터 리스트
            
        Returns:
            bool: 전체 처리 성공 여부
        """
        if not policies:
            logger.warning("인덱싱할 정책 데이터가 없습니다.")
            return True
        
        try:
            # 벌크 요청 데이터 구성
            bulk_data = []
            
            for policy in policies:
                processed_data = self.process_policy_data(policy)
                doc_id = processed_data.get('plcyNo')
                
                if not doc_id:
                    logger.warning("정책 번호가 없는 데이터 건너뜀")
                    continue
                
                # 인덱스 액션 정의
                index_action = {
                    "index": {
                        "_index": index_name,
                        "_id": doc_id
                    }
                }
                
                bulk_data.append(json.dumps(index_action))
                bulk_data.append(json.dumps(processed_data))
            
            if not bulk_data:
                logger.warning("유효한 인덱싱 데이터가 없습니다.")
                return False
            
            # 벌크 요청 실행
            bulk_body = '\n'.join(bulk_data) + '\n'
            
            response = self.session.post(
                f"{self.base_url}/_bulk",
                data=bulk_body,
                headers={'Content-Type': 'application/x-ndjson'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 결과 분석
                if result.get('errors'):
                    # 개별 오류 처리
                    for item in result.get('items', []):
                        if 'index' in item:
                            index_result = item['index']
                            if index_result.get('status') in [200, 201]:
                                if index_result.get('result') == 'created':
                                    self.stats['total_indexed'] += 1
                                elif index_result.get('result') == 'updated':
                                    self.stats['total_updated'] += 1
                            else:
                                self.stats['total_failed'] += 1
                                logger.error(f"벌크 인덱싱 개별 오류: {index_result.get('error', 'Unknown')}")
                else:
                    # 전체 성공
                    for item in result.get('items', []):
                        if 'index' in item:
                            index_result = item['index']
                            if index_result.get('result') == 'created':
                                self.stats['total_indexed'] += 1
                            elif index_result.get('result') == 'updated':
                                self.stats['total_updated'] += 1
                
                logger.info(f"벌크 인덱싱 완료: {len(policies)}건 처리")
                return True
            else:
                logger.error(f"벌크 인덱싱 실패: {response.status_code} - {response.text}")
                self.stats['total_failed'] += len(policies)
                return False
                
        except Exception as e:
            logger.error(f"벌크 인덱싱 중 오류: {e}")
            self.stats['total_failed'] += len(policies)
            return False
    
    def search_policies(self, index_name: str, query: Dict[str, Any], 
                       size: int = 10, from_: int = 0) -> Dict[str, Any]:
        """
        정책 검색
        
        Args:
            index_name: 검색할 인덱스명
            query: 검색 쿼리
            size: 결과 개수
            from_: 시작 위치
            
        Returns:
            Dict: 검색 결과
        """
        try:
            search_body = {
                "query": query,
                "size": size,
                "from": from_,
                "sort": [
                    {"frstRegDt": {"order": "desc"}},
                    {"_score": {"order": "desc"}}
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/{index_name}/_search",
                json=search_body
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"검색 실패: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"검색 중 오류: {e}")
            return {}
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """
        인덱스 통계 조회
        
        Args:
            index_name: 인덱스명
            
        Returns:
            Dict: 통계 정보
        """
        try:
            response = self.session.get(f"{self.base_url}/{index_name}/_stats")
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"통계 조회 실패: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"통계 조회 중 오류: {e}")
            return {}
    
    def refresh_index(self, index_name: str) -> bool:
        """
        인덱스 새로고침 (검색 가능하도록)
        
        Args:
            index_name: 새로고침할 인덱스명
            
        Returns:
            bool: 성공 여부
        """
        try:
            response = self.session.post(f"{self.base_url}/{index_name}/_refresh")
            
            if response.status_code == 200:
                logger.info(f"인덱스 '{index_name}' 새로고침 완료")
                return True
            else:
                logger.error(f"인덱스 새로고침 실패: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"인덱스 새로고침 중 오류: {e}")
            return False
    
    def print_stats(self):
        """통계 정보 출력"""
        logger.info("=" * 50)
        logger.info("OpenSearch 인덱싱 통계")
        logger.info("=" * 50)
        
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            logger.info(f"처리 시간: {duration}")
        
        logger.info(f"신규 인덱싱: {self.stats['total_indexed']}건")
        logger.info(f"업데이트: {self.stats['total_updated']}건")
        logger.info(f"실패: {self.stats['total_failed']}건")
        
        total_processed = self.stats['total_indexed'] + self.stats['total_updated'] + self.stats['total_failed']
        if total_processed > 0:
            success_rate = ((self.stats['total_indexed'] + self.stats['total_updated']) / total_processed) * 100
            logger.info(f"성공률: {success_rate:.1f}%")
        
        logger.info("=" * 50)

class YouthPolicyOpenSearchManager:
    """
    청년정책 API 데이터를 OpenSearch에 저장하는 통합 매니저
    """
    
    def __init__(self, opensearch_host: str = "localhost", opensearch_port: int = 9200):
        """
        통합 매니저 초기화
        
        Args:
            opensearch_host: OpenSearch 호스트
            opensearch_port: OpenSearch 포트
        """
        self.opensearch = OpenSearchManager(host=opensearch_host, port=opensearch_port)
        self.index_name = "youth_policies"
        
    def setup_index(self, mapping_file: str = "opensearch_mapping.json") -> bool:
        """
        인덱스 설정 및 생성
        
        Args:
            mapping_file: 매핑 파일 경로
            
        Returns:
            bool: 설정 성공 여부
        """
        try:
            # OpenSearch 연결 확인
            if not self.opensearch.check_connection():
                logger.error("OpenSearch 연결 실패")
                return False
            
            # 인덱스 생성
            if not self.opensearch.create_index(self.index_name, mapping_file):
                logger.error("인덱스 생성 실패")
                return False
            
            logger.info("인덱스 설정 완료")
            return True
            
        except Exception as e:
            logger.error(f"인덱스 설정 중 오류: {e}")
            return False
    
    def index_api_data(self, api_data: Dict[str, Any]) -> bool:
        """
        API 데이터를 OpenSearch에 인덱싱
        
        Args:
            api_data: API 응답 데이터
            
        Returns:
            bool: 인덱싱 성공 여부
        """
        try:
            # 데이터 유효성 검사
            if not api_data.get('result', {}).get('youthPolicyList'):
                logger.warning("인덱싱할 정책 데이터가 없습니다.")
                return False
            
            policies = api_data['result']['youthPolicyList']
            
            # 통계 시작
            self.opensearch.stats['start_time'] = datetime.now()
            
            # 벌크 인덱싱 실행
            success = self.opensearch.bulk_index_policies(self.index_name, policies)
            
            # 통계 종료
            self.opensearch.stats['end_time'] = datetime.now()
            
            if success:
                # 인덱스 새로고침
                self.opensearch.refresh_index(self.index_name)
                
                # 통계 출력
                self.opensearch.print_stats()
                
                logger.info(f"API 데이터 인덱싱 완료: {len(policies)}건")
                return True
            else:
                logger.error("API 데이터 인덱싱 실패")
                return False
                
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
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            
            # API 데이터 인덱싱
            return self.index_api_data(file_data)
            
        except FileNotFoundError:
            logger.error(f"파일을 찾을 수 없습니다: {file_path}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파일 파싱 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"파일 데이터 인덱싱 중 오류: {e}")
            return False
    
    def search_by_keyword(self, keyword: str, size: int = 10) -> List[Dict[str, Any]]:
        """
        키워드로 정책 검색
        
        Args:
            keyword: 검색 키워드
            size: 결과 개수
            
        Returns:
            List: 검색 결과
        """
        query = {
            "multi_match": {
                "query": keyword,
                "fields": [
                    "plcyNm^3",
                    "plcyExplnCn^2",
                    "plcySprtCn^2",
                    "plcyKywdNm^2",
                    "sprvsnInstCdNm",
                    "operInstCdNm"
                ],
                "type": "best_fields"
            }
        }
        
        result = self.opensearch.search_policies(self.index_name, query, size)
        
        hits = result.get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    
    def search_by_category(self, category: str, size: int = 10) -> List[Dict[str, Any]]:
        """
        카테고리별 정책 검색
        
        Args:
            category: 카테고리 (대분류)
            size: 결과 개수
            
        Returns:
            List: 검색 결과
        """
        query = {
            "term": {
                "lclsfNm": category
            }
        }
        
        result = self.opensearch.search_policies(self.index_name, query, size)
        
        hits = result.get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    
    def search_by_age_range(self, min_age: int, max_age: int, size: int = 10) -> List[Dict[str, Any]]:
        """
        연령대별 정책 검색
        
        Args:
            min_age: 최소 연령
            max_age: 최대 연령
            size: 결과 개수
            
        Returns:
            List: 검색 결과
        """
        query = {
            "bool": {
                "should": [
                    {
                        "bool": {
                            "must": [
                                {"range": {"sprtTrgtMinAge": {"lte": max_age}}},
                                {"range": {"sprtTrgtMaxAge": {"gte": min_age}}}
                            ]
                        }
                    },
                    {
                        "bool": {
                            "must_not": [
                                {"exists": {"field": "sprtTrgtMinAge"}},
                                {"exists": {"field": "sprtTrgtMaxAge"}}
                            ]
                        }
                    }
                ]
            }
        }
        
        result = self.opensearch.search_policies(self.index_name, query, size)
        
        hits = result.get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    
    def search_by_region(self, region_code: str, size: int = 10) -> List[Dict[str, Any]]:
        """
        지역별 정책 검색
        
        Args:
            region_code: 지역 코드
            size: 결과 개수
            
        Returns:
            List: 검색 결과
        """
        query = {
            "term": {
                "zipCodes": region_code
            }
        }
        
        result = self.opensearch.search_policies(self.index_name, query, size)
        
        hits = result.get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    
    def get_policy_statistics(self) -> Dict[str, Any]:
        """
        정책 통계 조회
        
        Returns:
            Dict: 통계 정보
        """
        try:
            # 전체 문서 수
            total_query = {"match_all": {}}
            total_result = self.opensearch.search_policies(self.index_name, total_query, size=0)
            total_count = total_result.get('hits', {}).get('total', {}).get('value', 0)
            
            # 카테고리별 통계
            category_agg = {
                "size": 0,
                "aggs": {
                    "categories": {
                        "terms": {
                            "field": "lclsfNm",
                            "size": 10
                        }
                    }
                }
            }
            
            category_result = self.opensearch.session.post(
                f"{self.opensearch.base_url}/{self.index_name}/_search",
                json=category_agg
            )
            
            categories = {}
            if category_result.status_code == 200:
                agg_data = category_result.json()
                buckets = agg_data.get('aggregations', {}).get('categories', {}).get('buckets', [])
                categories = {bucket['key']: bucket['doc_count'] for bucket in buckets}
            
            return {
                'total_policies': total_count,
                'categories': categories,
                'index_stats': self.opensearch.get_index_stats(self.index_name)
            }
            
        except Exception as e:
            logger.error(f"통계 조회 중 오류: {e}")
            return {}
