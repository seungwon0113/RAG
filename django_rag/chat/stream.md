# RAG 비동기 Stream 처리

| 메서드 | 동기 | 설명 |
|--------|------|------|
| invoke | 동기 | 한 번에 전체 응답을 반환 |
| stream | 동기 | 응답이 생성되는 대로 점진적으로 반환 |
| ainvoke | 비동기 | 한 번에 전체 응답을 반환 |
| astream | 비동기 | 응답이 생성되는 대로 점진적으로 반환 |
---
![Stream 처리 방식](../../image/stream.git)

---
## StreamingHttpResponse
- 장고 HttpResponse >> StreamingHttpResponse

