from django.http import HttpResponse
from django.shortcuts import render

from chat.ai import ask_paikdabang


def index(request):
    return render(request, "chat/index.html")


async def reply(request):
    if request.method == "POST":
        human_message = request.POST.get("message", "")

        # ai_message = await ask_paikdabang(human_message)

        ai_message = ""
        ai_message_chunk: str
        async for ai_message_chunk in ask_paikdabang.astream(human_message):
            # None 일 경우, 빈 문자열로 변환해야만 문자열을 추가할 수 있습니다.
            ai_message += ai_message_chunk or ""
            print(ai_message_chunk, end="", flush=True)
        print()

        return render(
            request,
            "chat/_chat_message.html",
            {
                "human_message": human_message,
                "ai_message": ai_message,
            },
        )
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
