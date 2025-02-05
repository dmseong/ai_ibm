import streamlit as st

# 페이지 설정
st.set_page_config(page_title="책 지피티 - 주변 도서 안내 도우미", layout="wide")

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
    
    /* 추천 질문 영역 스타일 */
    .recommendation {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 30px 40px;
        text-align: center;
        margin: 40px auto;
        max-width: 600px;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .recommendation strong {
        display: block;
        font-size: 1.2rem;
        margin-bottom: 20px;
        color: #333;
    }
    .recommendation ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .recommendation ul li {
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
        cursor: pointer;
    }
    .recommendation ul li:last-child {
        border-bottom: none;
    }
    
    /* 하단 채팅 입력창 스타일 */
    .chat-input {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 600px;
    }
    .chat-input input[type="text"] {
        width: 100%;
        padding: 15px 20px;
        border: 1px solid #e0e0e0;
        border-radius: 25px;
        font-size: 1rem;
        outline: none;
        transition: all 0.3s ease;
        background-color: #ffffff;
        color: #1a1a1a;
    }
    .chat-input input[type="text"]:focus {
        border-color: #0070f3;
        box-shadow: 0 0 8px rgba(0, 112, 243, 0.2);
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
        .recommendation {
            background-color: #1e1e1e;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
        }
        .recommendation strong {
            color: #e0e0e0;
        }
        .recommendation ul li {
            border-bottom: 1px solid #333;
        }
        .chat-input input[type="text"] {
            background-color: #1e1e1e;
            border: 1px solid #333;
            color: #e0e0e0;
        }
        .chat-input input[type="text"]:focus {
            border-color: #66b0ff;
            box-shadow: 0 0 8px rgba(102, 176, 255, 0.2);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 메인 제목 출력
st.markdown("<div class='main-title'>책 지피티 - 주변 도서 안내 도우미</div>", unsafe_allow_html=True)

# 추천 질문 리스트
recommended_questions = [
    "가장 인기 있는 도서는 무엇인가요?",
    "최근 출간된 도서 추천 부탁해요.",
    "특정 주제에 관한 도서가 있을까요?"
]

# 추천 질문 영역 출력 (내부에 질문 리스트가 포함됨)
st.markdown(
    f"""
    <div class="recommendation">
        <strong>추천 질문</strong>
        <ul>
            {"".join(f"<li>{question}</li>" for question in recommended_questions)}
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# 하단 채팅 입력창 (고정 위치)
st.markdown(
    """
    <div class="chat-input">
        <form action="#" method="get">
            <input type="text" name="user_input" placeholder="채팅을 입력하세요...">
        </form>
    </div>
    """,
    unsafe_allow_html=True,
)