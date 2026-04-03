import streamlit as st
import plotly.express as px
import altair as alt
import pandas as pd
import sys
import os

# ---- [강력한 경로 설정] 어떤 환경에서도 상위 폴더(utils)를 찾도록 합니다 ----
# 1. 현재 이 파일(2_charts.py)의 절대 경로를 가져옵니다.
current_file = os.path.abspath(__file__)
# 2. 이 파일이 들어있는 폴더(pages)를 찾습니다.
pages_dir = os.path.dirname(current_file)
# 3. 그 한 단계 위인 프로젝트 루트(bike_dashboard)를 찾습니다.
root_dir = os.path.dirname(pages_dir)

# 4. 파이썬이 모듈을 찾는 경로(sys.path) 맨 앞에 root_dir을 추가합니다.
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 이제 utils를 불러오면 절대 실패하지 않습니다.
from utils.data_loader import load_bike_data

# ---- 대시보드 UI 시작 ----
st.set_page_config(page_title="따릉이 차트 분석", layout="wide")
st.title('📊 차트 분석')

# 데이터 로드
df = load_bike_data()

# 탭 구성
tab1, tab2, tab3 = st.tabs(['시간대별 패턴', '대여소 비교 (Altair)', '이용시간 분포'])

with tab1:
    st.subheader('시간대별 대여 패턴')
    hourly = df.groupby('시간대')['대여건수'].mean().reset_index()
    hourly.columns = ['시간대', '평균대여건수']
    fig = px.bar(hourly, x='시간대', y='평균대여건수', color='평균대여건수', color_continuous_scale='YlOrRd')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader('대여소별 비교 (Altair 브러시 선택)')
    station_daily = df.groupby(['날짜', '대여소'])['대여건수'].sum().reset_index()
    selected_stations = st.multiselect('비교할 대여소 선택', df['대여소'].unique(), default=list(df['대여소'].unique()[:3]))
    
    if selected_stations:
        chart_data = station_daily[station_daily['대여소'].isin(selected_stations)]
        brush = alt.selection_interval(encodings=['x'])
        upper = alt.Chart(chart_data).mark_line().encode(x='날짜:T', y='대여건수:Q', color='대여소:N').add_params(brush).properties(height=250)
        lower = alt.Chart(chart_data).mark_bar().encode(x='대여소:N', y='mean(대여건수):Q', color='대여소:N').transform_filter(brush).properties(height=200)
        st.altair_chart(upper & lower, use_container_width=True)

with tab3:
    st.subheader('이용 시간 분포')
    fig = px.histogram(df, x='이용시간(분)', nbins=30, marginal='box', color_discrete_sequence=['#a855f7'])
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric('중앙값', f"{df['이용시간(분)'].median():.1f}분")
    c2.metric('평균', f"{df['이용시간(분)'].mean():.1f}분")
    c3.metric('최댓값', f"{df['이용시간(분)'].max():.1f}분")