from typing import List, Dict
from langchain_core.documents import Document
import openai
import pickle
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from pprint import pprint

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

client = openai.Client()


# 비용 계산 함수
def print_prices(input_tokens: int, output_tokens: int) -> None:
    input_price = (input_tokens * 0.150 / 1_000_000) * 1_500
    output_price = (output_tokens * 0.600 / 1_000_000) * 1_500
    print("input: tokens {}, krw {:.4f}".format(input_tokens, input_price))
    print("output: tokens {}, krw {:4f}".format(output_tokens, output_price))



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
class VectorStore(list):
    embedding_model = "text-embedding-3-small"

    @classmethod
    def make(cls, doc_list: List[Document]) -> "VectorStore":
        vector_store = cls()

        for doc in doc_list:
            response = client.embeddings.create(
                model=cls.embedding_model,
                input=doc.page_content,
            )
            vector_store.append(
                {
                    "document": doc.model_copy(),
                    "embedding": response.data[0].embedding,
                }
            )

        return vector_store

    def save(self, vector_store_path: Path) -> None: 
        with vector_store_path.open("wb") as f:
            pickle.dump(self, f)
    @classmethod
    def load(cls, vector_store_path: Path) -> "VectorStore":
        with vector_store_path.open("rb") as f:
            return pickle.load(f)
      
      
    def search(self, question: str, k: int = 4) -> List[Document]:
        """
        질의 문자열을 받아서, 벡터 스토어에서 유사 문서를 최대 k개 반환
        """

        # 질문 문자열을 임베딩 벡터 배열로 변환
        response = client.embeddings.create(
            model=self.embedding_model,
            input=question,
        )
        question_embedding = response.data[0].embedding  # 1536 차원, float 배열

        # VectorStore 내에 저장된 모든 벡터 데이터를 리스트로 추출
        embedding_list = [row["embedding"] for row in self]

        # 모든 문서와 코사인 유사도 계산
        similarities = cosine_similarity([question_embedding], embedding_list)[0]
        # 유사도가 높은 순으로 정렬하여 k 개 선택
        top_indices = np.argsort(similarities)[::-1][:k]

        # 상위 k 개 문서를 리스트로 반환
        return [
            self[idx]["document"].model_copy()
            for idx in top_indices
        ]


def main():
    current_dir = Path(__file__).parent 
    vector_store_path = current_dir / "vector_store.pickle"

    if not vector_store_path.is_file():
        doc_list = load()
        print(f"loaded {len(doc_list)} documents")
        doc_list = split(doc_list)
        print(f"split into {len(doc_list)} documents")
        vector_store = VectorStore.make(doc_list)
        vector_store.save(vector_store_path)
        print(f"created {len(vector_store)} items in vector store")
    else:
        vector_store = VectorStore.load(vector_store_path)
        print(f"loaded {len(vector_store)} items in vector store")

    # 1. RAG를 수행할 질문을 먼전 정의
    question = "빽다방 카페인이 높은 음료와 가격은?"
    print(f"RAG를 통해 '{question}' 질문에 대해서 지식에 기반한 AI 답변을 구해보겠습니다.")

    # 2. vector_store에서 질문에 대한 유사 문서 검색
    search_doc_list: List[Document] = vector_store.search(question)
    pprint(search_doc_list)

    print("## 지식 ##")
    지식: str = str(search_doc_list)
    print(repr(지식))

    # 3. prompt 형식으로 질문에 대한 답변 생성
    res = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"넌 AI Assistant. 모르는 건 모른다고 대답.\n\n[[빽다방 메뉴 정보]]\n{지식}",
        },
        {
            "role": "user",
            "content": question,
        },
    ],
    model="gpt-4o-mini",
    temperature=0,
)
    print()
    print("[AI]", res.choices[0].message.content)
    print_prices(res.usage.prompt_tokens, res.usage.completion_tokens)

if __name__ == "__main__":
    main()