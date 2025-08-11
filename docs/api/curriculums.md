# Curriculum API Documentation

## API 엔드포인트 목록

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/curriculums` | 커리큘럼 생성 | ✅ |
| POST | `/curriculums/generate` | AI 커리큘럼 생성 | ✅ |
| GET | `/curriculums/me` | 내 커리큘럼 목록 | ✅ |
| GET | `/curriculums/public` | 공개 커리큘럼 목록 | ✅ |
| GET | `/curriculums/following` | 팔로우 사용자 커리큘럼 | ✅ |
| GET | `/curriculums/{curriculum_id}` | 커리큘럼 상세 조회 | ✅ |
| PATCH | `/curriculums/{curriculum_id}` | 커리큘럼 수정 | ✅ |
| DELETE | `/curriculums/{curriculum_id}` | 커리큘럼 삭제 | ✅ |
| POST | `/curriculums/{curriculum_id}/weeks` | 주차 스케줄 생성 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/weeks/{week_number}` | 주차 스케줄 삭제 | ✅ |
| POST | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons` | 레슨 생성 | ✅ |
| PUT | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}` | 레슨 수정 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}` | 레슨 삭제 | ✅ |

## 커리큘럼 관리 (Curriculums)

### 1. 커리큘럼 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `title` | string | ✅ | 2-50자, 커리큘럼 제목 |
| `week_schedules` | array | ✅ | 최소 1개 주차, 주차별 스케줄 |
| `visibility` | string | ❌ | PUBLIC/PRIVATE (기본값: PRIVATE) |

**WeekSchedule 객체:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `week_number` | integer | ✅ | 1-24, 주차 번호 |
| `title` | string | ❌ | 2-50자, 주차 제목 |
| `lessons` | array | ✅ | 1-5개, 수업 목록 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 생성된 커리큘럼 정보 |
| `400` | 유효성 검증 실패 | 제목/주차/레슨 규칙 위반 |
| `403` | 권한 없음 | 최대 10개 제한 초과 |

### 2. AI 커리큘럼 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/generate` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `goal` | string | ✅ | 학습 목표 (예: "Python 백엔드 개발") |
| `period` | integer | ✅ | 1-24, 기간(주 단위) |
| `difficulty` | string | ✅ | beginner/intermediate/expert |
| `details` | string | ❌ | 추가 세부사항 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | AI 생성된 커리큘럼 정보 |
| `400` | 유효성 검증 실패 | 난이도/기간 등 규칙 위반 |
| `500` | LLM 생성 실패 | AI 서비스 오류 |

### 3. 내 커리큘럼 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/me` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 페이지네이션된 커리큘럼 목록 |

### 4. 공개 커리큘럼 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/public` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 공개 커리큘럼 목록 |

### 5. 팔로우 사용자 커리큘럼 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/following` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 팔로우한 사용자들의 공개 커리큘럼 |

### 6. 커리큘럼 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 커리큘럼 상세 정보 |
| `404` | 커리큘럼 없음 | - |
| `403` | 접근 권한 없음 | 비공개 커리큘럼 |

### 7. 커리큘럼 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PATCH` |
| **URL** | `/curriculums/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `title` | string | ❌ | 2-50자, 새 제목 |
| `visibility` | string | ❌ | PUBLIC/PRIVATE |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 수정된 커리큘럼 정보 |
| `404` | 커리큘럼 없음 | - |
| `403` | 권한 없음 | 본인 커리큘럼만 수정 가능 |

### 8. 커리큘럼 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 커리큘럼 없음 |
| `403` | 권한 없음 |

## 주차 관리 (Weeks)

### 9. 주차 스케줄 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/weeks` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `week_number` | integer | ✅ | 1-24, 삽입할 주차 번호 |
| `lessons` | array | ✅ | 1-5개, 레슨 목록 |
| `title` | string | ❌ | 2-50자, 주차 제목 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 업데이트된 커리큘럼 정보 |
| `400` | 유효성 검증 실패 | 주차 번호/레슨 규칙 위반 |
| `403` | 권한 없음 | 본인 커리큘럼만 수정 가능 |

