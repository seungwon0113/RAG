# django-llm-chat-proj
```
├── 📁 accounts/            # 사용자 인증 및 관련 기능
├── 📁 chat/                # 채팅 기능 관련 앱
├── 📁 mysite/              # Django 설정 및 루트 구성 (settings, urls 등)
├── 📁 pickle/              # Pickle 관련 기능 (예: 파일 저장/불러오기 등)
├── 📁 posts/               # 게시글 관리 기능
├── 📁 static/              # 정적 파일(css, js, 이미지 등)
├── 📁 templates/           # HTML 템플릿 파일
├── 📄 .env                 # 환경 변수 파일
├── 📄 .gitignore           # Git에서 제외할 파일 목록
├── 📄 docker-compose.yml   # Docker 서비스 구성 파일
├── 📄 dockerfile           # Docker 이미지 빌드 설정
├── 📄 manage.py            # Django 프로젝트 실행 스크립트
└── 📄 requirements.txt     # 프로젝트 의존 패키지 목록
```

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

