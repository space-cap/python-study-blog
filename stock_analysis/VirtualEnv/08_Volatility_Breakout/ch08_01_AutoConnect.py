from pywinauto import application
import time
import os
from dotenv import load_dotenv


# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
CREON_USER = os.getenv('CREON_USER')
CREON_PWD = os.getenv('CREON_PWD')
CREON_PWDCERT = os.getenv('CREON_PWDCERT')

os.system('taskkill /IM coStarter* /F /T')
os.system('taskkill /IM CpStart* /F /T')
os.system('taskkill /IM DibServer* /F /T')
os.system('wmic process where "name like \'%coStarter%\'" call terminate')
os.system('wmic process where "name like \'%CpStart%\'" call terminate')
os.system('wmic process where "name like \'%DibServer%\'" call terminate')
time.sleep(5)        

cmd_line = f"C:\CREON\STARTER\coStarter.exe /prj:cp /id:{CREON_USER} /pwd:{CREON_PWD} /pwdcert:{CREON_PWDCERT} /autostart"
app = application.Application()
app.start(cmd_line)
time.sleep(60)
