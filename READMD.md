# LLearn

> 단기 기억을 장기 기억으로 전환시키는 AI 기반 CS 학습 시스템

## 주요 기능

-  **커리큘럼 생성**: 학습 목표 기반, CS 커리큘럼 자동 생성
- ️ **요약 제출**: 주차별 학습 내용을 Markdown으로 정리
-  **AI 피드백**: 5단계 구조화된 요약 피드백 제공
-  **학습 진도 추적**: 주차별 완료 상태, 학습 스트릭 관리
-  **JWT 인증**: 회원가입 / 로그인 / 내 정보 수정

## 기술 스택

- **Backend**: FastAPI, Python 3.13
- **Database**: MySQL, SQLAlchemy
- **Infra**: Redis, Kafka, Docker
- **AI**: OpenAI GPT-4
- **DevOps**: GitHub Actions, Prometheus, Grafana, Locust
- **Testing**: Pytest

## 프로젝트 구조
```bash
llearn  
├── domain/ # 비즈니스 로직 (엔티티, 인터페이스)  
├── usecase/ # 유스케이스 계층  
├── infrastructure/ # DB, LLM, Redis, Kafka 등  
├── app/ # FastAPI API 계층  
└── tests/ # 테스트 코드  
```



