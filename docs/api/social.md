# Social API Documentation

## API 엔드포인트 목록

### 좋아요 (Like)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/curriculums/{curriculum_id}/like` | 커리큘럼 좋아요 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/like` | 좋아요 취소 | ✅ |
| GET | `/curriculums/{curriculum_id}/likes` | 좋아요 목록 조회 | ✅ |
| GET | `/curriculums/{curriculum_id}/like/status` | 좋아요 상태 조회 | ✅ |
| GET | `/users/me/likes` | 내 좋아요 목록 | ✅ |

### 댓글 (Comment)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/curriculums/{curriculum_id}/comments` | 댓글 작성 | ✅ |
| GET | `/curriculums/{curriculum_id}/comments` | 댓글 목록 조회 | ✅ |
| GET | `/curriculums/comments/{comment_id}` | 댓글 상세 조회 | ✅ |
| PUT | `/curriculums/comments/{comment_id}` | 댓글 수정 | ✅ |
| DELETE | `/curriculums/comments/{comment_id}` | 댓글 삭제 | ✅ |
| GET | `/users/me/comments` | 내 댓글 목록 | ✅ |

### 북마크 (Bookmark)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/curriculums/{curriculum_id}/bookmark` | 북마크 추가 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/bookmark` | 북마크 제거 | ✅ |
| GET | `/curriculums/{curriculum_id}/bookmark/status` | 북마크 상태 조회 | ✅ |
| GET | `/users/me/bookmarks` | 내 북마크 목록 | ✅ |

### 팔로우 (Follow)
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/social/follow` | 사용자 팔로우 | ✅ |
| DELETE | `/social/unfollow` | 사용자 언팔로우 | ✅ |
| GET | `/social/users/{user_id}/followers` | 팔로워 목록 조회 | ✅ |
| GET | `/social/users/{user_id}/following` | 팔로잉 목록 조회 | ✅ |
| GET | `/social/me/followers` | 내 팔로워 목록 | ✅ |
| GET | `/social/me/following` | 내 팔로잉 목록 | ✅ |
| GET | `/social/users/{user_id}/stats` | 팔로우 통계 조회 | ✅ |
| GET | `/social/users/{user_id}/status` | 팔로우 상태 조회 | ✅ |
| GET | `/social/suggestions` | 팔로우 추천 목록 | ✅ |

### 통합 통계
| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/curriculums/{curriculum_id}/social-stats` | 커리큘럼 소셜 통계 | ✅ |

## 좋아요 (Like) API

### 1. 커리큘럼 좋아요
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/like` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
```json
{}
```

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | `{"id": "01HJWXZ...", "curriculum_id": "01HJWXZ...", "user_id": "01HJWXZ...", "created_at": "2025-01-15T10:30:00Z"}` |
| `409` | 중복 | 이미 좋아요한 커리큘럼 |
| `404` | 커리큘럼 없음 | 접근할 수 없는 커리큘럼 |

### 2. 좋아요 취소
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/{curriculum_id}/like` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 좋아요 없음 |

### 3. 좋아요 상태 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/like/status` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
```json
{
  "is_liked": true,
  "like_count": 15
}
```

## 댓글 (Comment) API

### 1. 댓글 작성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/comments` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `content` | string | ✅ | 1-1000자 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 댓글 정보 |
| `400` | 유효성 검증 실패 | 내용 길이 위반 |
| `404` | 커리큘럼 없음 | 접근할 수 없는 커리큘럼 |

### 2. 댓글 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/comments` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 (최대 50) |

**Response:**
```json
{
  "total_count": 25,
  "page": 1,
  "items_per_page": 10,
  "comments": [
    {
      "id": "01HJWXZ123456789ABCDEF0123",
      "curriculum_id": "01HJWXZ123456789ABCDEF0456",
      "user_id": "01HJWXZ123456789ABCDEF0789",
      "user_name": "홍길동",
      "content_snippet": "정말 좋은 커리큘럼이네요...",
      "content_length": 150,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### 3. 댓글 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PUT` |
