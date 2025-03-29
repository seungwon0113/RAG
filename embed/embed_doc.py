from typing import List, Dict
from langchain_core.documents import Document
import openai

# 예전에는 `langchain` 라이브러리 기본에서 다양한 `Loader`를 지원했지만,
# 요즘은 `langchain-community` 라이브러리 등 외부 라이브러리로 지원하는 경우가 많습니다.
from langchain_community.document_loaders import TextLoader

# 앞선 "파이썬 코드로 직접 문서 변환" 코드와 동일한 동작
# 문서 변환
def load() -> List[Document]:
    file_path = "backdabang.txt"
    loader = TextLoader(file_path=file_path)
    docs: List[Document] = loader.load()
    return docs

# 문서 쪼개기
def split(src_doc_list: List[Document]) -> List[Document]:
    new_doc_list = []
    for doc in src_doc_list:
        for new_page_content in doc.page_content.split("\n\n"):
            new_doc_list.append(
                Document(
                    metadata=doc.metadata.copy(),
                    page_content=new_page_content,
                )
            )
    return new_doc_list

# 문서 임베딩 : 문서를 벡터 형태로 변환
def embed(doc_list: List[Document]) -> List[Dict]:
    vector_store = []
    client = openai.Client()
    
    for doc in doc_list:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=doc.page_content,
        )
        vector_store.append(
            {
                "document": doc.model_copy(),
                "embedding": response.data[0].embedding,
            }
        )

    return vector_store


doc_list = load()
print(f"loaded {len(doc_list)} documents")
doc_list = split(doc_list)
print(f"split into {len(doc_list)} documents")
# pprint(doc_list)

# 문서 임베딩
vector_store = embed(doc_list)
print(f"created {len(vector_store)} items in vector store")
for row in vector_store:
    print(
        "{}... => {} 차원, {} ...".format(
            row["document"].page_content[:10],
            len(row["embedding"]),
            row["embedding"][:2],
        )
    )
    
"""
[문서 임베딩 결과]
loaded 1 documents
split into 10 documents
created 10 items in vector store
1. 아이스티샷추가... => 1536 차원, [-0.02684219554066658, -0.04342048242688179] ...
2. 바닐라라떼(I... => 1536 차원, [0.024926191195845604, -0.04808809980750084] ...
3. 사라다빵
  ... => 1536 차원, [0.02738669142127037, -0.042352572083473206] ...
4. 빽사이즈 아메... => 1536 차원, [-0.009571642614901066, -0.034707192331552505] ...
5. 빽사이즈 원조... => 1536 차원, [0.03405801206827164, 0.03657251223921776] ...
6. 빽사이즈 원조... => 1536 차원, [0.041632045060396194, -0.0009402853902429342] ...
7. 빽사이즈 달콤... => 1536 차원, [0.014816408045589924, -0.017857378348708153] ...
8. 빽사이즈 아이... => 1536 차원, [-0.012083002366125584, -0.02603047899901867] ...
9. 빽사이즈 아이... => 1536 차원, [0.009232023730874062, 0.05004415661096573] ...
10. 빽사이즈 초... => 1536 차원, [0.06580878049135208, 0.010091517120599747] ...
"""