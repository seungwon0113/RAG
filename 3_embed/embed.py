# OpenAI API를 활용한 벡터 데이터 생성 예시

from typing import List, Dict
import openai, os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(text: str) -> List[float]:
    client = openai.Client()
    res = client.embeddings.create(
        model="text-embedding-3-small",  # 1536 차원
        input=text)
    print(res)
    
    return res.data[0].embedding


# 지식 데이터 준비
text_list = ["오렌지", "설탕 커피", "카푸치노", "coffee"]
vector_list =[embed_text(text) for text in text_list]

# zip 함수는 text_list와 vector_list의 요소를 하나씩 꺼내서 반복문에서 사용할 수 있게 해줍니다.
for text, vector in zip(text_list, vector_list):
    print(f"{text} => {len(vector)} 차원 : {vector[:2]}")

"""
[결과]
오렌지 => 1536 차원 : [0.012033403851091862, -0.050717972218990326]
설탕 커피 => 1536 차원 : [-0.0007802481413818896, -0.03417724370956421]
카푸치노 => 1536 차원 : [-0.021412773057818413, 0.001213638810440898]
coffee => 1536 차원 : [-0.010084450244903564, 0.003752504475414753]
"""

# 유사도 높은 데이터 찾기
question = "커피"
question_vector = embed_text(question) # 질문 벡터 생성
print(f"{question} => {len(question_vector)} 차원 : {question_vector[:2]}")

"""
[결과]
커피 => 1536 차원 : [-0.03492514789104462, -0.007396534085273743]
"""

# 벡터 데이터 코사인 유사도 계산
from sklearn.metrics.pairwise import cosine_similarity

similarity_list = cosine_similarity([question_vector], vector_list)[0]
print(similarity_list) # numpy 배열 타입

'''
[결과]
커피와 유사도가 높은 데이터
[오렌지, 설탕 커피, 카푸치노, coffee]
[0.2494598  0.49108656 0.24739216 0.44322914]
'''


