# 파이썬 코드를 이용한 문서변환
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from pprint import pprint # 파이썬 라이브러리 : 자료구조에 맞춰서 출력
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

def load() -> List[Document]:
    file_path = "backdabang.txt"
    loader = TextLoader(file_path=file_path)
    docs: List[Document] = loader.load()
    return docs

def split(src_doc_list: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=140,  # 문서를 나눌 최소 글자 수 (디폴트: 4000)
        chunk_overlap=0,  # 문서를 나눌 때 겹치는 글자 수 (디폴트: 200)
    )
    new_doc_list = text_splitter.split_documents(src_doc_list)
    return new_doc_list

doc_list = load()
print(f"loaded {len(doc_list)} documents")
# load한 문서 쪼개기
doc_list = split(doc_list)
print(f"split into {len(doc_list)} documents")
pprint(doc_list)