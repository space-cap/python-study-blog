import pandas as pd
import numpy as np
import tensorflow as tf
from pykrx import stock
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta

# 삼성전자 종목 코드
ticker = '005930'

days = 365
today = datetime.today()
start_date = (today - timedelta(days=days)).strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')



