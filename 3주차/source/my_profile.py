import streamlit as st
import pandas as pd
st.title('자기소개')
# 본인 정보 수정하기!
st.write('## 기본정보')
st.write('**이름**: 전건주')
st.write('**학과**: 인공지능소프트웨어학과')
st.write('**학년**: 3학년')
st.write('---') # 구분선
st.write('## 이번 학기 시간표')
schedule = pd.DataFrame({
 '요일': ['월', '화', '수', '목', '금'],
 '1교시': ['-', '-', '-', '-', '-'],
 '2교시': ['-','-','인공지능 라이브러리', '-','자연어처리'],
 '3교시': ['-', '웹프로그래밍', '-', '웹프로그래밍', '-'],
 '4교시': ['-', '자연어 처리', '-', '웹프로그래밍', '-']
})
st.write(schedule)
st.write('---')
st.write('## 관심 분야')
st.write('- 머신러닝')
st.write('- 데이터 시각화')
st.write('- 웹 개발')
st.write('---')
st.write('## 이번 학기 목표')
goals = pd.DataFrame({
 '목표': ['Streamlit 마스터', 'HuggingFace 활용', '포트폴리오 완성'],
 '달성률': [10, 10, 5]
})
st.write(goals)
st.bar_chart(goals.set_index('목표'))