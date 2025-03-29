# 파이썬 코드를 이용한 문서변환

from typing import List
from pprint import pprint # 파이썬 라이브러리 : 자료구조에 맞춰서 출력
from langchain_core.documents import Document

def load() -> List[Document]:
    file_path = "backdabang.txt"
    지식: str = open(file_path, "rt", encoding="utf-8").read()
    docs = [
        Document(
            # 의미있는 메타데이터가 있다면, 맘껏 더 담으시면 됩니다.
            metadata={"source": file_path},
            page_content=지식,
        )
    ]
    return docs

doc_list = load()
print(f"loaded {len(doc_list)} documents")
pprint(doc_list)