# Admin API Documentation

## API 엔드포인트 목록

### 사용자 관리 (Admin Users)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/admin/users` | 사용자 목록 조회 | ✅ (Admin) |
| GET | `/admin/users/{user_id}` | 사용자 상세 조회 | ✅ (Admin) |
| PATCH | `/admin/users/{user_id}/role` | 사용자 역할 변경 | ✅ (Admin) |

### 커리큘럼 관리 (Admin Curriculums)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/admin/curriculums` | 커리큘럼 목록 조회 | ✅ (Admin) |
| GET | `/admin/curriculums/{curriculum_id}` | 커리큘럼 상세 조회 | ✅ (Admin) |
| PATCH | `/admin/curriculums/{curriculum_id}/visibility` | 공개/비공개 변경 | ✅ (Admin) |
| DELETE | `/admin/curriculums/{curriculum_id}` | 커리큘럼 삭제 | ✅ (Admin) |

## 사용자 관리 (Admin Users) API

### 1. 사용자 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/admin/users` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 사용자 목록 |
| `403` | 권한 없음 | 관리자 권한 필요 |

**Response Body 구조:**
```json
{
  "items": [
    {
      "user_id": "01HJWXZ123456789ABCDEF0123",
      "role": "USER",
      "email": "hong@example.com",
      "name": "홍길동"
    }
  ],
  "total": 150,
  "page": 1,
  "items_per_page": 10
}
```

### 2. 사용자 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/admin/users/{user_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `user_id` | string | ✅ | 조회할 사용자 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 사용자 상세 정보 |
| `404` | 사용자 없음 | - |

**Response Body 구조:**
```json
{
  "user_id": "01HJWXZ123456789ABCDEF0123",
  "role": "USER",
  "email": "hong@example.com",
  "name": "홍길동"
}
```

### 3. 사용자 역할 변경
| 항목 | 내용 |
|------|------|
| **Method** | `PATCH` |
| **URL** | `/admin/users/{user_id}/role` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |
| **권한** | ADMIN 권한 필요 |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `user_id` | string | ✅ | 역할을 변경할 사용자 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `role` | string | ✅ | "USER" 또는 "ADMIN" |

**Request Body 예시:**
```json
{
  "role": "ADMIN"
}
```

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 변경된 사용자 정보 |
| `404` | 사용자 없음 | - |
| `422` | 잘못된 역할 | 유효하지 않은 역할 값 |

## 커리큘럼 관리 (Admin Curriculums) API

### 1. 커리큘럼 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/admin/curriculums` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |
| `owner_id` | string | ❌ | - | 특정 소유자의 커리큘럼만 조회 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 커리큘럼 목록 |
| `403` | 권한 없음 | 관리자 권한 필요 |

**Response Body 구조:**
```json
{
  "curriculums": [
    {
      "curriculum_id": "01HJWXZ123456789ABCDEF0123",
      "owner_id": "01HJWXZ123456789ABCDEF0456",
      "title": "Python 기초 과정",
      "visibility": "PUBLIC"
    }
  ],
  "total_count": 250,
  "page": 1,
  "items_per_page": 10
}
```

### 2. 커리큘럼 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/admin/curriculums/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 조회할 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 커리큘럼 상세 정보 |
| `404` | 커리큘럼 없음 | - |

**Response Body 구조:**
```json
{
  "curriculum_id": "01HJWXZ123456789ABCDEF0123",
  "owner_id": "01HJWXZ123456789ABCDEF0456",
  "title": "Python 기초 과정",
  "visibility": "PUBLIC"
}
```

### 3. 커리큘럼 공개/비공개 변경
| 항목 | 내용 |
|------|------|
| **Method** | `PATCH` |
| **URL** | `/admin/curriculums/{curriculum_id}/visibility` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |
| **권한** | ADMIN 권한 필요 |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 변경할 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `visibility` | string | ✅ | "PUBLIC" 또는 "PRIVATE" |

**Request Body 예시:**
```json
{
  "visibility": "PRIVATE"
}
```

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 변경된 커리큘럼 정보 |
| `404` | 커리큘럼 없음 | - |
| `422` | 잘못된 공개 설정 | 유효하지 않은 visibility 값 |

### 4. 커리큘럼 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/admin/curriculums/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 삭제할 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 커리큘럼 없음 |

## 데이터 모델

### AdminUserItem
| 필드 | 타입 | 설명 |
|------|------|------|
| `user_id` | string | 사용자 ID |
| `role` | string | 사용자 역할 (USER, ADMIN) |
| `email` | string | 이메일 주소 |
| `name` | string | 사용자 이름 |

### AdminCurriculumItem
| 필드 | 타입 | 설명 |
|------|------|------|
| `curriculum_id` | string | 커리큘럼 ID |
| `owner_id` | string | 소유자 ID |
| `title` | string | 커리큘럼 제목 |
| `visibility` | string | 공개 설정 (PUBLIC, PRIVATE) |

