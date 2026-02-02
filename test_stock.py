import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# 1. 저장할 경로 설정 (1TB 하드디스크)
save_dir = "/data/quant_project/stock_db"
os.makedirs(save_dir, exist_ok=True)  # 폴더가 없으면 알아서 만듭니다.

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
        file_path = f"{save_dir}/{ticker}.csv"
        df.to_csv(file_path)
        print(f"  ✅ 저장 완료: {file_path}")
    else:
        print(f"  ⚠️ 실패: 데이터를 가져오지 못했습니다.")

print("\n🎉 모든 작업이 끝났습니다. 1TB 창고를 확인해보세요!")