import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title='기초 EDA 대시보드', layout='wide')

st.title('📊 기초 EDA 대시보드')

# 2. 데이터 생성
@st.cache_data
def load_data():
    np.random.seed(42)
    data = pd.DataFrame({
        '날짜': pd.date_range('2026-01-01', periods=100),
        '카테고리': np.random.choice(['전자제품', '의류', '식품'], 100),
        '매출': np.random.randint(100, 1000, 100),
        '고객수': np.random.randint(10, 200, 100),
        '전환율': np.random.uniform(0.01, 0.20, 100).round(4)
    })
    # [핵심 수정] .dt.date를 붙여서 pyarrow 에러를 방지합니다.
    data['날짜'] = pd.to_datetime(data['날짜']).dt.date
    return data

df = load_data()

# 3. 사이드바 필터
st.sidebar.header('🔍 필터 설정')
selected_category = st.sidebar.selectbox('카테고리 선택', ['전체'] + list(df['카테고리'].unique()))
data_range = st.sidebar.slider('데이터 표시 일수', 10, 100, 50, 10)

# 4. 데이터 필터링
filtered_df = df.head(data_range).copy()
if selected_category != '전체':
    filtered_df = filtered_df[filtered_df['카테고리'] == selected_category]

st.sidebar.write('---')
st.sidebar.write(f'✅ 필터링된 데이터: **{len(filtered_df)}행**')

# 5. 메인 화면 구성
tab1, tab2 = st.tabs(['📈 요약 대시보드', '📄 원본 데이터'])

with tab1:
    st.subheader('핵심 지표 (KPI)')
    k1, k2, k3 = st.columns(3)
    k1.metric('총 매출', f"₩{filtered_df['매출'].sum():,}만")
    k2.metric('총 고객수', f"{filtered_df['고객수'].sum():,}명")
    k3.metric('평균 전환율', f"{filtered_df['전환율'].mean():.2%}")
    
    st.write('---')
    st.subheader('일별 매출 추이')
    # 차트 데이터 생성 시에도 날짜가 인덱스로 잘 가도록 설정
    chart_data = filtered_df.groupby('날짜')['매출'].sum()
    st.line_chart(chart_data)

with tab2:
    st.subheader('데이터 상세 보기')
    st.dataframe(filtered_df, use_container_width=True, height=400)
    with st.expander('📊 데이터 통계 요약 보기'):
        st.write(filtered_df.describe())