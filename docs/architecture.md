# 아키텍처

## 기술 스택
- **FastAPI** (REST, OpenAPI)
- **SQLAlchemy(Async) + MySQL**
- **Redis** (캐시/세션/카운팅)
- **(선택) Kafka/Celery** (비동기 처리)
- **Prometheus + Grafana** (모니터링)

## Clean Architecture
- 계층: `interface → application(usecase) → domain → infrastructure`
- 이점: 모듈화, 테스트 용이, 교체 용이(LLM/DB/Cache)

## 디렉터리 가이드(예시)
```
app/
  core/               # 설정, DI, 인증
  common/             # 공통 클라이언트(LLM/Redis/metrics)
  modules/
    <feature>/
      domain/
        entity/
        value_object/
        repository/
      application/
        service/      # Usecase
        dto.py
      interface/
        controller/   # FastAPI Router
        schema/       # Pydantic Schemas
      infrastructure/
        db_models/
        repository/
```

## 의존성 규칙
- Interface → Application → Domain → Infrastructure (단방향)
- Domain은 외부(Infra)에 의존하지 않음

## 비동기/캐시/모니터링 개요
- **비동기**: 요약 → 피드백 생성은 별도 워커에서 처리(대기시간↓)
- **캐시**: 인기 피드, 좋아요 수, 세션/JWT 블랙리스트 등 (TTL·정합성 정책 필수)
- **모니터링**: 요청 지연/에러, DB/Redis, LLM 호출량·비용 대시보드
