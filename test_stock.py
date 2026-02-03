import yfinance as yf
import pandas as pd
import os
from datetime import datetime


# [수정 후] - 어디서든 작동 (Portable)
# 1. 현재 이 파일(test_stock.py)의 위치를 알아냄
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. 그 위치 안에 있는 'stock_db' 폴더를 저장소로 지정
SAVE_DIR = os.path.join(CURRENT_DIR, "stock_db")

# 3. 만약 폴더가 없으면 알아서 만듦 (자동화)
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 2. 사용자님의 보유 종목 리스트
my_tickers = {
    "MBLY": "Mobileye",
    "SMR": "NuScale Power",
    "CPNG": "Coupang"
}

print(f"[{datetime.now()}] 데이터 수집을 시작합니다...\n")

for ticker, name in my_tickers.items():
    print(f"🚀 {name} ({ticker}) 데이터를 가져오는 중...")
    
    # 데이터 다운로드 (최근 1년치)
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    
    # 데이터가 비어있지 않다면 저장
    if not df.empty:
        # 파일명: 종목코드_수집날짜.csv
        file_path = f"{SAVE_DIR}/{ticker}.csv"
        df.to_csv(file_path)
        print(f"  ✅ 저장 완료: {file_path}")
    else:
        print(f"  ⚠️ 실패: 데이터를 가져오지 못했습니다.")

print("\n🎉 모든 작업이 끝났습니다. 1TB 창고를 확인해보세요!")