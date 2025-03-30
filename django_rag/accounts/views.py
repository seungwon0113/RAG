from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SignupForm


signup = CreateView.as_view(
    form_class=SignupForm,
    template_name="form.html",
    success_url="/accounts/login/",  # 추후에는 reverse_lazy 사용을 추천
)


login = LoginView.as_view(
    form_class=AuthenticationForm,
    redirect_authenticated_user=True,
    template_name="form.html",
    # 디폴트 이동 주소
    # success_url="/accounts/profile/",
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


logout = LogoutView.as_view(
    # next_page="accounts:login",
)
