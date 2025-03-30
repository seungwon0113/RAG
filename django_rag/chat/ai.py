import logging
from typing import Union, AsyncGenerator, Optional

import openai
from django.conf import settings

# 비동기 처리
from openai import AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from . import rag

logger = logging.getLogger(__name__)

sync_client = openai.Client(api_key=settings.OPENAI_API_KEY)
async_client = openai.AsyncClient(api_key=settings.OPENAI_API_KEY)


def make_ai_message(system_prompt: str, human_message: str) -> str:
    completion = sync_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_message},
        ],
    )
    ai_message = completion.choices[0].message.content

    return ai_message


class PaikdabangAI:
    def __init__(self):
        try:
            self.vector_store = rag.VectorStore.load(settings.VECTOR_STORE_PATH)
            logger.debug("Loaded vector store %s items", len(self.vector_store))
        except FileNotFoundError as e:
            logger.error("Failed to load vector store: %s", e)
            self.vector_store = rag.VectorStore()
    
    # 비동기 처리
    async def get_response(self, question: str, stream: bool = False) -> Union[
        ChatCompletion,  # 동기 OpenAI API 호출 시
        AsyncStream[ChatCompletionChunk],  # 비동기 OpenAI API 호출 시
    ]:
        search_doc_list = self.vector_store.search(question)
        지식 = "\n\n".join(doc.page_content for doc in search_doc_list)

        return await async_client.chat.completions.create(
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
            stream=stream,
        )

    # 비동기. 한 번에 전체 응답을 반환
    async def __call__(self, question: str) -> str:
        return await self.ainvoke(question)

    # 비동기. 한 번에 전체 응답을 반환
    async def ainvoke(self, question: str) -> str:
        res: ChatCompletion
        res = await self.get_response(question, stream=False)
        ai_message = res.choices[0].message.content
        return ai_message

    # 비동기. 응답이 생성되는 대로 점진적으로 반환
    async def astream(self, question: str) -> AsyncGenerator[Optional[str]]:
        res: AsyncStream[ChatCompletionChunk]
        res = await self.get_response(question, stream=True)
        async for chunk in res:
            ai_message_chunk: str = chunk.choices[0].delta.content
            yield ai_message_chunk


ask_paikdabang = PaikdabangAI()