| **URL** | `/curriculums/comments/{comment_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `content` | string | ✅ | 1-1000자 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `200` | 성공 |
| `403` | 권한 없음 (자신의 댓글만 수정 가능) |
| `404` | 댓글 없음 |

## 북마크 (Bookmark) API

### 1. 북마크 추가
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/bookmark` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `201` | 성공 |
| `409` | 중복 |
| `404` | 커리큘럼 없음 |

### 2. 북마크 상태 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/bookmark/status` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
```json
{
  "is_bookmarked": true
}
```

## 팔로우 (Follow) API

### 1. 사용자 팔로우
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/social/follow` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `followee_id` | string | ✅ | 팔로우할 사용자 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `201` | 성공 |
| `400` | 자기 자신 팔로우 시도 |
| `409` | 이미 팔로우 중 |
| `404` | 사용자 없음 |

### 2. 팔로워 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/social/users/{user_id}/followers` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
```json
{
  "total_count": 15,
  "page": 1,
  "items_per_page": 10,
  "followers": [
    {
      "user_id": "01HJWXZ123456789ABCDEF0123",
      "username": "홍길동",
      "email": "hong@example.com",
      "followers_count": 20,
      "followees_count": 10,
      "is_following": true,
      "is_followed_by": false
    }
  ]
}
```

### 3. 팔로우 통계 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/social/users/{user_id}/stats` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
```json
{
  "user_id": "01HJWXZ123456789ABCDEF0123",
  "followers_count": 15,
  "followees_count": 8,
  "mutual_followers_count": null
}
```

## 통합 통계 API

### 1. 커리큘럼 소셜 통계
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/social-stats` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
```json
{
  "curriculum_id": "01HJWXZ123456789ABCDEF0123",
  "like_count": 25,
  "comment_count": 8,
  "is_liked_by_user": true,
  "is_bookmarked_by_user": false
}
```

## 데이터 모델

### Like DTO
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 좋아요 ID |
| `curriculum_id` | string | 커리큘럼 ID |
| `user_id` | string | 사용자 ID |
| `created_at` | datetime | 생성일시 |

### Comment DTO
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 댓글 ID |
| `curriculum_id` | string | 커리큘럼 ID |
| `user_id` | string | 작성자 ID |
| `content` | string | 댓글 내용 |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### Follow DTO
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 팔로우 ID |
| `follower_id` | string | 팔로워 ID |
| `followee_id` | string | 팔로위 ID |
| `created_at` | datetime | 팔로우일시 |

## 비즈니스 규칙

### 댓글 검증
| 규칙 | 설명 |
|------|------|
| **길이** | 1-1000자 |
| **내용** | 공백만으로 구성 불가 |
| **수정 권한** | 작성자 또는 관리자만 |
| **삭제 권한** | 작성자 또는 관리자만 |

### 팔로우 규칙
| 규칙 | 설명 |
|------|------|
| **자기 팔로우** | 불가능 |
| **중복 팔로우** | 불가능 |
| **상호 팔로우** | 가능 |
| **팔로우 추천** | 2차 연결 기반 |

### 접근 권한
| 기능 | 권한 |
|------|------|
| **공개 커리큘럼** | 모든 사용자 |
| **비공개 커리큘럼** | 소유자, 관리자만 |
| **자신의 소셜 활동** | 본인만 조회 |
| **타인의 소셜 활동** | 관리자만 조회 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회 성공 |
| `201` | Created | 생성 성공 |
| `204` | No Content | 삭제 성공 |
| `400` | Bad Request | 잘못된 요청 (자기 팔로우 등) |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 없음 |
| `404` | Not Found | 리소스 없음 |
| `409` | Conflict | 중복 (이미 좋아요/팔로우) |
| `422` | Unprocessable Entity | 유효성 검증 실패 |