### 10. 주차 스케줄 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 삭제할 주차 번호 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 주차 없음 |
| `403` | 권한 없음 |

## 레슨 관리 (Lessons)

### 11. 레슨 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 주차 번호 |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `lesson` | string | ✅ | 1-100자, 레슨 내용 |
| `lesson_index` | integer | ❌ | 삽입 위치 (기본값: 마지막) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 업데이트된 커리큘럼 정보 |
| `400` | 유효성 검증 실패 | 인덱스 범위 초과 |
| `404` | 주차 없음 | - |

### 12. 레슨 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PUT` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 주차 번호 |
| `lesson_index` | integer | ✅ | 레슨 인덱스 |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `lesson` | string | ✅ | 1-100자, 새 레슨 내용 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 업데이트된 커리큘럼 정보 |
| `400` | 유효성 검증 실패 | 인덱스 범위 초과 |
| `404` | 주차/레슨 없음 | - |

### 13. 레슨 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |
| `week_number` | integer | ✅ | 주차 번호 |
| `lesson_index` | integer | ✅ | 레슨 인덱스 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `400` | 인덱스 범위 초과 |
| `404` | 주차/레슨 없음 |

## 데이터 모델

### Curriculum 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 커리큘럼 ID |
| `owner_id` | string | 소유자 사용자 ID |
| `title` | string | 커리큘럼 제목 |
| `visibility` | string | 공개 설정 (PUBLIC/PRIVATE) |
| `week_schedules` | array | 주차별 스케줄 목록 |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### WeekSchedule 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `week_number` | integer | 주차 번호 (1-24) |
| `title` | string | 주차 제목 |
| `lessons` | array | 레슨 목록 (1-5개) |

### CurriculumPage 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `total_count` | integer | 전체 항목 수 |
| `page` | integer | 현재 페이지 |
| `items_per_page` | integer | 페이지당 항목 수 |
| `curriculums` | array | 커리큘럼 목록 |

## 비즈니스 규칙

### 커리큘럼 제약사항
| 규칙 | 설명 |
|------|------|
| **제목** | 2-50자 |
| **개수 제한** | 사용자당 최대 10개 |
| **주차 수** | 1-24주 |
| **공개 설정** | PUBLIC(공개)/PRIVATE(비공개) |

### 주차 스케줄 제약사항
| 규칙 | 설명 |
|------|------|
| **주차 번호** | 1-24, 연속적이어야 함 |
| **제목** | 2-50자 |
| **레슨 수** | 1-5개 |

### 레슨 제약사항
| 규칙 | 설명 |
|------|------|
| **내용** | 1-100자 |
| **개수** | 주차당 1-5개 |

### 난이도 (Difficulty)
| 값 | 설명 |
|-----|------|
| `beginner` | 초급 |
| `intermediate` | 중급 |
| `expert` | 고급 |

### 공개 설정 (Visibility)
| 값 | 설명 |
|-----|------|
| `PUBLIC` | 모든 사용자가 조회 가능 |
| `PRIVATE` | 소유자만 조회 가능 |

## 권한 관리

### 접근 권한
| 역할 | 권한 |
|------|------|
| **소유자** | 모든 작업 가능 (CRUD) |
| **일반 사용자** | 공개 커리큘럼 조회만 가능 |
| **관리자** | 모든 커리큘럼 접근 가능 |

### 수정 권한
| 작업 | 권한 요구사항 |
|------|---------------|
| **생성/수정/삭제** | 소유자 또는 관리자 |
| **조회** | 소유자, 관리자 또는 공개 커리큘럼 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회/수정 성공 |
| `201` | Created | 생성 성공 |
| `204` | No Content | 삭제 성공 |
| `400` | Bad Request | 유효성 검증 실패 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 없음 |
| `404` | Not Found | 리소스 없음 |
| `500` | Internal Server Error | LLM 생성 실패 등 |
