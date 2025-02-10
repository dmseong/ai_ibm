from fastapi import FastAPI, Request, BackgroundTasks
# from routers import 
# CORS 정책
from fastapi.middleware.cors import CORSMiddleware
import os
import os
from fastapi import FastAPI, Form
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from model import Message, PromptMessage

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


def create_llm(api_key, api_url, project_id):
   
   parameters = { 
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY.value,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.STOP_SEQUENCES: ["<|endoftext|>"]
    }
   
   credentials = Credentials(
        url=api_url,
        api_key=api_key
    )

   model_id =  'ibm/granite-3-8b-instruct' # 'mistralai/mistral-large' # 'meta-llama/llama-3-1-70b-instruct' # ModelTypes.LLAMA_2_70B_CHAT.value #
   llm = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=project_id
    ) 
   
   return llm

api_key = os.environ["API_KEY"]
api_url = os.environ["API_URL"]
project_id = os.environ["PROJECT_ID"]


model = create_llm(api_key, api_url, project_id)


@app.post("/processing", description="prompt message",response_model = Message)
def watsonx_ai_api(promptMessage: PromptMessage):
    
    response = model.generate(prompt=promptMessage.prompt)['results'][0]['generated_text'].strip()
    print(response) 
    msg = {"text": response}
    
    return msg