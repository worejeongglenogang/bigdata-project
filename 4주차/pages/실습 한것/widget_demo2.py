import streamlit as st  # 이 줄이 반드시 있어야 합니다!
import time

placeholder = st.empty() 
for i in range(10, 0, -1):
    placeholder.write(f'카운트다운: {i}') 
    time.sleep(0.5)
placeholder.write('발사!')