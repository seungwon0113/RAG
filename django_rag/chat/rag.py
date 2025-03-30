import pickle
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai
from django.conf import settings
from colorlog import getLogger

logger = getLogger(__name__)


client = openai.Client(api_key=settings.OPENAI_API_KEY)


def load(txt_file_path: Path) -> List[Document]:
    지식: str = txt_file_path.open("rt", encoding="utf-8").read()
    return [
        Document(
            metadata={"source": txt_file_path.name},
            page_content=지식,
        )
    ]


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


class VectorStore(list):
    embedding_model = settings.RAG_EMBEDDING_MODEL

    @classmethod
    def make(cls, doc_list: List[Document]) -> "VectorStore":
        vector_store = cls()
        for doc in doc_list:
            text = doc.page_content
            response = client.embeddings.create(model=cls.embedding_model, input=text)
            vector_store.append(
                {
                    "text": text,
                    "embedding": response.data[0].embedding,
                }
            )
        return vector_store

    @classmethod
    def load(cls, vector_store_path: Path) -> "VectorStore":
        with open(vector_store_path, "rb") as f:
            return pickle.load(f)

    def save(self, vector_store_path: Path) -> None:
        with vector_store_path.open("wb") as f:
            pickle.dump(self, f)
            # print(f"saved vector store to {vector_store_path}")
            logger.debug("saved vector store to %s", vector_store_path)
    
    # 벡터 저장소에서 질문에 대한 답변을 찾는 함수
    # top_k는 찾을 답변의 개수
    def search(self, question: str, top_k: int = 10) -> List[Document]:
        # pip install -U scikit-learn
        response = client.embeddings.create(model=self.embedding_model, input=question)
        question_embedding = response.data[0].embedding
        embedding_list = [row["embedding"] for row in self]

        # 모든 데이터와 코사인 유사도 계산
        similarities = cosine_similarity([question_embedding], embedding_list)[0]

        # 유사도가 높은 순으로 정렬
        indices = np.argsort(similarities)[::-1]
        
        # 중복 제거를 위한 세트
        seen_menus = set()
        filtered_indices = []
        
        # 중복되지 않은 메뉴만 선택
        for idx in indices:
            menu_text = self[idx]["text"]
            # 메뉴 이름 추출 (첫 줄의 첫 단어)
            menu_name = menu_text.split('\n')[0].split()[0] if menu_text else ''
            
            if menu_name not in seen_menus:
                seen_menus.add(menu_name)
                filtered_indices.append(idx)
                
            if len(filtered_indices) >= top_k:
                break

        return [
            Document(
                metadata={"similarity": similarities[idx]},
                page_content=self[idx]["text"],
            )
            for idx in filtered_indices
        ]


def print_prices(input_tokens: int, output_tokens: int) -> None:
    input_price = (input_tokens * 0.150 / 1_000_000) * 1_500
    output_price = (output_tokens * 0.600 / 1_000_000) * 1_500
    print("input: tokens {}, krw {:.4f}".format(input_tokens, input_price))
    print("output: tokens {}, krw {:4f}".format(output_tokens, output_price))