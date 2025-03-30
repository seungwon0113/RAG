import openai
from django.conf import settings
from . import rag

# 로깅 라이브러리
from colorlog import getLogger

logger = getLogger(__name__)

# 명시적으로 OPENAI_API_KEY 설정을 지정합니다.
client = openai.Client(api_key=settings.OPENAI_API_KEY)


# def make_ai_message(system_prompt: str, human_message: str) -> str:
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": human_message},
#         ],
#     )
#     ai_message = completion.choices[0].message.content

#     return ai_message


class PaikdabangAI:
    # 서버 시작할 때에만 1회 호출되어, 벡터 스토어 파일을 로딩합니다.
    def __init__(self):
        try:
            self.vector_store = rag.VectorStore.load(settings.VECTOR_STORE_PATH)
            # print(f"Loaded vector store {len(self.vector_store)} items")
            logger.debug("Loaded vector store %s items", len(self.vector_store))

        except FileNotFoundError as e:
            # print(f"Failed to load vector store: {e}")
            logger.error("Failed to load vector store: %s", e)
            self.vector_store = rag.VectorStore()

    # 매 AI 답변을 요청받을 때마다 호출됩니다.
    def __call__(self, question: str) -> str:
        # 답변과 유사한 지식을 찾습니다.
        search_doc_list = self.vector_store.search(question)
        # 찾은 지식을 문자열로 변환합니다.
        지식 = "\n\n".join(doc.page_content for doc in search_doc_list)

        res = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    # 지식을 포함한 시스템 프롬프트를 생성합니다.
                    "content": f"넌 AI Assistant. 모르는 건 모른다고 대답.\n\n[[빽다방 메뉴 정보]]\n{지식}",
                },
                {
                    "role": "user",
                    # 커밋에서는 질문이 하드코딩되어있습니다.
                    "content": question,
                },
            ],
            model="gpt-4o-mini",
            temperature=0,
        )
        ai_message = res.choices[0].message.content

        return ai_message


# 함수처럼 사용할 수 있는 인스턴스를 생성합니다.
# 인자로 질문 문자열 인자 하나만 받습니다.
ask_paikdabang = PaikdabangAI()