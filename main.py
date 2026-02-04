import pandas as pd
import os
import sys

# 1. 설정 (Configuration)
TICKERS = ['CPNG', 'SMR', 'MBLY']  # 분석할 종목 리스트
DB_PATH = 'stock_db'

def load_data(ticker):
    """데이터를 불러오고 전처리하는 함수 (ETL)"""
    file_path = os.path.join(DB_PATH, f'{ticker}.csv')
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    return df

def calculate_indicators(df):
    """보조지표 계산 모듈"""
    # 이동평균선
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA60'] = df['Close'].rolling(window=60).mean() # 추세 필터용

    # RSI (14일)
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def analyze_rsi_strategy(today):
    """전략 1: RSI 역추세 (변동성 종목용)"""
    price = today['Close']
    rsi = today['RSI']
    ma5 = today['MA5']
    
    # 매수: RSI가 40 미만이고 + 5일선 위에 있을 때 (반등 확인)
    if rsi < 40 and price > ma5:
        return "BUY 🚀"
    # 매도: RSI가 70 초과 (과열)
    elif rsi > 70:
        return "SELL 💰"
    # 그 외: 관망
    else:
        return "WAIT ✋"

def analyze_trend_strategy(today, yesterday):
    """전략 2: 골든크로스 + 추세 필터 (추세 종목용)"""
    # 골든크로스: 어제는 5일선이 20일선 아래, 오늘은 위
    golden_cross = (yesterday['MA5'] < yesterday['MA20']) and (today['MA5'] > today['MA20'])
    # 데드크로스: 어제는 위, 오늘은 아래
    dead_cross = (yesterday['MA5'] > yesterday['MA20']) and (today['MA5'] < today['MA20'])
    
    # 추세 필터: 현재가가 60일선보다 위에 있는가? (상승장 확인)
    trend_ok = today['Close'] > today['MA60']

    if golden_cross and trend_ok:
        return "BUY 🚀 (Trend)"
    elif dead_cross:
        return "SELL 📉 (Trend)"
    else:
        return "WAIT ✋"

def main():
    print("="*80)
    print(f"{'Ticker':<6} | {'Price':<8} | {'RSI':<5} | {'MA60':<8} | {'RSI 전략 (단기)':<15} | {'추세 전략 (장기)':<15}")
    print("="*80)

    for ticker in TICKERS:
        df = load_data(ticker)
        if df is None:
            print(f"{ticker:<6} | Data Not Found")
            continue

        df = calculate_indicators(df)
        
        # 오늘과 어제 데이터 추출 (최신 데이터)
        if len(df) < 60: # 데이터 부족 시 패스
            print(f"{ticker:<6} | Not Enough Data")
            continue
            
        today = df.iloc[-1]
        yesterday = df.iloc[-2]
        
        # 전략 분석 실행
        rsi_action = analyze_rsi_strategy(today)
        trend_action = analyze_trend_strategy(today, yesterday)
        
        # 결과 출력
        print(f"{ticker:<6} | ${today['Close']:<7.2f} | {today['RSI']:<5.1f} | ${today['MA60']:<7.2f} | {rsi_action:<15} | {trend_action:<15}")

    print("="*80)
    print("💡 Tip: SMR 같은 변동성 종목은 'RSI 전략'을, CPNG/MBLY 같은 추세 종목은 '추세 전략'을 참고하세요.")

if __name__ == "__main__":
    main()