# OpenAI API를 활용한 벡터 데이터 생성 예시

from typing import List, Dict
import openai
from environ import Env

env = Env()
env.read_env(overwrite=True)  # .env 파일을 환경변수로 로딩합니다.

def embed_text(text: str) -> List[float]:
    client = openai.Client()
    res = client.embeddings.create(
        model="text-embedding-3-small",  # 1536 차원
        input=text)
    print(res)
    
    return res.data[0].embedding

text_list = ["오렌지", "설탕 커피", "카푸치노", "coffee"]
vector_list =[embed_text(text) for text in text_list]

# zip 함수는 text_list와 vector_list의 요소를 하나씩 꺼내서 반복문에서 사용할 수 있게 해줍니다.
for text, vector in zip(text_list, vector_list):
    print(f"{text} => {len(vector)} 차원 : {vector[:2]}")