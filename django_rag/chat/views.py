from django.http import HttpResponse
from django.shortcuts import render

from chat.ai import ask_paikdabang


def index(request):
    return render(request, "chat/index.html")


def reply(request):
    if request.method == "POST":
        human_message = request.POST.get("message", "")

        ai_message = ask_paikdabang(human_message)

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
