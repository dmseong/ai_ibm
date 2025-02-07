import streamlit as st
import requests, json

# 페이지 설정
st.set_page_config(page_title="레시피 추천 챗봇", layout="wide")

# 시스템 폰트와 다크/라이트 모드 대응 CSS 적용
st.markdown(
    """
    <style>
    /* 기본 (라이트 모드) 스타일 */
    body {
        background-color: #f7f9fc;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Segoe UI", Roboto, sans-serif;
        color: #1a1a1a;
    }
    
    /* 메인 제목 스타일 */
    .main-title {
        color: #1a1a1a;
        font-size: 2.8rem;
        text-align: center;
        margin-top: 60px;
        font-weight: bold;
    }
    
    /* 다크 모드 스타일 */
    @media (prefers-color-scheme: dark) {
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        .main-title {
            color: #ffffff;
        }
    }
    
    button[kind="secondary"] {
        display: inline-block;
        justify-content: center;
        padding: 8px;
        border-radius: 16px;
        cursor: pointer;
        width: 12%;
        position: fixed;
        bottom: 115px; 
        transform: translateX(30%);
    }

    button[kind="secondary"]:hover {
        transition: 0.4s;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#세션 상태 변수 초기화
if "messages" not in st.session_state: # 채팅 메시지 기록
    st.session_state.messages = []

if "user_input" not in st.session_state: # 사용자 입력
    st.session_state.question = ""

if "visibility" not in st.session_state: # 제목 & 추천 질문 영역 가시성
    st.session_state.visibility = True

with st.sidebar:
    kcal = st.slider("원하는 칼로리", 10, 2000, 1000)
    st.write("원하는 칼로리는", kcal, "kcal 이하!")
    st.subheader("", divider='grey')

# LLM 호출 함수
def watsonx_ai_api(user_input, kcal):
    payload = {"prompt": user_input, "kcal": kcal}
    try:
        response_data = requests.post("http://localhost:8050/processing", json=payload, timeout=5)
        response_data.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        response = response_data.json()
        if "text" in response:
            return response["text"]
        else:
            return "답변을 가져올 수 없습니다."
    except requests.exceptions.RequestException:
        return "서버와의 연결이 원활하지 않습니다."

# 채팅 메시지 출력 함수
def send_chat_response(user_input, kcal):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # response = "hello" # 임시 답변

    with st.chat_message("assistant"):
        with st.spinner("Making..."):
            response = watsonx_ai_api(user_input, kcal)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 추천 질문 리스트
recommended_questions = [
    "인기 급상승 레시피🔥",
    "초간단 레시피🍽",
    "랜덤 레시피🎲",
]

# 질문이 한 번 들어오면 제목과 추천 질문 가시성을 False로 변경
if st.session_state.visibility:
    st.markdown("<div class='main-title'>레시피 추천 챗봇</div>", unsafe_allow_html=True)
    cols = st.columns(len(recommended_questions))  # 버튼을 가로로 배치
    for i, question in enumerate(recommended_questions):
        if cols[i].button(question):
            st.session_state.question = question
            st.session_state.visibility = False
            send_chat_response(st.session_state.question, kcal)
            st.rerun()

# 저장된 채팅 기록을 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력을 받는 채팅 입력창
prompt = st.chat_input("질문을 입력하세요...")

if prompt:
    st.session_state.question = prompt
    st.session_state.visibility = False
    send_chat_response(st.session_state.question, kcal)
    st.rerun()