from django.contrib import admin
from .models import PaikdabangMenuDocument

@admin.register(PaikdabangMenuDocument)
class PaikdabangMenuDocumentAdmin(admin.ModelAdmin):
    # form 인자를 지정하지 않으면, 내부에서 모델폼 클래스를 직접 생성하여 사용합니다.
    # form = PaikdabangMenuDocumentForm
    pass