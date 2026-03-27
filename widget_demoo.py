# slider_demo.py
import streamlit as st
st.title('위젯 실습 - slider')
# 기본 슬라이더
age = st.slider('나이를 선택하세요', 0, 100, 25)
st.write(f'선택한 나이: {age}세')
# 범위 슬라이더 (튜플 반환)
price_range = st.slider(
 '가격 범위를 설정하세요',
 min_value=0,
 max_value=100000,
 value=(20000, 80000), # 기본값을 튜플로 주면 범위 슬라이더
 step=5000,
 format='₩%d'
)
st.write(f'선택 범위: ₩{price_range[0]:,} ~ ₩{price_range[1]:,}')