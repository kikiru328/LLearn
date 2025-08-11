# Learning API Documentation

## API 엔드포인트 목록

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/curriculums/{curriculum_id}/weeks/{week_number}/summaries` | 학습 요약 생성 | ✅ |
| GET | `/curriculums/{curriculum_id}/weeks/{week_number}/summaries` | 특정 주차 요약 목록 | ✅ |
| GET | `/curriculums/{curriculum_id}/summaries` | 커리큘럼 요약 목록 | ✅ |
| GET | `/curriculums/summaries/{summary_id}` | 요약 상세 조회 | ✅ |
| PUT | `/curriculums/summaries/{summary_id}` | 요약 수정 | ✅ |
| DELETE | `/curriculums/summaries/{summary_id}` | 요약 삭제 | ✅ |
| GET | `/users/me/summaries` | 내 요약 목록 | ✅ |
| POST | `/summaries/{summary_id}/feedbacks/generate` | AI 피드백 생성 | ✅ |
| GET | `/summaries/{summary_id}/feedbacks` | 요약의 피드백 조회 | ✅ |
| GET | `/summaries/feedbacks/{feedback_id}` | 피드백 상세 조회 | ✅ |
| DELETE | `/summaries/feedbacks/{feedback_id}` | 피드백 삭제 | ✅ |
| GET | `/curriculums/{curriculum_id}/feedbacks` | 커리큘럼 피드백 목록 | ✅ |
| GET | `/users/me/feedbacks` | 내 피드백 목록 | ✅ |
| GET | `/users/me/learning/stats` | 내 학습 통계 | ✅ |
| GET | `/users/me/learning/overview` | 학습 현황 요약 | ✅ |
| GET | `/users/me/learning/progress` | 커리큘럼별 진도 | ✅ |
| GET | `/users/me/learning/streak` | 학습 연속성 정보 | ✅ |

## 학습 요약 관리 (Summaries)

### 1. 학습 요약 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}/summaries` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 주차 번호 (1-24) |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `content` | string | ✅ | 100-5000자, 학습 요약 내용 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 생성된 요약 정보 |
| `400` | 유효성 검증 실패 | 내용 길이 제한 위반 |
| `404` | 주차 없음 | 해당 주차가 커리큘럼에 존재하지 않음 |
| `403` | 권한 없음 | 본인 커리큘럼만 작성 가능 |

### 2. 특정 주차 요약 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}/summaries` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 주차 번호 |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 요약 목록 (페이지네이션) |

### 3. 커리큘럼 요약 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/summaries` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 해당 커리큘럼의 모든 요약 |

### 4. 요약 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/summaries/{summary_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `summary_id` | string | ✅ | 요약 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 요약 상세 정보 |
| `404` | 요약 없음 | - |
| `403` | 접근 권한 없음 | - |

### 5. 요약 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PUT` |
| **URL** | `/curriculums/summaries/{summary_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `summary_id` | string | ✅ | 요약 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `content` | string | ✅ | 100-5000자, 수정할 요약 내용 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 수정된 요약 정보 |
| `404` | 요약 없음 | - |
| `403` | 권한 없음 | 본인 요약만 수정 가능 |

### 6. 요약 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/summaries/{summary_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `summary_id` | string | ✅ | 요약 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 요약 없음 |
| `403` | 권한 없음 |

### 7. 내 요약 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/summaries` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 내가 작성한 모든 요약 목록 |

## 학습 피드백 관리 (Feedbacks)

### 8. AI 피드백 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/summaries/{summary_id}/feedbacks/generate` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `summary_id` | string | ✅ | 요약 ID |

**Request Body:** (빈 객체)
```json
{}
```

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | AI 생성된 피드백 |
| `400` | 이미 피드백 존재 | 하나의 요약당 하나의 피드백만 가능 |
| `404` | 요약 없음 | - |
| `500` | AI 생성 실패 | LLM 서비스 오류 |

### 9. 요약의 피드백 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/summaries/{summary_id}/feedbacks` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `summary_id` | string | ✅ | 요약 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 피드백 정보 (없으면 null) |
| `404` | 요약 없음 | - |

### 10. 피드백 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/summaries/feedbacks/{feedback_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `feedback_id` | string | ✅ | 피드백 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 피드백 상세 정보 |
| `404` | 피드백 없음 | - |
| `403` | 접근 권한 없음 | - |

### 11. 피드백 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/summaries/feedbacks/{feedback_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `feedback_id` | string | ✅ | 피드백 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 피드백 없음 |
| `403` | 권한 없음 |

### 12. 커리큘럼 피드백 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/feedbacks` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 해당 커리큘럼의 모든 피드백 |

### 13. 내 피드백 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/feedbacks` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |
| `min_score` | float | ❌ | - | 최소 점수 (0.0-10.0) |
| `max_score` | float | ❌ | - | 최대 점수 (0.0-10.0) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 내가 받은 모든 피드백 목록 |

## 학습 통계 (Learning Stats)

### 14. 내 학습 통계 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/learning/stats` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `days` | integer | ❌ | 30 | 통계 기간 (7-365일) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 상세한 학습 통계 |

### 15. 학습 현황 요약
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/learning/overview` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 대시보드용 간단 요약 |

### 16. 커리큘럼별 진도 현황
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/learning/progress` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 커리큘럼별 진도 정보 |

