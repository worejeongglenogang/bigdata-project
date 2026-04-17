import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="한국어 AI 챗봇", page_icon="🇰🇷")
st.title("🇰🇷 HuggingFace 한국어 텍스트 생성 챗봇")
st.caption("skt/ko-gpt-trinity-1.2B-v0.5 모델 사용")

# ── 모델 로딩 (캐싱) ──
@st.cache_resource
def load_model():
    # 모델 로딩 시도 (CPU 모드)
    return pipeline(
        "text-generation",
        model="skt/ko-gpt-trinity-1.2B-v0.5",
        device=-1  # -1은 CPU를 의미합니다.
    )

with st.spinner("모델 로딩 중... (최초 1회만 소요되며 용량이 큽니다)"):
    try:
        generator = load_model()
    except Exception as e:
        st.error(f"모델 로딩 실패: {e}")
        st.stop()

# ── 사이드바 설정 ──
with st.sidebar:
    st.header("⚙ 생성 설정")
    max_tokens = st.slider("최대 생성 토큰", 50, 300, 150)
    temperature = st.slider("Temperature", 0.1, 1.5, 0.7, 0.1)
    rep_penalty = st.slider("반복 방지 강도", 1.0, 2.0, 1.2, 0.1)

    st.divider()
    if st.button("🗑 대화 초기화", use_container_width=True):
        st.session_state.hf_messages = []
        st.rerun()

# ── 대화 기록 초기화 ──
if "hf_messages" not in st.session_state:
    st.session_state.hf_messages = []

# 기존 대화 표시
for msg in st.session_state.hf_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 처리 ──
user_input = st.chat_input("문장을 입력하면 AI가 이어서 작성합니다")

if user_input:
    # 1. 사용자 메시지 기록 및 표시
    st.session_state.hf_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. AI 답변 생성
    with st.chat_message("assistant"):
        with st.spinner("텍스트 생성 중..."):
            try:
                result = generator(
                    user_input,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    repetition_penalty=rep_penalty
                )
                generated = result[0]["generated_text"]

                # 입력 텍스트 이후의 생성된 부분만 추출
                if generated.startswith(user_input):
                    new_text = generated[len(user_input):].strip()
                else:
                    new_text = generated.strip()

                if not new_text:
                    new_text = "(생성된 결과가 없습니다. 다시 입력해주세요.)"

                st.write(new_text)
                st.session_state.hf_messages.append({"role": "assistant", "content": new_text})
                
            except Exception as e:
                st.error(f"생성 중 오류 발생: {e}")