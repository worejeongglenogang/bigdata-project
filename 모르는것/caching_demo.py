import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. 페이지 설정
st.set_page_config(page_title="캐싱 실전", layout="wide")
st.title('⚡ 캐싱 전 vs 후 속도 비교')

# ---- 캐싱 없는 함수 ----
def load_data_slow():
    """매번 2초가 걸리는 데이터 로딩 (캐싱 없음)"""
    time.sleep(2) # 느린 데이터 로딩을 시뮬레이션
    np.random.seed(42)
    return pd.DataFrame({
        '날짜': pd.date_range('2025-01-01', periods=1000),
        '매출': np.random.randint(100, 10000, 1000),
        '카테고리': np.random.choice(['식품', '전자', '의류', '도서'], 1000)
    })

# ---- 캐싱 있는 함수 ----
@st.cache_data(show_spinner="데이터를 불러오는 중...")
def load_data_fast():
    """첫 실행만 2초, 이후는 즉시 반환 (캐싱 있음)"""
    time.sleep(2)
    np.random.seed(42)
    return pd.DataFrame({
        '날짜': pd.date_range('2025-01-01', periods=1000),
        '매출': np.random.randint(100, 10000, 1000),
        '카테고리': np.random.choice(['식품', '전자', '의류', '도서'], 1000)
    })

# ---- 비교 실행 영역 ----
col1, col2 = st.columns(2)

with col1:
    st.subheader('❌ 캐싱 없음')
    # 버튼을 눌렀을 때만 아래 코드들이 실행되도록 '들여쓰기'가 중요합니다.
    if st.button('데이터 로딩 (느림)', key='slow'):
        start_time = time.time()  # 시작 시간 기록
        df = load_data_slow()     # 함수 실행
        elapsed = time.time() - start_time # 소요 시간 계산
        
        st.metric('소요 시간', f'{elapsed:.2f}초')
        st.dataframe(df.head(5))
    else:
        st.write("위 버튼을 눌러보세요.")

with col2:
    st.subheader('✅ 캐싱 있음')
    if st.button('데이터 로딩 (빠름)', key='fast'):
        start_time = time.time()  # 시작 시간 기록
        df = load_data_fast()     # 함수 실행 (캐싱 작동)
        elapsed = time.time() - start_time
        
        st.metric('소요 시간', f'{elapsed:.2f}초')
        st.dataframe(df.head(5))
    else:
        st.write("위 버튼을 눌러보세요.")

st.divider()
st.info('💡 **캐싱 있음** 버전은 첫 번째 클릭 이후부터는 즉시(0.00초) 반환됩니다.')

# ---- 사이드바 조작 영역 ----
st.sidebar.header('⚙️ 필터 조작')
category = st.sidebar.selectbox('카테고리 선택', ['전체', '식품', '전자', '의류', '도서'])
st.sidebar.write(f'현재 선택: **{category}**')
st.sidebar.warning('위 카테고리를 바꿔보세요. 캐싱이 없는 쪽은 페이지가 다시 그려질 때마다 버튼이 풀리며 초기화됩니다.')