### 17. 학습 연속성 정보
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me/learning/streak` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 연속 학습 기록 정보 |

## 데이터 모델

### Summary 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 요약 ID |
| `curriculum_id` | string | 커리큘럼 ID |
| `week_number` | integer | 주차 번호 (1-24) |
| `content` | string | 요약 내용 (100-5000자) |
| `content_length` | integer | 내용 길이 |
| `snippet` | string | 내용 미리보기 (100자) |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### Feedback 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 피드백 ID |
| `summary_id` | string | 요약 ID |
| `comment` | string | 피드백 코멘트 |
| `score` | float | 점수 (0.0-10.0) |
| `grade` | string | 등급 (A+, A, B+, B, C+, C, D) |
| `comment_snippet` | string | 코멘트 미리보기 |
| `is_good_score` | boolean | 좋은 점수 여부 (≥7.0) |
| `is_poor_score` | boolean | 낮은 점수 여부 (≤4.0) |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### LearningStats 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `user_id` | string | 사용자 ID |
| `stats_period_days` | integer | 통계 기간 (일수) |
| `total_summaries` | integer | 총 요약 수 |
| `total_feedbacks` | integer | 총 피드백 수 |
| `active_curriculums` | integer | 활성 커리큘럼 수 |
| `completed_curriculums` | integer | 완료된 커리큘럼 수 |
| `learning_streak` | object | 학습 연속성 정보 |
| `score_distribution` | object | 점수 분포 |
| `curriculum_progress` | array | 커리큘럼별 진도 |
| `recent_activities` | array | 최근 활동 |
| `monthly_progress` | array | 월별 진도 |
| `weekly_goal_achievement` | float | 주간 목표 달성률 (%) |
| `generated_at` | datetime | 통계 생성 시간 |

### LearningStreak 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `current_streak` | integer | 현재 연속 학습 일수 |
| `longest_streak` | integer | 최장 연속 학습 일수 |
| `total_learning_days` | integer | 총 학습 일수 |

### ScoreDistribution 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `grade_counts` | object | 등급별 개수 {"A+": 5, "A": 3, ...} |
| `average_score` | float | 평균 점수 |
| `highest_score` | float | 최고 점수 |
| `lowest_score` | float | 최저 점수 |
| `total_feedbacks` | integer | 총 피드백 수 |

## 비즈니스 규칙

### 요약 (Summary) 제약사항
| 규칙 | 설명 |
|------|------|
| **내용 길이** | 100-5000자 |
| **주차 검증** | 해당 주차가 커리큘럼에 존재해야 함 |
| **소유권** | 커리큘럼 소유자만 요약 작성 가능 |

### 피드백 (Feedback) 제약사항
| 규칙 | 설명 |
|------|------|
| **점수 범위** | 0.0-10.0 |
| **관계** | 하나의 요약당 하나의 피드백 (1:1) |
| **생성 방식** | AI 자동 생성만 지원 |
| **코멘트** | 빈 값 불가 |

### 피드백 등급 시스템
| 점수 범위 | 등급 | 설명 |
|-----------|------|------|
| 9.0-10.0 | A+ | 매우 우수 |
| 8.0-8.9 | A | 우수 |
| 7.0-7.9 | B+ | 양호 |
| 6.0-6.9 | B | 보통 |
| 5.0-5.9 | C+ | 부족 |
| 4.0-4.9 | C | 미흡 |
| 0.0-3.9 | D | 매우 미흡 |

### AI 피드백 생성 규칙
| 규칙 | 설명 |
|------|------|
| **입력** | 커리큘럼 주차별 레슨 + 사용자 요약 |
| **출력** | 코멘트 + 점수 (0.0-10.0) |
| **중복 방지** | 이미 피드백이 있는 요약에는 생성 불가 |
| **권한** | 커리큘럼 소유자만 생성 가능 |

### 학습 통계 계산 규칙
| 지표 | 계산 방식 |
|------|----------|
| **완료율** | (작성된 요약 수 / 전체 주차 수) × 100 |
| **피드백율** | (받은 피드백 수 / 작성된 요약 수) × 100 |
| **연속 학습 일수** | 연속으로 요약을 작성한 날짜 수 |
| **주간 목표 달성률** | (실제 학습 일수 / 목표 일수) × 100 |

## 권한 관리

### 접근 권한
| 리소스 | 소유자 | 일반 사용자 | 관리자 |
|--------|--------|-------------|--------|
| **요약** | 읽기/쓰기/수정/삭제 | 공개 커리큘럼 읽기만 | 모든 권한 |
| **피드백** | 읽기/삭제 | 공개 커리큘럼 읽기만 | 모든 권한 |
| **통계** | 본인 통계만 | 본인 통계만 | 모든 사용자 통계 |

### 비즈니스 로직
| 작업 | 요구사항 |
|------|----------|
| **요약 작성** | 커리큘럼 소유자, 유효한 주차 |
| **피드백 생성** | 요약 존재, 기존 피드백 없음 |
| **수정/삭제** | 소유자 또는 관리자 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회/수정 성공 |
| `201` | Created | 생성 성공 |
| `204` | No Content | 삭제 성공 |
| `400` | Bad Request | 유효성 검증 실패, 이미 피드백 존재 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 없음 |
| `404` | Not Found | 리소스 없음 |
| `500` | Internal Server Error | AI 피드백 생성 실패 |

## 사용 예시

### 학습 플로우 예시
1. **커리큘럼 선택** → 특정 주차 학습
2. **요약 작성** → `POST /curriculums/{id}/weeks/{week}/summaries`
3. **AI 피드백 요청** → `POST /summaries/{id}/feedbacks/generate`
4. **피드백 확인** → `GET /summaries/{id}/feedbacks`
5. **학습 통계 확인** → `GET /users/me/learning/stats`

### 관리자 모니터링 예시
1. **전체 피드백 현황** → `GET /curriculums/{id}/feedbacks`
2. **점수 분포 분석** → `GET /users/me/feedbacks?min_score=8.0`
3. **학습 패턴 분석** → `GET /users/me/learning/progress`
