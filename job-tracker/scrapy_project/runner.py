import subprocess
import sys
import os
import threading

def run_spider(url=None):
    """FastAPI와 호환되는 방식으로 Scrapy 스파이더를 실행하는 함수
    
    Args:
        url (str, optional): 크롤링할 특정 URL. 제공되지 않으면 기본 URL들 사용
    """
    
    def run_crawling_subprocess():
        try:
            # 현재 디렉토리에서 scrapy 명령어로 크롤링 실행
            cmd = [
                sys.executable, '-m', 'scrapy', 'crawl', 'saramin',
                '-L', 'INFO'  # 로그 레벨 설정
            ]
            
            # URL이 제공된 경우 파라미터로 전달
            if url:
                cmd.extend(['-a', f'target_url={url}'])
                print(f"크롤링 시작: {url}")
            else:
                print("기본 URL들로 크롤링 시작")
            
            print(f"실행 명령어: {' '.join(cmd)}")
            
            # 별도 프로세스에서 크롤링 실행
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=60  # 60초 타임아웃
            )
            
            print(f"크롤링 완료 - 반환 코드: {process.returncode}")
            if process.stdout:
                print(f"표준 출력: {process.stdout}")
            if process.stderr:
                print(f"표준 에러: {process.stderr}")
                
        except subprocess.TimeoutExpired:
            print("크롤링이 타임아웃되었습니다.")
        except Exception as e:
            print(f"크롤링 실행 중 오류: {e}")
            import traceback
            traceback.print_exc()
    
    # 별도 스레드에서 크롤링 실행
    thread = threading.Thread(target=run_crawling_subprocess)
    thread.daemon = True
    thread.start()
    
    print("크롤링이 백그라운드에서 시작되었습니다.")