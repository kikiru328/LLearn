# LLearn — AI 학습 설계 & 피드백 플랫폼 (Backend)

> **TL;DR (3줄 요약)**  
> 1) 목표 → 커리큘럼 → 요약 → AI 피드백 → 반복의 학습 사이클을 자동화합니다.  
> 2) FastAPI + MySQL + Redis (+ 비동기 처리) 기반, Clean Architecture로 확장 가능한 구조입니다.  
> 3) 핵심 API는 `auth`, `users`, `curriculums`, `summaries`, `feedbacks`, `feed`, `social(like/comment)`, `admin` 입니다.

<br/>

## 🔗 빠른 링크(문서)
- [개요(Overview)](docs/overview.md)
- [아키텍처](docs/architecture.md)
- [설치 & 실행(Setup)](docs/setup.md)
- [운영(캐시·모니터링·비동기·트러블슈팅)](docs/operations.md)
- [보안 가이드](docs/security.md)
- [API 색인](docs/api/README.md)

---

## 🚀 빠른 시작 (Quick Start)

### 1) 요구 사항
- Docker, Docker Compose

### 2) 환경변수 예시 (`.env`)
```bash
# App
APP_NAME=llearn
APP_PORT=8000
ENV=local
SECRET_KEY=change_me

# DB (MySQL)
MYSQL_HOST=llearn-db
MYSQL_PORT=3306
MYSQL_DATABASE=llearn
DATABASE_NAME=llearn_user
DATABASE_PASSWORD=change_me
DATABASE_ROOT_PASSWORD=change_me
SQLALCHEMY_DATABASE_URI=mysql+aiomysql://${DATABASE_NAME}:${DATABASE_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}

# Redis
REDIS_HOST=llearn-redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_secure_password_2024

# LLM
OPENAI_API_KEY=...

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
```

### 3) 실행
```bash
# 1) 컨테이너 기동
docker compose -f docker-compose.yml up -d --build

# 2) DB 마이그레이션 (자동으로 migration)
docker exec -it llearn-app alembic upgrade head

# 3) 확인
open http://localhost:3000        # React APP
open http://localhost:8000/docs   # Swagger / OpenAPI
open http://localhost:3001/       # Grafana (예시)
```

> 참고: `/metrics` 엔드포인트가 노출된다면 Prometheus가 스크랩하는 메트릭을 확인할 수 있습니다.

---

## 🧱 프로젝트 구조(요약)
```
app/
  core/                 # 설정, DI, 인증 등
  common/               # 공통 유틸 (redis, llm, metrics 등)
  modules/
    user/
      domain/           # Entity, ValueObject, Repository Interface
      application/      # Usecase(Service), DTO
      interface/        # Controller / Router / Schema
      infrastructure/   # DB Models, Repository Impl
    curriculum/
    summary/
    feedback/
    social/             # like, comment
    admin/
infrastructure/         # 외부 I/O (선택 사항)
tests/
```

- **의존 흐름**: Interface → Application(Usecase) → Domain → Infrastructure  
- **장점**: 테스트 용이, 모듈 분리, 교체 가능(LLM/DB/Cache)

---

## 📡 API 한눈에 보기 (요약 표)
자세한 스펙은 **[API 색인](docs/api/README.md)** 및 각 문서를 참고하세요.

| 도메인 | Base Path | 주요 기능 | 인증 | 참고 |
|---|---|---|---|---|
| Auth | `/auth` | 회원가입, 로그인(JWT), 로그아웃, 리프레시 | 일부 필요 | [auth.md](docs/api/auth.md) |
| Users | `/users` | 내 정보 조회/수정/삭제 | 필요 | [users.md](docs/api/users.md) |
| Curriculums | `/curriculums` | 생성(LLM), 저장/조회/수정/삭제, 목록 | 필요 | [curriculums.md](docs/api/curriculums.md) |
| Summaries | `/summaries` | 주차 요약 생성/조회/수정/삭제, 피드 노출 | 필요 | [summaries.md](docs/api/summaries.md) |
| Feedbacks | `/feedbacks` | 요약 기반 AI 피드백 조회(5단계) | 필요 | [feedbacks.md](docs/api/feedbacks.md) |
| Feed | `/summaries/feed` | 공개 요약 피드 | 선택 | [feed.md](docs/api/feed.md) |
| Social | `/.../like`, `/comments` | 좋아요/댓글(요약/커리큘럼) | 필요 | [social.md](docs/api/social.md) |
| Admin | `/admin` | 사용자/콘텐츠 관리, LLM 로그 | 관리자 | [admin.md](docs/api/admin.md) |

---

## 📈 모니터링 & 지표(예시 목표)
- **주요 메트릭**: 요청 QPS, 에러율(4xx/5xx), DB 커넥션/슬로우쿼리, LLM 호출 수·지연·비용, 사용자 활동 수치(커리큘럼/요약/피드백/좋아요/댓글)

---

## 🗺️ 로드맵 (요약)
- **Phase 1**: 커리큘럼 생성/요약/피드백/진도 추적
- **Phase 2**: 피드/좋아요/댓글 + Admin + 캐시/비동기 + 부하테스트
- **Phase 3**: 모니터링·알림, CI/CD, 성능 개선

---

## 📚 참고(내부 문서)
- 모든 근거, 상세 흐름, 문제 해결 기록은 `docs/` 하위 문서를 참조하세요.
