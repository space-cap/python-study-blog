pip freeze

pip install --upgrade setuptools wheel
pip install matplotlib==3.7.5

pip install pandas==2.0.3

pip install yfinance
pip install pandas-datareader
pip install --upgrade yfinance pandas_datareader

32bit scipy를 설치를 하고 싶으면
32bit 가상화를 만들고 scipy 1.9.1 를 먼저 설치를 해 주자.
만약 회사에서 작업한다면 회사에서 사용하는 가상화를 따로 만들어 주자.
집, 회사 각각 하나씩 가상화. 소스는 같이 사용을 해도 된다.
pip install scipy==1.9.1
pip install pandas
pip install matplotlib
pip install yfinance
pip install pandas-datareader
pip install pymysql
pip install SQLAlchemy
pip install python-dotenv
pip install dart-fss
pip install backtrader
pip install slacker
pip install slack_sdk
pip install mplfinance
pip install pywinauto
pip install selenium

파이썬 3.8.10 32비트 설치
https://www.python.org/downloads/release/python-3810/
Windows installer (32-bit) 다운 받아서 설치

챕터 09 를 하기 위해서는 64비트를 설치를 해야 한다.
C:\Python\Python38\python.exe -m venv Py3810_64

pip install tensorflow
pip install matplotlib
pip install scipy
pip install pandas
pip install yfinance
pip install backtrader
