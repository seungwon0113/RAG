from typing import List, Dict
from langchain_core.documents import Document
import openai
import pickle
from pathlib import Path

from langchain_community.document_loaders import TextLoader

client = openai.Client()

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

class VectorStore(list):
    # 지식에 사용한 임베딩 모델과 질문에 사용할 임베딩 모델은 동일해야만 합니다.
    # 각각 임베딩 모델명을 지정하지 않고, 임베딩 모델명을 클래스 변수로 선언하여
    # 모델명 변경의 용이성을 확보합니다.
    embedding_model = "text-embedding-3-small"

    @classmethod
    # 본 embed 함수 make 메서드로 수정
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

        

# 벡터 스토어 문서/임베딩 데이터를 지정 경로에 파일로 저장
    def save(self, vector_store_path: Path) -> None: 
        """
        벡터 스토어 문서/임베딩 데이터를 지정 경로에 파일로 저장
        """
        with vector_store_path.open("wb") as f:
            # 리스트(self)를 pickle 포맷으로 파일(f)에 저장
            # dump : 객체를 파일에 저장(덮어쓰기)
            pickle.dump(self, f)
    @classmethod
    def load(cls, vector_store_path: Path) -> "VectorStore":
        """
        지정 경로의 파일을 읽어서 벡터 스토어 문서/임베딩 데이터 복원
        """
        with vector_store_path.open("rb") as f:
            return pickle.load(f)




def main():
    # Path(__file__).parent : 현재 파일이 있는 디렉토리를 기준으로 경로 설정
    current_dir = Path(__file__).parent 
    vector_store_path = current_dir / "vector_store.pickle"

    # 지정 경로에 파일이 없으면
    # 문서를 로딩하고 분할하여 벡터 데이터를 생성하고 해당 경로에 저장합니다.
    if not vector_store_path.is_file():
        doc_list = load()
        print(f"loaded {len(doc_list)} documents")
        doc_list = split(doc_list)
        print(f"split into {len(doc_list)} documents")
        # vector_store = embed(doc_list) >> 임베드 함수 주석 처리하고 클래스 호출
        vector_store = VectorStore.make(doc_list)
        vector_store.save(vector_store_path)
        print(f"created {len(vector_store)} items in vector store")
     # 지정 경로에 파일이 있으면, 로딩하여 VectorStore 객체를 복원합니다.
    else:
        vector_store = VectorStore.load(vector_store_path)
        print(f"loaded {len(vector_store)} items in vector store")

    # TODO: RAG를 통해 지식에 기반한 AI 답변을 구해보겠습니다.
    question = "빽다방 카페인이 높은 음료와 가격은?"
    print(f"RAG를 통해 '{question}' 질문에 대해서 지식에 기반한 AI 답변을 구해보겠습니다.")


if __name__ == "__main__":
    main()