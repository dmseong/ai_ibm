from fastapi import FastAPI, Request, BackgroundTasks
# from routers import 
# CORS 정책
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv

# swagger 페이지 소개
SWAGGER_HEADERS = {
    "title": "ai_ibm 관리 페이지",
    "version": "1.0.0",
    "description": "## 관리페이지에 오신것을 환영합니다 \n - 무분별한 사용은 하지 말아주세요 \n - 관리자 번호: 010-1234-5678",
    "contact": {
       "name": "ai_ibm",
       "url": "https://localhost"
    },
    
}


# 환경변수 이용을 위한 전역변수
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI(**SWAGGER_HEADERS)

# CROS 허용 ip
origins = [
   os.environ['FRONTEND_URL'],
]

#api설정값
app.add_middleware(
    CORSMiddleware,
    # 허용 ip
    #allow_origins=origins,
    #일단 열어둠
    allow_origins=["*"],
    # 인증, 쿠키
    #allow_credentials=True,
    # 허용 메소드
    allow_methods=["GET","POST","PUT","DELETE"],
    # 허용 헤더
    allow_headers=["*"],  
)

@app.get("/")
def helloworld():
    return {"Hello World"}