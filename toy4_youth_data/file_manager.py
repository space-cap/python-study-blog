import requests
import json
import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youth_policy_file_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouthPolicyFileManager:
    """
    청년정책 API 데이터를 파일로 저장하는 클래스
    API 데이터를 JSON 형태로 텍스트 파일에 저장하고 관리하는 기능 제공
    """
    
    def __init__(self, output_dir: str = "youth_policy_data"):
        """
        파일 관리자 초기화
        
        Args:
            output_dir: 출력 파일이 저장될 디렉토리 경로
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 출력 디렉토리 생성
        self._create_output_directory()
        
        # 통계 정보 초기화
        self.stats = {
            'total_files': 0,
            'total_policies': 0,
            'success_count': 0,
            'error_count': 0,
            'start_time': None,
            'end_time': None
        }
    
    def _create_output_directory(self):
        """출력 디렉토리 생성"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"출력 디렉토리 생성/확인: {self.output_dir}")
        except Exception as e:
            logger.error(f"출력 디렉토리 생성 실패: {e}")
            raise
    
    def fetch_api_data(self, api_url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        청년정책 API에서 데이터 가져오기
        
        Args:
            api_url: API URL
            params: API 요청 파라미터
            
        Returns:
            Dict: API 응답 데이터 또는 None (실패 시)
        """
        start_time = time.time()
        
        try:
            # API 요청 정보 로깅
            logger.info(f"API 요청 시작: {api_url}")
            logger.info(f"요청 파라미터: {params}")
            
            # API 요청 (타임아웃 설정)
            response = self.session.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # 응답 상태 확인
            logger.info(f"API 응답 상태: {response.status_code}")
            
            # JSON 데이터 파싱
            data = response.json()
            
            # 응답 데이터 유효성 검사
            if not self._validate_response_data(data):
                logger.error("API 응답 데이터가 유효하지 않음")
                return None
            
            # 실행 시간 계산
            execution_time = time.time() - start_time
            
            # 성공 로깅
            result = data.get('result', {})
            pagging = result.get('pagging', {})
            policy_list = result.get('youthPolicyList', [])
            
            logger.info(f"API 호출 성공:")
            logger.info(f"  - 실행시간: {execution_time:.2f}초")
            logger.info(f"  - 총 데이터 수: {pagging.get('totCount', 0)}건")
            logger.info(f"  - 현재 페이지: {pagging.get('pageNum', 0)}")
            logger.info(f"  - 페이지 크기: {pagging.get('pageSize', 0)}")
            logger.info(f"  - 현재 페이지 데이터 수: {len(policy_list)}건")
            
            return data
            
        except requests.exceptions.Timeout:
            logger.error("API 요청 타임아웃")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 실패: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            return None
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return None
    
    def _validate_response_data(self, data: Dict[str, Any]) -> bool:
        """
        API 응답 데이터 유효성 검사
        
        Args:
            data: API 응답 데이터
            
        Returns:
            bool: 유효성 검사 결과
        """
        # 기본 구조 검사
        if not isinstance(data, dict):
            logger.error("응답 데이터가 딕셔너리가 아님")
            return False
        
        # 결과 코드 확인
        result_code = data.get('resultCode')
        if result_code != 200:
            logger.error(f"API 결과 코드 오류: {result_code}")
            logger.error(f"결과 메시지: {data.get('resultMessage', 'Unknown')}")
            return False
        
        # result 구조 확인
        result = data.get('result')
        if not isinstance(result, dict):
            logger.error("result 필드가 딕셔너리가 아님")
            return False
        
        # youthPolicyList 확인
        youth_policy_list = result.get('youthPolicyList')
        if not isinstance(youth_policy_list, list):
            logger.error("youthPolicyList 필드가 리스트가 아님")
            return False
        
        return True
    
    def generate_filename(self, api_sn: str, page_num: int, page_size: int) -> str:
        """
        파일명 생성
        
        Args:
            api_sn: API 일련번호
            page_num: 페이지 번호
            page_size: 페이지 크기
            
        Returns:
            str: 생성된 파일명
        """
        filename = f"youthcenter-{api_sn}-{page_num}-{page_size}.txt"
        return os.path.join(self.output_dir, filename)
    
    def save_to_file(self, data: Dict[str, Any], filename: str, 
                     pretty_print: bool = True, add_metadata: bool = True) -> bool:
        """
        데이터를 파일로 저장
        
        Args:
            data: 저장할 데이터
            filename: 저장할 파일명
            pretty_print: JSON 데이터를 보기 좋게 포맷팅할지 여부
            add_metadata: 메타데이터 추가 여부
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            # 메타데이터 추가
            if add_metadata:
                data = self._add_metadata_to_data(data)
            
            # 파일 저장
            with open(filename, 'w', encoding='utf-8') as f:
                if pretty_print:
                    # 보기 좋게 포맷팅하여 저장
                    json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
                else:
                    # 한 줄로 저장 (공간 절약)
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            
            # 파일 크기 확인
            file_size = os.path.getsize(filename)
            logger.info(f"파일 저장 성공: {filename}")
            logger.info(f"파일 크기: {self._format_file_size(file_size)}")
            
            return True
            
        except IOError as e:
            logger.error(f"파일 저장 실패 (I/O 오류): {filename} - {e}")
            return False
        except Exception as e:
            logger.error(f"파일 저장 실패 (기타 오류): {filename} - {e}")
            return False
    
    def _add_metadata_to_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        데이터에 메타데이터 추가
        
        Args:
            data: 원본 데이터
            
        Returns:
            Dict: 메타데이터가 추가된 데이터
        """
        # 원본 데이터 복사
        enhanced_data = data.copy()
        
        # 메타데이터 추가
        metadata = {
            'file_saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_created_by': 'YouthPolicyFileManager',
            'api_response_time': datetime.now().isoformat(),
            'data_summary': {
                'total_policies': len(data.get('result', {}).get('youthPolicyList', [])),
                'result_code': data.get('resultCode'),
                'result_message': data.get('resultMessage')
            }
        }
        
        enhanced_data['file_metadata'] = metadata
        
        return enhanced_data
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        파일 크기를 읽기 쉬운 형태로 포맷팅
        
        Args:
            size_bytes: 바이트 단위 파일 크기
            
        Returns:
            str: 포맷팅된 파일 크기
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def collect_all_pages(self, api_url: str, base_params: Dict[str, Any], 
                         max_pages: int = None, delay_between_requests: float = 0.5) -> bool:
        """
        모든 페이지의 데이터를 수집하여 파일로 저장
        
        Args:
            api_url: API URL
            base_params: 기본 API 파라미터
            max_pages: 최대 수집 페이지 수 (None이면 모든 페이지)
            delay_between_requests: 요청 간 지연 시간 (초)
            
        Returns:
            bool: 전체 수집 성공 여부
        """
        self.stats['start_time'] = datetime.now()
        logger.info("전체 페이지 데이터 수집 시작")
        
        try:
            page_num = 1
            total_count = None
            
            while True:
                # 페이지별 파라미터 설정
                params = base_params.copy()
                params['pageNum'] = page_num
                
                logger.info(f"페이지 {page_num} 처리 시작")
                
                # API 데이터 가져오기
                api_data = self.fetch_api_data(api_url, params)
                
                if not api_data:
                    logger.error(f"페이지 {page_num} 데이터 가져오기 실패")
                    self.stats['error_count'] += 1
                    break
                
                # 총 데이터 수 확인 (첫 페이지에서만)
                if total_count is None:
                    pagging = api_data.get('result', {}).get('pagging', {})
                    total_count = pagging.get('totCount', 0)
                    page_size = pagging.get('pageSize', 100)
                    
                    logger.info(f"총 데이터 수: {total_count}건")
                    logger.info(f"페이지 크기: {page_size}건")
                    logger.info(f"예상 페이지 수: {(total_count + page_size - 1) // page_size}페이지")
                
                # 현재 페이지 데이터 확인
                current_policies = api_data.get('result', {}).get('youthPolicyList', [])
                if not current_policies:
                    logger.info(f"페이지 {page_num}에 더 이상 데이터가 없음")
                    break
                
                # 파일명 생성
                filename = self.generate_filename(
                    api_sn=params.get('apiSn', '86'),
                    page_num=page_num,
                    page_size=params.get('pageSize', 100)
                )
                
                # 파일 저장
                if self.save_to_file(api_data, filename):
                    self.stats['success_count'] += 1
                    self.stats['total_files'] += 1
                    self.stats['total_policies'] += len(current_policies)
                    
                    logger.info(f"페이지 {page_num} 처리 완료: {len(current_policies)}건 저장")
                else:
                    self.stats['error_count'] += 1
                    logger.error(f"페이지 {page_num} 파일 저장 실패")
                
                # 페이지 진행 상황 확인
                pagging = api_data.get('result', {}).get('pagging', {})
                current_page = pagging.get('pageNum', page_num)
                current_page_size = pagging.get('pageSize', 100)
                
                # 마지막 페이지 확인
                if current_page * current_page_size >= total_count:
                    logger.info("모든 페이지 처리 완료")
                    break
                
                # 최대 페이지 수 확인
                if max_pages and page_num >= max_pages:
                    logger.info(f"최대 페이지 수 도달: {max_pages}")
                    break
                
                # 다음 페이지로 이동
                page_num += 1
                
                # 요청 간 지연 (서버 부하 방지)
                if delay_between_requests > 0:
                    logger.debug(f"{delay_between_requests}초 대기 중...")
                    time.sleep(delay_between_requests)
            
            self.stats['end_time'] = datetime.now()
            self._print_final_statistics()
            
            return self.stats['error_count'] == 0
            
        except KeyboardInterrupt:
            logger.warning("사용자에 의해 중단됨")
            return False
        except Exception as e:
            logger.error(f"데이터 수집 중 오류 발생: {e}")
            return False
    
    def collect_single_page(self, api_url: str, params: Dict[str, Any]) -> bool:
        """
        단일 페이지 데이터 수집
        
        Args:
            api_url: API URL
            params: API 파라미터
            
        Returns:
            bool: 수집 성공 여부
        """
        self.stats['start_time'] = datetime.now()
        logger.info("단일 페이지 데이터 수집 시작")
        
        try:
            # API 데이터 가져오기
            api_data = self.fetch_api_data(api_url, params)
            
            if not api_data:
                logger.error("데이터 가져오기 실패")
                return False
            
            # 파일명 생성
            filename = self.generate_filename(
                api_sn=params.get('apiSn', '86'),
                page_num=params.get('pageNum', 1),
                page_size=params.get('pageSize', 100)
            )
            
            # 파일 저장
            if self.save_to_file(api_data, filename):
                policy_count = len(api_data.get('result', {}).get('youthPolicyList', []))
                self.stats['success_count'] = 1
                self.stats['total_files'] = 1
                self.stats['total_policies'] = policy_count
                
                logger.info(f"단일 페이지 처리 완료: {policy_count}건 저장")
                self.stats['end_time'] = datetime.now()
                self._print_final_statistics()
                return True
            else:
                self.stats['error_count'] = 1
                logger.error("파일 저장 실패")
                return False
                
        except Exception as e:
            logger.error(f"단일 페이지 수집 중 오류 발생: {e}")
            self.stats['error_count'] = 1
            return False
    
    def _print_final_statistics(self):
        """최종 통계 출력"""
        logger.info("=" * 50)
        logger.info("최종 처리 통계")
        logger.info("=" * 50)
        
        if self.stats['start_time'] and self.stats['end_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            logger.info(f"처리 시간: {duration}")
        
        logger.info(f"총 처리 파일 수: {self.stats['total_files']}개")
        logger.info(f"총 저장 정책 수: {self.stats['total_policies']}건")
        logger.info(f"성공 파일 수: {self.stats['success_count']}개")
        logger.info(f"실패 파일 수: {self.stats['error_count']}개")
        
        if self.stats['total_files'] > 0:
            success_rate = (self.stats['success_count'] / self.stats['total_files']) * 100
            logger.info(f"성공률: {success_rate:.1f}%")
        
        logger.info(f"출력 디렉토리: {os.path.abspath(self.output_dir)}")
        logger.info("=" * 50)
    
    def list_saved_files(self) -> List[Dict[str, Any]]:
        """
        저장된 파일 목록 조회
        
        Returns:
            List: 파일 정보 리스트
        """
        files = []
        
        try:
            for filename in os.listdir(self.output_dir):
                if filename.startswith('youthcenter-') and filename.endswith('.txt'):
                    filepath = os.path.join(self.output_dir, filename)
                    stat = os.stat(filepath)
                    
                    files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': stat.st_size,
                        'size_formatted': self._format_file_size(stat.st_size),
                        'created_time': datetime.fromtimestamp(stat.st_ctime),
                        'modified_time': datetime.fromtimestamp(stat.st_mtime)
                    })
            
            # 수정 시간 기준 정렬
            files.sort(key=lambda x: x['modified_time'], reverse=True)
            
        except Exception as e:
            logger.error(f"파일 목록 조회 실패: {e}")
        
        return files
    
    def validate_saved_file(self, filename: str) -> bool:
        """
        저장된 파일의 유효성 검사
        
        Args:
            filename: 검사할 파일명
            
        Returns:
            bool: 유효성 검사 결과
        """
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            if not os.path.exists(filepath):
                logger.error(f"파일이 존재하지 않음: {filepath}")
                return False
            
            # 파일 크기 확인
            file_size = os.path.getsize(filepath)
            if file_size == 0:
                logger.error(f"파일이 비어있음: {filepath}")
                return False
            
            # JSON 형식 검증
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 데이터 구조 검증
            if not self._validate_response_data(data):
                logger.error(f"파일 데이터 구조가 올바르지 않음: {filepath}")
                return False
            
            logger.info(f"파일 유효성 검사 통과: {filename}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {filepath} - {e}")
            return False
        except Exception as e:
            logger.error(f"파일 검증 중 오류: {filepath} - {e}")
            return False
    
    def cleanup_old_files(self, days_old: int = 30) -> int:
        """
        오래된 파일 정리
        
        Args:
            days_old: 삭제할 파일의 기준 일수
            
        Returns:
            int: 삭제된 파일 수
        """
        deleted_count = 0
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        try:
            for filename in os.listdir(self.output_dir):
                if filename.startswith('youthcenter-') and filename.endswith('.txt'):
                    filepath = os.path.join(self.output_dir, filename)
                    
                    # 파일 수정 시간 확인
                    if os.path.getmtime(filepath) < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
                        logger.info(f"오래된 파일 삭제: {filename}")
            
            logger.info(f"총 {deleted_count}개의 오래된 파일 삭제 완료")
            
        except Exception as e:
            logger.error(f"파일 정리 중 오류: {e}")
        
        return deleted_count

def main():
    """메인 실행 함수"""
    
    # 파일 매니저 초기화
    file_manager = YouthPolicyFileManager(output_dir="youth_policy_data")
    
    # API 설정
    api_url = "https://www.youthcenter.go.kr/cmnFooter/testbed"
    base_params = {
        'apiKeyNm': 'testKey',
        'apiSn': '86',
        'pageSize': 100  # 한 페이지당 가져올 데이터 수
    }
    
    try:
        # 실행 모드 선택
        mode = input("실행 모드를 선택하세요 (1: 모든 페이지, 2: 단일 페이지, 3: 파일 목록 조회): ").strip()
        
        if mode == '1':
            # 모든 페이지 수집
            logger.info("모든 페이지 데이터 수집 모드")
            
            # 최대 페이지 수 설정 (옵션)
            max_pages_input = input("최대 페이지 수 (엔터 시 모든 페이지): ").strip()
            max_pages = int(max_pages_input) if max_pages_input else None
            
            # 요청 간 지연 시간 설정
            delay_input = input("요청 간 지연 시간 (초, 기본값: 0.5): ").strip()
            delay = float(delay_input) if delay_input else 0.5
            
            # 데이터 수집 실행
            success = file_manager.collect_all_pages(
                api_url=api_url,
                base_params=base_params,
                max_pages=max_pages,
                delay_between_requests=delay
            )
            
            if success:
                logger.info("모든 페이지 수집 완료")
            else:
                logger.error("일부 페이지 수집 실패")
        
        elif mode == '2':
            # 단일 페이지 수집
            logger.info("단일 페이지 데이터 수집 모드")
            
            # 페이지 번호 입력
            page_num = input("페이지 번호 (기본값: 1): ").strip()
            page_num = int(page_num) if page_num else 1
            
            # 페이지 크기 입력
            page_size = input("페이지 크기 (기본값: 100): ").strip()
            page_size = int(page_size) if page_size else 100
            
            # 파라미터 설정
            params = base_params.copy()
            params['pageNum'] = page_num
            params['pageSize'] = page_size
            
            # 데이터 수집 실행
            success = file_manager.collect_single_page(api_url, params)
            
            if success:
                logger.info("단일 페이지 수집 완료")
            else:
                logger.error("단일 페이지 수집 실패")
        
        elif mode == '3':
            # 파일 목록 조회
            logger.info("저장된 파일 목록 조회")
            
            files = file_manager.list_saved_files()
            
            if files:
                logger.info(f"총 {len(files)}개의 파일이 저장되어 있습니다:")
                logger.info("-" * 80)
                
                for i, file_info in enumerate(files, 1):
                    logger.info(f"{i:2d}. {file_info['filename']}")
                    logger.info(f"     크기: {file_info['size_formatted']}")
                    logger.info(f"     수정일: {file_info['modified_time']}")
                    logger.info("-" * 80)
                
                # 파일 유효성 검사 옵션
                validate_input = input("파일 유효성 검사를 수행하시겠습니까? (y/n): ").strip().lower()
                if validate_input == 'y':
                    valid_count = 0
                    for file_info in files:
                        if file_manager.validate_saved_file(file_info['filename']):
                            valid_count += 1
                    
                    logger.info(f"유효성 검사 결과: {valid_count}/{len(files)} 파일이 유효합니다.")
            else:
                logger.info("저장된 파일이 없습니다.")
        
        else:
            logger.warning("잘못된 모드 선택")
    
    except KeyboardInterrupt:
        logger.warning("사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}")
    
    finally:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
