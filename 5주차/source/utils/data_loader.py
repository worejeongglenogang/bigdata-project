# utils/data_loader.py
import streamlit as st
import pandas as pd
import numpy as np
@st.cache_data(ttl="1h", show_spinner="데이터를 불러오는 중...")
# ttl="1h" → 1시간 후 캐시 만료, 다시 로딩
# show_spinner="..." → 첫 로딩 시 사용자에게 보여줄 메시지
def load_bike_data():
 """따릉이 이용 데이터 로딩 (시뮬레이션)"""
 np.random.seed(42)
 n = 5000
 stations = ['여의도역', '강남역', '홍대입구', '서울역', '잠실역',
 '신촌역', '합정역', '건대입구', '왕십리역', '이태원역']
 dates = pd.date_range('2025-01-01', periods=90)
 data = {
 '날짜': np.random.choice(dates, n),
 '대여소': np.random.choice(stations, n),

 '시간대': np.random.choice(range(0, 24), n),
 # np.random.poisson(lam=15) → 평균 15건인 포아송 분포로 난수 생성
 # 포아송 분포: "일정 시간에 평균 N번 발생하는 사건" 모델링에 사용
 # (예: 1시간에 평균 15건의 대여가 발생)
 '대여건수': np.random.poisson(lam=15, size=n),
 '반납건수': np.random.poisson(lam=14, size=n),
 # np.random.exponential(scale=25) → 평균 25분인 지수 분포로 난수 생성
 # 지수 분포: "대기 시간/이용 시간" 모델링에 사용 (짧은 시간이 많고, 긴 시간은드문 분포)
 '이용시간(분)': np.random.exponential(scale=25, size=n).astype(int) + 5
 }
 df = pd.DataFrame(data)
 df['날짜'] = pd.to_datetime(df['날짜'])
 df = df.sort_values(['날짜', '시간대']).reset_index(drop=True)
 return df
@st.cache_data
def get_station_summary(df):
 """대여소별 요약 통계"""
 # .groupby('대여소') → 대여소별로 데이터를 그룹으로 나눔
 # .agg() → 각 그룹에 대해 집계(합계, 평균 등) 수행
 # 이름 지정 집계: 새컬럼명=('원본컬럼', '집계함수')
 summary = df.groupby('대여소').agg(
 총대여건수=('대여건수', 'sum'), # 대여건수의 합계
 총반납건수=('반납건수', 'sum'), # 반납건수의 합계
 평균이용시간=('이용시간(분)', 'mean'), # 이용시간의 평균
 일평균대여=('대여건수', lambda x: x.sum() / df['날짜'].nunique())
 # ↑ lambda: 커스텀 계산 (총 대여건수 ÷ 전체 날짜 수 = 일 평균)
 ).round(1).reset_index()
 # .round(1) → 소수점 1자리로 반올림
 # .reset_index() → groupby로 인덱스가 된 '대여소'를 다시 일반 컬럼으로
 return summary
