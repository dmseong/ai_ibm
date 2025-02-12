import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from langchain.llms import WatsonxLLM


__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()


api_key = os.environ["API_KEY"]
api_url = os.environ["API_URL"]
project_id = os.environ["PROJECT_ID"]

wml_credentials = {
    "apikey": api_key,
    "url": api_url
}

filename = os.path.join(os.getcwd(), 'data', 'recipes.json')

loader = TextLoader(filename, encoding='UTF8')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

len(texts)

texts[0:9]

embeddings = HuggingFaceEmbeddings()

docsearch = Chroma.from_documents(texts, embeddings)

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY.value,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 500,
    GenParams.STOP_SEQUENCES: ["<|endoftext|>"]
}

model_id =  'ibm/granite-3-8b-instruct' # 'mistralai/mistral-large' # 'meta-llama/llama-3-1-70b-instruct' # ModelTypes.LLAMA_2_70B_CHAT.value #
watsonx_llama2_korean = WatsonxLLM(
    model_id=model_id,
    url=wml_credentials.get("url"),
    apikey=wml_credentials.get("apikey"),
    project_id=project_id,
    params=parameters
)

retriever = docsearch.as_retriever(search_kwargs={'k': 5})

resutls = retriever.get_relevant_documents("두부, 계란으로 만들수 있는 레시피는?")

print(resutls)

from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_input}"),
    ("user", "{user_input}"),
])

chain = chat_prompt | watsonx_llama2_korean

qa = RetrievalQA.from_chain_type(llm=watsonx_llama2_korean, chain_type="stuff", retriever=retriever)

qa.invoke("두부, 계란으로 만들수 있는 레시피는?")