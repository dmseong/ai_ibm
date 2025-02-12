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

credentials = {
    "url" : api_url,
    "apikey": api_key,
}

@app.post("/api/processing", description="prompt message",response_model = Message)
def watsonx_ai_test1(promptMessage: PromptMessage):
    
    print(promptMessage)
    
    input = """
    Context : 삼중따옴표로 구분된 텍스트가 제공됩니다. 아래의 규칙을 지켜 답변해주세요.
    
    - 질문에 대한 답을 한국어로 답변해주세요.  
    - 질문 내용을 답변에 포함하지 말아주세요.  
    - 절대 같은 말을 반복하여 답변하지 말아주세요.
    - 통곡물과 채소 중심으로 구성된 건강한 식단의 레시피를 추천해주세요.  
    - 제공된 kcal 이하의 레시피만 추천해주세요.   
    - 재료 손질 및 조리 과정에서 불필요한 반복을 제거하고, 자연스럽고 정확한 문장을 사용해주세요.  
    - 예시를 그대로 출력하는 것과 예시의 조리 과정에서 재료만 바꾸어 출력하는 것은 금지됩니다.
    - 같은 레시피가 반복되지 않도록 새로운 조리법을 제안해주세요.
    - 해당 레시피가 저속노화 식단에 적합한 이유를 마지막에 설명해주세요.
    - 주어진 재료를 최대한 활용하여 레시피를 작성해주세요. 사용된 재료는 중복 없이 모두 포함되어야 하며, 불필요한 재료는 배제해주세요.
    - 한 번에 하나의 레시피만 생성해주세요.
    - 건강하지 못한 재료가 주어진다면, 레시피를 제공하지 않고 예제 3번의 출력 형식을 참고하여 해당 사실을 설명해주세요.
    - 반드시 코드 블록을 사용하지 않고 텍스트 형식으로만 제공해주세요.
    - 반드시 레시피를 끝까지 작성해주세요.
    - 위 규칙들을 모두 지킬 시 100불의 팁이 주어집니다.
    
    출력 형식:
        **레시피 이름:** (요리 이름)
        
    **재료:** 재료1, 재료2, 재료3, ...  

    **칼로리:** 약 (해당 레시피의 칼로리)kcal

    **조리 과정:**
    1. (조리 과정 1)
    2. (조리 과정 2)
    3. (조리 과정 3)
    ...

    **저속노화 식단인 이유:**  
    - (해당 레시피가 저속노화에 기여하는 이유를 설명)  
    - (사용된 주요 재료의 항산화 효과, 항염 효과, 혈당 조절, 심혈관 건강 기여 등 관련 정보를 포함) 

    

    예시 1 :
        입력 : 연어, 렌틸콩으로 만들 수 있는 요리 알려줘
        
        **레시피 제목:** 연어 렌틸콩 스튜  

    **재료:** 연어 150g, 렌틸콩 100g, 당근 1개, 양파 1/2개, 마늘 2쪽, 토마토 1개, 올리브 오일 1작은술, 소금 1/2작은술, 후추 약간, 채소 육수 200ml  
    
    **칼로리:** 약 540kcal

    **조리 과정:**  
    1. 렌틸콩을 씻어 끓는 물에 15분간 삶은 후 체에 밭쳐 물기를 제거한다.  
    2. 냄비에 올리브 오일을 두르고, 다진 마늘과 양파를 볶아 향을 낸다.  
    3. 당근과 토마토를 깍둑썰기하여 냄비에 넣고 5분간 볶는다.  
    4. 채소 육수와 삶은 렌틸콩을 넣고 중불에서 10분간 끓인다.  
    5. 연어를 큼직하게 썰어 넣고 5분간 더 끓인다.  
    6. 소금과 후추로 간을 맞추고, 그릇에 담아 완성한다.

    **저속노화 식단인 이유:**  
    - **연어**: 오메가-3 지방산이 풍부하여 항염 작용을 돕고, 세포 노화를 늦추는 데 기여함.  
    - **렌틸콩**: 식이섬유와 단백질이 풍부하여 혈당을 조절하고 장 건강을 지원함.  
    - **당근 & 토마토**: 항산화 성분(베타카로틴, 라이코펜)이 풍부하여 세포 손상을 예방하고 면역력을 높임.  
    - **올리브 오일**: 건강한 지방이 포함되어 있어 심혈관 건강을 돕고 노화 속도를 늦추는 데 도움을 줌.  
    

    예시 2 :
        입력 : 잡곡, 계란으로 만들 수 있는 요리 알려줘
        
        **레시피 제목:** 잡곡 계란 볶음밥

    **재료:** 잡곡밥 1공기, 계란 2개, 양파 1/2개, 당근 1/2개, 파프리카 1/2개, 마늘 2쪽, 올리브 오일 1작은술, 소금 1/2작은술, 후추 약간, 간장 1작은술, 참기름 1작은술
    
    **칼로리:** 약 400kcal

    **조리 과정:**
    1. 잡곡밥을 미리 지어 준비한다.
    2. 양파, 당근, 파프리카를 잘게 썰고, 마늘은 다진다.
    3. 팬에 올리브 오일을 두르고 마늘을 볶아 향을 낸 후, 양파와 당근을 넣고 2분 정도 볶는다.
    4. 파프리카를 넣고 1분 정도 볶은 후, 잡곡밥을 넣고 잘 섞어준다.
    5. 다른 팬에서 계란을 풀어 스크램블 에그를 만든 후, 볶음밥에 섞어준다.
    6. 간장, 소금, 후추로 간을 맞추고, 마지막에 참기름을 넣어 풍미를 더한다.
    7. 그릇에 담아 완성한다.

    **저속노화 식단인 이유:**
    - **잡곡밥:** 식이섬유와 비타민, 미네랄이 풍부하여 장 건강을 돕고 혈당 조절에 유익하다.
    - **계란:** 단백질이 풍부하고, 비타민 B군이 포함되어 세포 회복과 노화 방지에 기여한다.
    - **당근 & 파프리카:** 항산화 성분(베타카로틴, 비타민 C)이 풍부하여 면역력 강화와 세포 손상 예방에 도움이 된다.
    - **올리브 오일 & 참기름:** 건강한 지방이 포함되어 심혈관 건강을 돕고 노화 속도를 늦춘다.
    

    예시 3 :
        입력: 사탕으로 만들 수 있는 요리 알려줘
        
    죄송합니다. 주어진 재료로 건강한 레시피를 만들 수 없습니다. 다른 재료를 이용하여 다시 시도해주세요😢
        
    """
    
    prompt = f"""
    ```{promptMessage}```
    
    
    {input}
    """
    
    response = send_to_watsonxai(prompts=[prompt], model_name="ibm/granite-3-8b-instruct", decoding_method="greedy", max_new_tokens=1000,
                              min_new_tokens=1, temperature=1, repetition_penalty=1.0)
    
    msg = {"text": response[0]}

    return msg

def send_to_watsonxai(prompts,
                    model_name,
                    decoding_method="greedy",
                    max_new_tokens=100,
                    min_new_tokens=30,
                    temperature=1.0,
                    repetition_penalty=1.0,
                    stop_sequence=['\n\n']
                    ):

    assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "make sure none of the prompts in the inputs prompts are empty"

    # Instantiate parameters for text generation
    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
    }
    
    # Instantiate a model proxy object to send your requests
    model = ModelInference(
        model_id=model_name,
        params=model_params,
        credentials=credentials,
        project_id=project_id)

    response = model.generate_text(prompt = prompts)

    return response  

