from django.shortcuts import render
from django.views import View

class PostListView(View):
    def get(self, request):
        # 예시 데이터 - 실제로는 DB에서 가져와야 합니다
        posts = [
            {"title": "첫 번째 포스트"},
            {"title": "두 번째 포스트"},
        ]
        return render(request, "posts/post.html", {"posts": posts})