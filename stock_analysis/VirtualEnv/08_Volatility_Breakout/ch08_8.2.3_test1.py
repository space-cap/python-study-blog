import ctypes
import win32com.client

# 8.2.3 크레온 시스템 접속 체크

# 크레온 플러스 공통 OBJECT
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos') # 시스템 상태 정보
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil') # 주문 관련 도구

# creon plus 시스템 점검 함수
def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_system() : admin user -> FAILED')
        return False
 
    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        print('check_creon_system() : connect to server -> FAILED')
        return False
    
    # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    if (cpTradeUtil.TradeInit(0) != 0):
        print('check_creon_system() : init trade -> FAILED')
        return False
    
    return True

result = check_creon_system()
print(result)
