# 랭체인 라이브러리를 이용한 문서 변환

from typing import List
from pprint import pprint
from langchain_core.documents import Document

# 예전에는 `langchain` 라이브러리 기본에서 다양한 `Loader`를 지원했지만,
# 요즘은 `langchain-community` 라이브러리 등 외부 라이브러리로 지원하는 경우가 많습니다.
from langchain_community.document_loaders import TextLoader

# 앞선 "파이썬 코드로 직접 문서 변환" 코드와 동일한 동작
def load() -> List[Document]:
    file_path = "backdabang.txt"
    loader = TextLoader(file_path=file_path)
    docs: List[Document] = loader.load()
    return docs

doc_list = load()
print(f"loaded {len(doc_list)} documents")
pprint(doc_list)