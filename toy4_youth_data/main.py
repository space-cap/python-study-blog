import requests
import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time
import logging
from typing import Dict, List, Optional, Any
import os
from urllib.parse import urlencode
from config import Config

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youth_policy_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouthPolicyDBManager:
    """
    청년정책 데이터베이스 관리 클래스
    API 데이터를 MySQL 데이터베이스에 저장하고 관리하는 기능 제공
    """
    
    def __init__(self, db_config: Dict[str, str]):
        """
        DB 연결 설정 초기화
        
        Args:
            db_config: 데이터베이스 연결 설정 딕셔너리
        """
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        
    def connect(self) -> bool:
        """
        데이터베이스 연결
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            self.connection = mysql.connector.connect(
                **self.db_config,
                autocommit=False,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            self.cursor = self.connection.cursor()
            logger.info("데이터베이스 연결 성공")
            return True
        except Error as e:
            logger.error(f"데이터베이스 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("데이터베이스 연결 해제")
    
    def fetch_api_data(self, api_url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        청년정책 API에서 데이터 가져오기
        
        Args:
            api_url: API URL
            params: API 요청 파라미터
            
        Returns:
            Dict: API 응답 데이터
        """
        start_time = time.time()
        
        try:
            # API 호출 로그 기록을 위한 정보 저장
            call_time = datetime.now()
            
            # API 요청
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # JSON 데이터 파싱
            data = response.json()
            
            # 실행 시간 계산
            execution_time = time.time() - start_time
            
            # API 호출 로그 저장
            self._log_api_call(
                api_url=api_url,
                call_time=call_time,
                response_code=response.status_code,
                total_count=data.get('result', {}).get('pagging', {}).get('totCount', 0),
                execution_time=execution_time
            )
            
            logger.info(f"API 호출 성공: {response.status_code}, 실행시간: {execution_time:.2f}초")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API 호출 실패: {e}")
            self._log_api_call(
                api_url=api_url,
                call_time=call_time,
                response_code=0,
                error_message=str(e),
                execution_time=time.time() - start_time
            )
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {e}")
            return {}
    
    def insert_policy_data(self, json_data: Dict[str, Any]) -> bool:
        """
        정책 데이터를 데이터베이스에 삽입
        
        Args:
            json_data: API에서 받은 JSON 데이터
            
        Returns:
            bool: 처리 성공 여부
        """
        if not json_data.get('result', {}).get('youthPolicyList'):
            logger.warning("삽입할 정책 데이터가 없습니다.")
            return False
        
        processed_count = 0
        error_count = 0
        
        try:
            # 트랜잭션 시작
            self.connection.start_transaction()
            
            # 각 정책 데이터 처리
            for policy in json_data['result']['youthPolicyList']:
                try:
                    # 메인 정책 데이터 삽입
                    self._insert_main_policy(policy)
                    
                    # 관련 코드 데이터 삽입 (정규화된 테이블)
                    self._insert_region_codes(policy)
                    self._insert_major_codes(policy)
                    self._insert_job_codes(policy)
                    self._insert_school_codes(policy)
                    
                    processed_count += 1
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"정책 {policy.get('plcyNo', 'Unknown')} 처리 실패: {e}")
                    continue
            
            # 트랜잭션 커밋
            self.connection.commit()
            
            logger.info(f"데이터 처리 완료: 성공 {processed_count}건, 실패 {error_count}건")
            return True
            
        except Exception as e:
            # 롤백
            self.connection.rollback()
            logger.error(f"데이터 삽입 실패: {e}")
            return False
    
    def _insert_main_policy(self, policy: Dict[str, Any]):
        """
        메인 정책 테이블에 데이터 삽입
        
        Args:
            policy: 정책 데이터 딕셔너리
        """
        sql = """
        INSERT INTO youth_policies (
            plcy_no, bsc_plan_cycl, bsc_plan_plcy_way_no, bsc_plan_fcs_asmt_no,
            bsc_plan_asmt_no, pvsn_inst_group_cd, plcy_pvsn_mthd_cd, plcy_aprv_stts_cd,
            plcy_nm, plcy_kywd_nm, plcy_expln_cn, lclsf_nm, mclsf_nm, plcy_sprt_cn,
            sprvsn_inst_cd, sprvsn_inst_cd_nm, sprvsn_inst_pic_nm,
            oper_inst_cd, oper_inst_cd_nm, oper_inst_pic_nm,
            sprt_scl_lmt_yn, aply_prd_se_cd, biz_prd_se_cd,
            biz_prd_bgnng_ymd, biz_prd_end_ymd, biz_prd_etc_cn,
            plcy_aply_mthd_cn, srng_mthd_cn, aply_url_addr,
            sbmsn_dcmnt_cn, etc_mttr_cn, ref_url_addr1, ref_url_addr2,
            sprt_scl_cnt, sprt_arvl_seq_yn, sprt_trgt_min_age, sprt_trgt_max_age,
            sprt_trgt_age_lmt_yn, mrg_stts_cd, earn_cnd_se_cd,
            earn_min_amt, earn_max_amt, earn_etc_cn,
            add_aply_qlfc_cnd_cn, ptcp_prp_trgt_cn, inq_cnt,
            rgtr_inst_cd, rgtr_inst_cd_nm, rgtr_up_inst_cd, rgtr_up_inst_cd_nm,
            rgtr_hghrk_inst_cd, rgtr_hghrk_inst_cd_nm,
            plcy_major_cd, job_cd, school_cd, sbiz_cd,
            aply_ymd, frst_reg_dt, last_mdfcn_dt
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON DUPLICATE KEY UPDATE
            plcy_nm = VALUES(plcy_nm),
            plcy_kywd_nm = VALUES(plcy_kywd_nm),
            plcy_expln_cn = VALUES(plcy_expln_cn),
            lclsf_nm = VALUES(lclsf_nm),
            mclsf_nm = VALUES(mclsf_nm),
            plcy_sprt_cn = VALUES(plcy_sprt_cn),
            sprvsn_inst_cd_nm = VALUES(sprvsn_inst_cd_nm),
            last_mdfcn_dt = VALUES(last_mdfcn_dt),
            updated_at = CURRENT_TIMESTAMP
        """
        
        # 날짜 문자열을 datetime 객체로 변환
        frst_reg_dt = self._parse_datetime(policy.get('frstRegDt'))
        last_mdfcn_dt = self._parse_datetime(policy.get('lastMdfcnDt'))
        
        # 숫자 필드 처리
        sprt_trgt_min_age = self._parse_int(policy.get('sprtTrgtMinAge'))
        sprt_trgt_max_age = self._parse_int(policy.get('sprtTrgtMaxAge'))
        earn_min_amt = self._parse_int(policy.get('earnMinAmt'))
        earn_max_amt = self._parse_int(policy.get('earnMaxAmt'))
        inq_cnt = self._parse_int(policy.get('inqCnt'))
        
        values = (
            policy.get('plcyNo'),
            policy.get('bscPlanCycl'),
            policy.get('bscPlanPlcyWayNo'),
            policy.get('bscPlanFcsAsmtNo'),
            policy.get('bscPlanAsmtNo'),
            policy.get('pvsnInstGroupCd'),
            policy.get('plcyPvsnMthdCd'),
            policy.get('plcyAprvSttsCd'),
            policy.get('plcyNm'),
            policy.get('plcyKywdNm'),
            policy.get('plcyExplnCn'),
            policy.get('lclsfNm'),
            policy.get('mclsfNm'),
            policy.get('plcySprtCn'),
            policy.get('sprvsnInstCd'),
            policy.get('sprvsnInstCdNm'),
            policy.get('sprvsnInstPicNm'),
            policy.get('operInstCd'),
            policy.get('operInstCdNm'),
            policy.get('operInstPicNm'),
            policy.get('sprtSclLmtYn'),
            policy.get('aplyPrdSeCd'),
            policy.get('bizPrdSeCd'),
            policy.get('bizPrdBgngYmd'),
            policy.get('bizPrdEndYmd'),
            policy.get('bizPrdEtcCn'),
            policy.get('plcyAplyMthdCn'),
            policy.get('srngMthdCn'),
            policy.get('aplyUrlAddr'),
            policy.get('sbmsnDcmntCn'),
            policy.get('etcMttrCn'),
            policy.get('refUrlAddr1'),
            policy.get('refUrlAddr2'),
            policy.get('sprtSclCnt'),
            policy.get('sprtArvlSeqYn'),
            sprt_trgt_min_age,
            sprt_trgt_max_age,
            policy.get('sprtTrgtAgeLmtYn'),
            policy.get('mrgSttsCd'),
            policy.get('earnCndSeCd'),
            earn_min_amt,
            earn_max_amt,
            policy.get('earnEtcCn'),
            policy.get('addAplyQlfcCndCn'),
            policy.get('ptcpPrpTrgtCn'),
            inq_cnt,
            policy.get('rgtrInstCd'),
            policy.get('rgtrInstCdNm'),
            policy.get('rgtrUpInstCd'),
            policy.get('rgtrUpInstCdNm'),
            policy.get('rgtrHghrkInstCd'),
            policy.get('rgtrHghrkInstCdNm'),
            policy.get('plcyMajorCd'),
            policy.get('jobCd'),
            policy.get('schoolCd'),
            policy.get('sbizCd'),
            policy.get('aplyYmd'),
            frst_reg_dt,
            last_mdfcn_dt
        )
        
        self.cursor.execute(sql, values)
    
    def _insert_region_codes(self, policy: Dict[str, Any]):
        """지역 코드 매핑 테이블에 데이터 삽입"""
        zip_codes = policy.get('zipCd', '').strip()
        if not zip_codes:
            return
        
        plcy_no = policy.get('plcyNo')
        
        # 기존 데이터 삭제
        self.cursor.execute(
            "DELETE FROM policy_regions WHERE plcy_no = %s",
            (plcy_no,)
        )
        
        # 새 데이터 삽입
        for zip_code in zip_codes.split(','):
            zip_code = zip_code.strip()
            if zip_code:
                self.cursor.execute(
                    "INSERT INTO policy_regions (plcy_no, zip_cd) VALUES (%s, %s)",
                    (plcy_no, zip_code)
                )
    
    def _insert_major_codes(self, policy: Dict[str, Any]):
        """전공 코드 매핑 테이블에 데이터 삽입"""
        major_codes = policy.get('plcyMajorCd', '').strip()
        if not major_codes:
            return
        
        plcy_no = policy.get('plcyNo')
        
        # 기존 데이터 삭제
        self.cursor.execute(
            "DELETE FROM policy_majors WHERE plcy_no = %s",
            (plcy_no,)
        )
        
        # 새 데이터 삽입
        for major_code in major_codes.split(','):
            major_code = major_code.strip()
            if major_code:
                self.cursor.execute(
                    "INSERT INTO policy_majors (plcy_no, plcy_major_cd) VALUES (%s, %s)",
                    (plcy_no, major_code)
                )
    
    def _insert_job_codes(self, policy: Dict[str, Any]):
        """취업 코드 매핑 테이블에 데이터 삽입"""
        job_codes = policy.get('jobCd', '').strip()
        if not job_codes:
            return
        
        plcy_no = policy.get('plcyNo')
        
        # 기존 데이터 삭제
        self.cursor.execute(
            "DELETE FROM policy_jobs WHERE plcy_no = %s",
            (plcy_no,)
        )
        
        # 새 데이터 삽입
        for job_code in job_codes.split(','):
            job_code = job_code.strip()
            if job_code:
                self.cursor.execute(
                    "INSERT INTO policy_jobs (plcy_no, job_cd) VALUES (%s, %s)",
                    (plcy_no, job_code)
                )
    
    def _insert_school_codes(self, policy: Dict[str, Any]):
        """학력 코드 매핑 테이블에 데이터 삽입"""
        school_codes = policy.get('schoolCd', '').strip()
        if not school_codes:
            return
        
        plcy_no = policy.get('plcyNo')
        
        # 기존 데이터 삭제
        self.cursor.execute(
            "DELETE FROM policy_schools WHERE plcy_no = %s",
            (plcy_no,)
        )
        
        # 새 데이터 삽입
        for school_code in school_codes.split(','):
            school_code = school_code.strip()
            if school_code:
                self.cursor.execute(
                    "INSERT INTO policy_schools (plcy_no, school_cd) VALUES (%s, %s)",
                    (plcy_no, school_code)
                )
    
    def _log_api_call(self, api_url: str, call_time: datetime, response_code: int = 0,
                      total_count: int = 0, processed_count: int = 0, error_count: int = 0,
                      error_message: str = None, execution_time: float = 0):
        """API 호출 로그 저장"""
        try:
            sql = """
            INSERT INTO api_call_logs (
                api_url, call_time, response_code, total_count, processed_count,
                error_count, error_message, execution_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(sql, (
                api_url, call_time, response_code, total_count, processed_count,
                error_count, error_message, execution_time
            ))
            self.connection.commit()
        except Exception as e:
            logger.error(f"API 호출 로그 저장 실패: {e}")
    
    def _parse_datetime(self, date_string: str) -> Optional[datetime]:
        """날짜 문자열을 datetime 객체로 변환"""
        if not date_string or date_string.strip() == '':
            return None
        
        try:
            # '2025-07-15 17:31:15' 형식 처리
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                # '20250715' 형식 처리
                return datetime.strptime(date_string, '%Y%m%d')
            except ValueError:
                logger.warning(f"날짜 형식 파싱 실패: {date_string}")
                return None
    
    def _parse_int(self, value: str) -> Optional[int]:
        """문자열을 정수로 변환"""
        if not value or value.strip() == '':
            return None
        
        try:
            return int(value)
        except ValueError:
            return None
    
    def get_policy_statistics(self) -> Dict[str, Any]:
        """정책 통계 조회"""
        stats = {}
        
        try:
            # 총 정책 수
            self.cursor.execute("SELECT COUNT(*) FROM youth_policies")
            stats['total_policies'] = self.cursor.fetchone()[0]
            
            # 분류별 정책 수
            self.cursor.execute("""
                SELECT lclsf_nm, COUNT(*) as count 
                FROM youth_policies 
                WHERE lclsf_nm IS NOT NULL 
                GROUP BY lclsf_nm 
                ORDER BY count DESC
            """)
            stats['by_category'] = dict(self.cursor.fetchall())
            
            # 지역별 정책 수
            self.cursor.execute("""
                SELECT COUNT(DISTINCT pr.zip_cd) as region_count,
                       COUNT(DISTINCT pr.plcy_no) as policy_count
                FROM policy_regions pr
            """)
            region_stats = self.cursor.fetchone()
            stats['regions'] = {
                'total_regions': region_stats[0],
                'total_policies': region_stats[1]
            }
            
            # 최근 업데이트 정책
            self.cursor.execute("""
                SELECT plcy_nm, last_mdfcn_dt 
                FROM youth_policies 
                ORDER BY last_mdfcn_dt DESC 
                LIMIT 5
            """)
            stats['recent_updates'] = self.cursor.fetchall()
            
        except Exception as e:
            logger.error(f"통계 조회 실패: {e}")
            
        return stats
    
    def search_policies(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """정책 검색"""
        conditions = []
        values = []
        
        # 검색 조건 구성
        if search_params.get('keyword'):
            conditions.append("""
                (plcy_nm LIKE %s OR plcy_expln_cn LIKE %s OR plcy_sprt_cn LIKE %s)
            """)
            keyword = f"%{search_params['keyword']}%"
            values.extend([keyword, keyword, keyword])
        
        if search_params.get('category'):
            conditions.append("lclsf_nm = %s")
            values.append(search_params['category'])
        
        if search_params.get('min_age'):
            conditions.append("(sprt_trgt_min_age IS NULL OR sprt_trgt_min_age <= %s)")
            values.append(search_params['min_age'])
        
        if search_params.get('max_age'):
            conditions.append("(sprt_trgt_max_age IS NULL OR sprt_trgt_max_age >= %s)")
            values.append(search_params['max_age'])
        
        if search_params.get('region'):
            conditions.append("""
                plcy_no IN (
                    SELECT plcy_no FROM policy_regions WHERE zip_cd = %s
                )
            """)
            values.append(search_params['region'])
        
        # 기본 쿼리
        base_query = """
            SELECT plcy_no, plcy_nm, plcy_expln_cn, lclsf_nm, mclsf_nm,
                   sprvsn_inst_cd_nm, aply_ymd, frst_reg_dt
            FROM youth_policies
        """
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # 정렬 및 제한
        base_query += " ORDER BY frst_reg_dt DESC"
        
        if search_params.get('limit'):
            base_query += f" LIMIT {search_params['limit']}"
        
        try:
            self.cursor.execute(base_query, values)
            
            # 결과를 딕셔너리 형태로 변환
            columns = [desc[0] for desc in self.cursor.description]
            results = []
            
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        except Exception as e:
            logger.error(f"정책 검색 실패: {e}")
            return []

def main():
    """메인 실행 함수"""
    # 데이터베이스 연결 설정
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'youth_policy_db',
        'port': 3306
    }

    db_config = Config.DB_CONFIG
    logger.info(f"db_config는 {db_config}.")


    # API URL 설정
    # api_url = "https://www.youthcenter.go.kr/cmnFooter/testbed"
    api_url = Config.API_CONFIG['base_url']


    # 데이터베이스 매니저 초기화
    db_manager = YouthPolicyDBManager(db_config)
    
    try:
        # 데이터베이스 연결
        if not db_manager.connect():
            logger.error("데이터베이스 연결 실패")
            return
        
        # API 파라미터 설정
        params = {
            'apiKeyNm': 'testKey',
            'apiSn': '86',
            'pageNum': 7,
            'pageSize': 100  # 한 번에 가져올 데이터 수
        }

        params['apiKeyNm'] = Config.API_CONFIG['api_key']
        logger.info(f"api_key는 {params['apiKeyNm']}.")

        # 전체 데이터 수집을 위한 루프
        page_num = 1
        total_processed = 0
        
        while True:
            params['pageNum'] = page_num
            
            logger.info(f"페이지 {page_num} 데이터 수집 시작")
            
            # API 데이터 가져오기
            api_data = db_manager.fetch_api_data(api_url, params)
            
            if not api_data or not api_data.get('result', {}).get('youthPolicyList'):
                logger.info("더 이상 가져올 데이터가 없습니다.")
                break
            
            # logger.info(f"api_data: {api_data}")


            # 데이터베이스에 저장
            if db_manager.insert_policy_data(api_data):
                current_count = len(api_data['result']['youthPolicyList'])
                total_processed += current_count
                logger.info(f"페이지 {page_num} 처리 완료: {current_count}건")
            else:
                logger.error(f"페이지 {page_num} 처리 실패")
                break
            
            # 페이징 정보 확인
            pagging = api_data.get('result', {}).get('pagging', {})
            total_count = pagging.get('totCount', 0)
            page_size = pagging.get('pageSize', 100)
            
            if page_num * page_size >= total_count:
                logger.info("모든 데이터 수집 완료")
                break
            
            page_num += 1
            
            # API 호출 간격 (서버 부하 방지)
            time.sleep(10)

            # 한번만 수행.
            # break
        
        # 통계 정보 출력
        stats = db_manager.get_policy_statistics()
        logger.info(f"데이터 수집 완료: 총 {stats.get('total_policies', 0)}건")
        logger.info(f"분류별 정책 수: {stats.get('by_category', {})}")
        
        # 검색 테스트
        search_results = db_manager.search_policies({
            'keyword': '청년',
            'limit': 5
        })
        
        if search_results:
            logger.info(f"검색 결과 샘플 ({len(search_results)}건):")
            for policy in search_results:
                logger.info(f"  - {policy['plcy_nm']} ({policy['lclsf_nm']})")
        
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}")
    
    finally:
        # 데이터베이스 연결 해제
        db_manager.disconnect()

if __name__ == "__main__":
    main()
