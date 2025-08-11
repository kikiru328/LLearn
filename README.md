# LLearn 🚀

> **AI 기반 개인화 학습 커리큘럼 플랫폼**  
> 목표에 맞는 커리큘럼을 AI로 생성하고, 학습 요약에 대한 개인화된 피드백을 받아보세요!

[![Python](https://img.shields.io/badge/Python-3.13+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green)](https://fastapi.tiangolo.com)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-blue)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-containerized-blue)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 목차

- [🎯 프로젝트 소개](#-프로젝트-소개)
- [✨ 주요 기능](#-주요-기능)
- [🏗️ 아키텍처](#️-아키텍처)
- [🚀 빠른 시작](#-빠른-시작)
- [📚 API 문서](#-api-문서)
- [🛠️ 기술 스택](#️-기술-스택)
- [🔒 보안](#-보안)
- [📊 모니터링](#-모니터링)
- [🤝 기여하기](#-기여하기)

## 🎯 프로젝트 소개

**LLearn**은 AI를 활용한 개인화 학습 플랫폼입니다. 학습자의 목표와 수준에 맞는 커리큘럼을 자동으로 생성하고, 학습 진행 상황에 따라 맞춤형 피드백을 제공합니다.

### 핵심 가치

- 🎯 **목표 기반 학습**: 개인의 학습 목표에 맞는 체계적인 커리큘럼
- 🤖 **AI 피드백**: 학습 요약에 대한 5단계 평가 (정확성, 누락, 오류, 심화질문, 확장학습)
- 📈 **진도 추적**: 학습 현황과 성취도를 한눈에 확인
- 👥 **커뮤니티**: 다른 학습자들과 경험 공유 및 동기 부여

## ✨ 주요 기능

### 🎓 학습 관리
- **AI 커리큘럼 생성**: 목표, 기간, 난이도를 입력하면 자동으로 주차별 커리큘럼 생성
- **주차별 학습 요약**: 학습 내용을 요약하고 기록
- **개인화 피드백**: AI가 요약 내용을 분석해 5가지 관점에서 피드백 제공
- **학습 통계**: 진도율, 연속 학습 일수, 점수 분포 등 상세 통계

### 🌐 소셜 기능
- **피드 공유**: 공개 커리큘럼을 피드에서 발견
- **좋아요 & 댓글**: 관심 있는 커리큘럼에 반응
- **팔로우 시스템**: 다른 학습자를 팔로우하고 학습 현황 확인
- **북마크**: 나중에 참고할 커리큘럼 저장

### 🏷️ 분류 & 검색
- **태그 시스템**: 커리큘럼에 태그를 추가해 분류
- **카테고리**: 관리자가 생성한 카테고리로 체계적 분류
- **검색 기능**: 태그, 카테고리, 키워드로 원하는 커리큘럼 발견

### 👨‍💼 관리자 기능
- **사용자 관리**: 사용자 역할 변경, 계정 관리
- **콘텐츠 관리**: 커리큘럼 공개/비공개 설정, 삭제
- **피드 관리**: 전체 피드 캐시 갱신, 콘텐츠 모더레이션

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                 Frontend (React)                        │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI Server                        │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │   Auth      │ │ Curriculum  │ │   Social & Feed     │ │
│ │   Users     │ │ Learning    │ │   Taxonomy          │ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Infrastructure Layer                       │
│ ┌───────────┐ ┌───────────┐ ┌─────────┐ ┌─────────────┐ │
│ │  MySQL    │ │   Redis   │ │ OpenAI  │ │  Langfuse   │ │
│ │  (Main    │ │  (Cache   │ │ (LLM    │ │ (Observ-    │ │
│ │   DB)     │ │  & Queue) │ │ Service)│ │  ability)   │ │
│ └───────────┘ └───────────┘ └─────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Clean Architecture 구조

```
backend/app/
├── api/v1/                    # API 라우터
├── core/                      # 설정, 인증, DI
├── common/                    # 공통 서비스 (LLM, Cache, DB)
├── modules/                   # 도메인별 모듈
│   ├── user/
│   ├── curriculum/
│   ├── learning/
│   ├── social/
│   ├── taxonomy/
│   ├── feed/
│   └── admin/
└── utils/                     # 유틸리티

각 모듈 구조:
module/
├── domain/                    # 엔티티, 도메인 서비스
├── application/               # 비즈니스 로직
├── infrastructure/           # DB, 외부 서비스
└── interface/                # API 컨트롤러
```

## 🚀 빠른 시작

### 사전 요구사항

- **Python 3.13+** 
- **Poetry** (의존성 관리)
- **Docker & Docker Compose**
- **MySQL 8.0+**
- **Redis 7.0+**
- **OpenAI API 키** (또는 다른 LLM 서비스)
- **Langfuse 계정** (선택사항, 모니터링용)

### 1. 프로젝트 클론 및 환경 설정

```bash
# 저장소 클론
git clone https://github.com/f-lab-edu/LLearn.git
cd LLearn

# 환경 변수 설정
cp .env.example .env
```

### 2. 환경 변수 설정

`.env` 파일에서 🔥 표시된 필수 항목들을 수정하세요:

```env
# 🔥 필수 변경 항목들
SECRET_KEY=your-secret-key-here                    # 🔥 
LLM_API_KEY=your-openai-api-key                   # 🔥
LANGFUSE_SECRET_KEY=your-langfuse-secret-key      # 🔥
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key      # 🔥
DATABASE_ROOT_PASSWORD=your-secure-db-password    # 🔥
REDIS_PASSWORD=your-secure-redis-password         # 🔥
```

**시크릿 키 생성**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Docker Compose로 실행

```bash
# 전체 서비스 실행 (백엔드 + 프론트엔드 + DB + Redis + 모니터링)
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 특정 서비스만 실행
docker-compose up -d db redis  # DB, Redis만
docker-compose up app          # 백엔드만
```

### 4. 개발 환경 설정 (로컬)

```bash
# Poetry 설치
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
cd backend
poetry install

# 가상환경 활성화
poetry shell

# 환경 변수 로드 후 서버 실행
cd ..
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 데이터베이스 마이그레이션

```bash
# 컨테이너 내에서 실행
docker-compose exec app poetry run alembic upgrade head

# 또는 로컬에서 실행
cd backend
poetry run alembic upgrade head
```

### 6. 접속 확인

- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **프론트엔드**: http://localhost:3000
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090

## 📚 API 문서

### 주요 엔드포인트

#### 🔐 인증 (`/api/v1/auth`)
```http
POST /api/v1/auth/signup      # 회원가입
POST /api/v1/auth/login       # 로그인
GET  /api/v1/users/me         # 내 정보 조회
```

#### 📚 커리큘럼 (`/api/v1/curriculums`)
```http
POST /api/v1/curriculums                    # 커리큘럼 생성
POST /api/v1/curriculums/generate           # AI 커리큘럼 생성
GET  /api/v1/curriculums/me                 # 내 커리큘럼 목록
GET  /api/v1/curriculums/public             # 공개 커리큘럼 목록
GET  /api/v1/curriculums/{id}               # 커리큘럼 상세 조회
```

#### 📝 학습 & 피드백 (`/api/v1/summaries`, `/api/v1/feedbacks`)
```http
POST /api/v1/curriculums/{id}/weeks/{week}/summaries  # 학습 요약 작성
POST /api/v1/summaries/{id}/feedbacks/generate        # AI 피드백 생성
GET  /api/v1/users/me/learning/stats                  # 내 학습 통계
```

#### 👥 소셜 (`/api/v1/social`)
```http
POST /api/v1/curriculums/{id}/like          # 좋아요
POST /api/v1/curriculums/{id}/comments      # 댓글 작성
POST /api/v1/social/follow                  # 사용자 팔로우
GET  /api/v1/feed/public                    # 공개 피드 조회
```

### 상세 API 문서

프로젝트의 `docs/api/` 폴더에서 각 도메인별 상세 API 문서를 확인하실 수 있습니다:

- [📄 Auth & Users API](docs/api/user.md)
- [📚 Curriculum API](docs/api/curriculums.md) 
- [🎓 Learning & Feedback API](docs/api/learning.md)
- [👥 Social API](docs/api/social.md)
- [📰 Feed API](docs/api/feed.md)
- [🏷️ Taxonomy API](docs/api/taxonomy.md)
- [👨‍💼 Admin API](docs/api/admin.md)

## 🛠️ 기술 스택

### Backend Core
- **Framework**: FastAPI 0.116+ (고성능 비동기 웹 프레임워크)
- **Language**: Python 3.13
- **Dependency Management**: Poetry
- **Database**: MySQL 8.0 + SQLAlchemy (Async ORM)
- **Cache & Queue**: Redis 7.0+ 
- **Authentication**: JWT (python-jose)

### AI & LLM Integration
- **LLM Framework**: LangChain 0.3+ (추상화 레이어)
- **LLM Provider**: OpenAI GPT-4o-mini
- **Observability**: Langfuse (LLM 호출 추적 및 분석)
- **Prompt Management**: 구조화된 프롬프트 템플릿

### Architecture & DI
- **Pattern**: Clean Architecture (4-layer)
- **Dependency Injection**: dependency-injector
- **ID Generation**: ULID (Universally Unique Lexicographically Sortable Identifier)
- **Password Hashing**: bcrypt (passlib)

### DevOps & Monitoring
- **Containerization**: Docker + Docker Compose
- **Database Migration**: Alembic
- **Metrics**: Prometheus + Grafana
- **Health Checks**: 내장 헬스체크 엔드포인트
- **Logging**: 구조화된 로깅

### Development Tools
- **Code Formatting**: Black + Poetry scripts
- **Testing**: pytest + pytest-asyncio
- **Type Checking**: Pydantic 2.0+ (runtime validation)
- **API Documentation**: OpenAPI 3.0 (자동 생성)

### Frontend (Development)
- **Framework**: React (CRA 기반)
- **Development Server**: Hot-reload 지원
- **Container**: 개발용 Docker 환경

## 🔒 보안

### 인증 & 인가
```python
# JWT 기반 토큰 인증
from app.core.auth import get_current_user, Role

@router.get("/protected")
async def protected_endpoint(
    current_user: CurrentUser = Depends(get_current_user)
):
    return {"user_id": current_user.id, "role": current_user.role}

# 관리자 권한 체크
from app.core.auth import assert_admin

@router.get("/admin-only")
async def admin_only(
    current_user: CurrentUser = Depends(get_current_user)
):
    assert_admin(current_user)  # 403 if not admin
    return {"message": "Admin access granted"}
```

### 데이터 보호
- **비밀번호**: bcrypt 해싱 (Crypto 클래스)
- **SQL Injection**: SQLAlchemy ORM 사용으로 방지
- **입력 검증**: Pydantic 스키마로 런타임 검증
- **CORS**: 설정된 오리진만 허용

### 보안 설정 예시
```python
# CORS 설정
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# 시크릿 관리
SECRET_KEY = "your-secret-key"  # 환경변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 15
```

## 📊 모니터링

### Prometheus 메트릭
- **API 성능**: 응답 시간 분포 (P50/P95/P99)
- **에러율**: 4xx/5xx 상태코드 추적
- **처리량**: 초당 요청 수 (QPS)
- **LLM 사용량**: 호출 수, 토큰 사용량

### Grafana 대시보드
```yaml
# 주요 대시보드 패널
- API Response Time (P95)
- Error Rate by Endpoint  
- Database Connections
- Redis Cache Hit Rate
- LLM Cost Tracking
```

### 헬스체크
```python
# 엔드포인트: GET /health
{
    "status": "healthy",
    "service": "curriculum-api",
    "database": "connected",
    "redis": "connected",
    "llm_service": "available"
}
```

### Langfuse LLM 추적
```python
# 자동 추적되는 정보
- 프롬프트 템플릿 사용량
- 토큰 소비량 및 비용
- 응답 품질 분석
- 에러율 및 지연시간
```

## 🚀 배포

### Docker 멀티스테이지 빌드
```dockerfile
FROM python:3.13
WORKDIR /workspace

# Poetry 설치 및 의존성 관리
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# 애플리케이션 복사
COPY . .
EXPOSE 8000
CMD ["sh", "/workspace/script/startup.sh"]
```

### 환경별 설정
```bash
# 개발 환경
docker-compose up -d

# 프로덕션 환경  
docker-compose -f docker-compose.prod.yml up -d
```

### CI/CD 권장사항
```yaml
# GitHub Actions 예시
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          docker-compose run app poetry run pytest
  
  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # 배포 스크립트 실행
```

## 🧪 테스트

### 테스트 실행
```bash
# Poetry를 통한 테스트
cd backend
poetry run pytest

# Docker를 통한 테스트
docker-compose run app poetry run pytest

# 커버리지 포함 테스트
poetry run pytest --cov=app tests/

# 특정 모듈 테스트
poetry run pytest tests/modules/curriculum/ -v
```

### 테스트 구조
```
backend/tests/
├── conftest.py              # 테스트 설정 및 픽스처
├── modules/
│   ├── user/               # 사용자 도메인 테스트
│   ├── curriculum/         # 커리큘럼 도메인 테스트
│   └── learning/          # 학습 도메인 테스트
├── integration/           # 통합 테스트
├── fixtures/             # 테스트 데이터
└── utils/               # 테스트 유틸리티
```

### 테스트 픽스처 예시
```python
# conftest.py
@pytest.fixture
async def test_db():
    """테스트용 DB 세션"""
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture
def test_user():
    """테스트용 사용자 데이터"""
    return {
        "email": "test@example.com",
        "name": "테스트 사용자",
        "password": "Test1234!"
    }
```

## 🔧 개발 가이드

### 로컬 개발 환경
```bash
# 백엔드만 개발하는 경우
docker-compose up -d db redis  # DB, Redis만 실행
cd backend
poetry shell
uvicorn app.main:app --reload

# 프론트엔드 포함 개발
docker-compose up -d  # 전체 실행
```

### 코드 스타일
```bash
# Poetry scripts 사용
cd backend
poetry run black .          # 코드 포맷팅
poetry run pytest          # 테스트 실행

# Pre-commit hooks 설정 권장
pip install pre-commit
pre-commit install
```

### DB 마이그레이션
```bash
# 새 마이그레이션 생성
cd backend
poetry run alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
poetry run alembic upgrade head

# 롤백
poetry run alembic downgrade -1
```

### 새 모듈 추가하기
```bash
# Clean Architecture 구조 따라서 생성
backend/app/modules/new_module/
├── domain/
│   ├── entity/
│   ├── repository/
│   └── service/
├── application/
│   └── service/
├── infrastructure/
│   └── repository/
├── interface/
│   └── controller/
└── core/
    └── di_container.py
```

## 🤝 기여하기

LLearn 프로젝트에 기여해주셔서 감사합니다! 

### 기여 방법

1. **Fork** 저장소를 포크합니다
2. **Branch** 새로운 기능 브랜치를 생성합니다
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** 변경사항을 커밋합니다
   ```bash
   git commit -m 'Add: amazing feature'
   ```
4. **Push** 브랜치에 푸시합니다
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Pull Request**를 생성합니다

### 커밋 컨벤션
```
Type: Subject

Body (optional)

Footer (optional)
```

**Types**: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Test`, `Docs`

### 개발 가이드라인
- Clean Architecture 패턴 준수
- 타입 힌트 사용 (Python 3.9+ 스타일)
- Pydantic 모델로 입출력 검증
- 단위 테스트 작성
- API 문서화 (docstring)

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE) 하에 배포됩니다.

## 🙏 감사의 말

- [FastAPI](https://fastapi.tiangolo.com/) - 빠르고 현대적인 웹 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org/) - 강력한 ORM
- [LangChain](https://langchain.com/) - LLM 애플리케이션 프레임워크
- [OpenAI](https://openai.com/) - AI 서비스 제공
- [Langfuse](https://langfuse.com/) - LLM 관측성 플랫폼

---

<div align="center">

**🌟 이 프로젝트가 도움이 되셨다면 별표를 눌러주세요!**

[![GitHub stars](https://img.shields.io/github/stars/f-lab-edu/LLearn.svg?style=social&label=Star)](https://github.com/f-lab-edu/LLearn)

Made with ❤️ by [LLearn](https://github.com/f-lab-edu/LLearn)

</div>
