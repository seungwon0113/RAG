from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html

from chat.ai import make_ai_message


def index(request):
    return render(request, "chat/index.html")


def reply(request):
    if request.method == "POST":
        human_message = request.POST.get("message", "")

        system_prompt = "당신은 친절한 AI 어시스턴트입니다."
        ai_message = make_ai_message(system_prompt, human_message)

        # https://daisyui.com/components/chat/
        return HttpResponse(
            format_html(
                """
                    <div class="chat chat-start"><div class="chat-bubble">{}</div></div>
                    <div class="chat chat-end"><div class="chat-bubble">{}</div></div>
                """,
                human_message,
                ai_message,
            )
        )
    else:
        return HttpResponse("<div>허용하지 않는 메서드</div>")
