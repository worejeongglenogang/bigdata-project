import streamlit as st
import time
import os
from PIL import Image  # 이미지 상태를 확인하기 위해 필요합니다

st.set_page_config(page_title="진행 표시 및 미디어 실습", page_icon="📊")

st.title('📊 Streamlit 진행 표시 및 미디어 실습')

# 1. 상단: 수동 실행 진행바
st.subheader("1. 클릭 시 작동하는 진행바")
if st.button('작업 시작'):
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1)
        time.sleep(0.01)
    st.success('✅ 모든 작업이 완료되었습니다!')

st.divider()

# 2. 중간: 자동 로딩 시뮬레이션
st.subheader("2. 자동 로딩 및 스피너")
status = st.empty() # 메시지용 빈 공간
progress_bar = st.progress(0)

status.write('⏳ 데이터를 로딩 중입니다...')
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)

progress_bar.empty() # 완료 후 바 제거
status.write('✅ 로딩 완료!')

with st.spinner('데이터를 분석하는 중입니다...'):
    time.sleep(2) 
st.success('분석이 끝났습니다!')

st.divider()

# 3. 하단: 미디어 표시 (파일 확인 로직 포함)
st.subheader('🖼️ 미디어 표시 섹션')

# --- 이미지 표시 ---
image_path = "photo.jpg"
if os.path.exists(image_path):
    try:
        # 파일이 실제 이미지인지 확인 시도
        img = Image.open(image_path)
        st.image(img, caption="파일에서 불러온 사진", width='stretch')
    except Exception:
        st.error(f"⚠️ '{image_path}' 파일이 손상되었거나 올바른 이미지 형식이 아닙니다. (그림판으로 새로 저장해 보세요)")
else:
    st.info(f"💡 '{image_path}' 파일이 폴더에 없습니다. 파일을 넣어주세요.")

# --- 오디오 표시 ---
audio_path = "audio.mp3"
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info(f"💡 '{audio_path}' 파일이 없습니다.")

# --- 비디오 표시 ---
video_path = "video.mp4"
if os.path.exists(video_path):
    st.video(video_path)
else:
    st.info(f"💡 '{video_path}' 파일이 없습니다.")

# 4. 효과 애니메이션
st.toast('화면이 성공적으로 로드되었습니다!')
st.balloons() # 풍선 효과
# st.snow() # 눈 효과 (필요하면 주석 해제)