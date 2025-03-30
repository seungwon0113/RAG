import uuid

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from chat.ai import ask_paikdabang
from chat.utils import aenumerate


def index(request):
    return render(request, "chat/index.html")


async def reply(request):
    if request.method == "POST":
        human_message = request.POST.get("message", "")

        # 스트리밍 응답을 생성하는 함수
        async def make_chunk_response():
            # astream 메서드는 AsyncGenerator를 반환합니다.
            ai_message = ""
            ai_message_chunk: str
            message_pair_id = "ai_" + uuid.uuid4().hex
            async for chunk_index, ai_message_chunk in aenumerate(
                ask_paikdabang.astream(human_message)
            ):
                # None 일 경우, 빈 문자열로 변환해야만 문자열을 추가할 수 있습니다.
                ai_message += ai_message_chunk or ""

                # 매 chunk를 덧붙인 ai_message로 렌더링한 HTML을 생산합니다.
                yield render_to_string(
                    "chat/_chat_message.html",
                    {
                        "message_pair_id": message_pair_id,
                        "chunk_index": chunk_index,
                        "human_message": human_message,
                        "ai_message": ai_message,
                    },
                )

            #     print(ai_message_chunk, end="", flush=True)
            # print()
            #
            # # 응답 텍스트만 생성해야 하기에, render가 아닌 render_to_string을 사용합니다.
            # yield render_to_string(
            #     "chat/_chat_message.html",
            #     {
            #         "human_message": human_message,
            #         "ai_message": ai_message,
            #     },
            # )

        return StreamingHttpResponse(
            make_chunk_response(),
            content_type="text/event-stream",
        )
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