### AdminUsersPageResponse
| 필드 | 타입 | 설명 |
|------|------|------|
| `items` | array | 사용자 목록 |
| `total` | integer | 전체 사용자 수 |
| `page` | integer | 현재 페이지 |
| `items_per_page` | integer | 페이지당 항목 수 |

### AdminCurriculumsPageResponse
| 필드 | 타입 | 설명 |
|------|------|------|
| `curriculums` | array | 커리큘럼 목록 |
| `total_count` | integer | 전체 커리큘럼 수 |
| `page` | integer | 현재 페이지 |
| `items_per_page` | integer | 페이지당 항목 수 |

## 비즈니스 규칙

### 관리자 권한 검증
| 규칙 | 설명 |
|------|------|
| **필수 권한** | ADMIN 역할 필요 |
| **모든 엔드포인트** | 관리자 권한 체크 |
| **권한 실패 시** | 403 Forbidden 반환 |
| **토큰 검증** | 유효한 인증 토큰 필요 |

### 사용자 역할 관리
| 규칙 | 설명 |
|------|------|
| **역할 종류** | USER, ADMIN |
| **기본 역할** | 신규 사용자는 USER |
| **역할 변경** | 관리자만 가능 |
| **자기 역할 변경** | 불가능 (다른 관리자를 통해서만) |

### 커리큘럼 관리
| 규칙 | 설명 |
|------|------|
| **공개 설정** | PUBLIC, PRIVATE |
| **강제 변경** | 관리자가 소유자 의사와 관계없이 변경 가능 |
| **삭제 권한** | 관리자만 삭제 가능 |
| **연관 데이터** | 커리큘럼 삭제 시 관련 소셜 데이터도 함께 삭제 |

### 페이지네이션
| 규칙 | 설명 |
|------|------|
| **최대 페이지 크기** | 100개/페이지 |
| **기본 페이지 크기** | 10개/페이지 |
| **최소 페이지** | 1 |
| **정렬 순서** | 생성일시 기준 내림차순 |

### 필터링
| 기능 | 설명 |
|------|------|
| **사용자 목록** | 역할별 필터링 가능 |
| **커리큘럼 목록** | 소유자별 필터링 가능 |
| **검색 기능** | 향후 확장 예정 |
| **날짜 범위** | 향후 확장 예정 |

## 보안 및 감사

### 접근 로그
| 항목 | 설명 |
|------|------|
| **모든 관리자 작업** | 로그 기록 |
| **사용자 역할 변경** | 변경 이력 추적 |
| **커리큘럼 삭제** | 삭제 로그 보관 |
| **권한 위반 시도** | 보안 로그 기록 |

### 데이터 보호
| 규칙 | 설명 |
|------|------|
| **민감 정보** | 비밀번호 등 민감 정보 미포함 |
| **개인정보** | 필요 최소한의 정보만 노출 |
| **삭제된 데이터** | 복구 불가능한 완전 삭제 |
| **백업 정책** | 관리자 작업 전 자동 백업 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회/수정 성공 |
| `204` | No Content | 삭제 성공 |
| `400` | Bad Request | 잘못된 요청 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 관리자 권한 없음 |
| `404` | Not Found | 리소스 없음 |
| `422` | Unprocessable Entity | 유효성 검증 실패 |
| `500` | Internal Server Error | 서버 오류 |

## 에러 응답 형식

### 권한 없음 (403)
```json
{
  "detail": "Admin access required"
}
```

### 리소스 없음 (404)
```json
{
  "detail": "User not found"
}
```

### 유효성 검증 실패 (422)
```json
{
  "detail": "invalid role: INVALID_ROLE"
}
```

## 사용 예시

### 사용자 목록 조회
```bash
curl -X GET "https://api.example.com/admin/users?page=1&items_per_page=20" \
  -H "Authorization: Bearer your_admin_token"
```

### 사용자 역할 변경
```bash
curl -X PATCH "https://api.example.com/admin/users/01HJWXZ123456789ABCDEF0123/role" \
  -H "Authorization: Bearer your_admin_token" \
  -H "Content-Type: application/json" \
  -d '{"role": "ADMIN"}'
```

### 커리큘럼 비공개 처리
```bash
curl -X PATCH "https://api.example.com/admin/curriculums/01HJWXZ123456789ABCDEF0456/visibility" \
  -H "Authorization: Bearer your_admin_token" \
  -H "Content-Type: application/json" \
  -d '{"visibility": "PRIVATE"}'
```

### 커리큘럼 삭제
```bash
curl -X DELETE "https://api.example.com/admin/curriculums/01HJWXZ123456789ABCDEF0456" \
  -H "Authorization: Bearer your_admin_token"
```
