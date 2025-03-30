# django-llm-chat-proj

## 가상환경 생성

```
python -m venv venv         # 가상환경 생성

venv\Scripts\activate       # 윈도우
source ./venv/bin/activate  # 맥/리눅스
```

## 개발서버 구동

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

