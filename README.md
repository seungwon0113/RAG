## RAG 학습
### RAG(Retrieval-Augmented Generation)
: 대규모 언어 모델의 출력을 최적화하여 응답을 생성하기 전에 학습 데이터 소스 외부의 신뢰할 수 있는 지식 베이스를 참조하도록 하는 프로세스입니다.

---
## 전형적인 RAG
- 준비단계
1. 지식 변환 (Load)
2. 지식을 쪼개기 (Split)
3. 지식 표현 (Embed)
4. 지식 저장 (Store)

- 활용단계
5. 지식 검색 (Search) 및 LLM 요청/응답
<image src="image/rag.png">


---
### OpenAI API 가격 (2025년 1월 기준)

| Model | Input (100만 토큰 당) | Output (100만 토큰 당) |
|-------|----------------------|---------------------|
| OpenAI gpt-4o-mini | $0.15 | $0.6 |
| OpenAI gpt-4o | $2.5 | $10.0 |
| OpenAI gpt-o1-mini | $3.0 | $12.0 |
| OpenAI gpt-o1 | $0.15 | $60.0 |
| OpenAI gpt-4o-audio-preview | $40.0 | $80.0 |

