import streamlit as st
import ollama

st.set_page_config(page_title="Ollama 챗봇", page_icon="🤖")
st.title("🤖 Ollama 챗봇")

# ── 1. 대화 기록 초기화 ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 2. 기존 대화 기록 표시 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 3. 사용자 입력 처리 ──
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 메시지를 기록에 추가 & 화면에 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # ── 4. Ollama에 전체 대화 기록 전달 ──
    with st.chat_message("assistant"):
        with st.spinner("생각하는 중..."):
            try:
                response = ollama.chat(
                    model="gemma3:4b",
                    messages=st.session_state.messages
                )
                
                # 라이브러리 버전에 따라 dict 또는 객체 형태이므로 안전하게 추출
                if hasattr(response, 'message'):
                    assistant_reply = response.message.content
                else:
                    assistant_reply = response["message"]["content"]
                
                st.write(assistant_reply)

                # ── 5. AI 응답을 기록에 추가
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")