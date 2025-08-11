# Feed API Documentation

## API 엔드포인트 목록

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/feed/public` | 공개 커리큘럼 피드 조회 | ✅ |
| POST | `/feed/refresh` | 전체 피드 캐시 갱신 | ✅ (Admin) |
| POST | `/feed/refresh/{curriculum_id}` | 특정 커리큘럼 피드 갱신 | ✅ |

## 피드 (Feed)

### 1. 공개 커리큘럼 피드 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/feed/public` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 20 | 페이지당 항목 수 (최대 50) |
| `category_id` | string | ❌ | - | 카테고리 ID로 필터링 |
| `tags` | string | ❌ | - | 태그로 필터링 (쉼표로 구분) |
| `search` | string | ❌ | - | 제목 또는 작성자로 검색 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"total_count": 100, "page": 1, "items_per_page": 20, "has_next": true, "items": [...]}` |
| `401` | 인증 실패 | 토큰 없음 또는 유효하지 않음 |

**Response Body 구조:**
```json
{
  "total_count": 100,
  "page": 1,
  "items_per_page": 20,
  "has_next": true,
  "items": [
    {
      "curriculum_id": "01HJWXZ123456789ABCDEF0123",
      "title": "Python 기초 과정",
      "owner_id": "01HJWXZ123456789ABCDEF0456",
      "owner_name": "홍길동",
      "total_weeks": 8,
      "total_lessons": 32,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-20T14:20:00Z",
      "category_name": "프로그래밍",
      "category_color": "#3B82F6",
      "tags": ["Python", "초급", "기초"],
      "time_ago": "2시간 전"
    }
  ]
}
```

### 2. 전체 피드 캐시 갱신
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/feed/refresh` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **권한** | ADMIN 권한 필요 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `403` | 권한 없음 (관리자 권한 필요) |

### 3. 특정 커리큘럼 피드 갱신
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/feed/refresh/{curriculum_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 갱신할 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `401` | 인증 실패 |

## 데이터 모델

### FeedItem
| 필드 | 타입 | 설명 |
|------|------|------|
| `curriculum_id` | string | 커리큘럼 ID |
| `title` | string | 커리큘럼 제목 |
| `owner_id` | string | 작성자 ID |
| `owner_name` | string | 작성자 이름 |
| `total_weeks` | integer | 총 주차 수 |
| `total_lessons` | integer | 총 레슨 수 |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |
| `category_name` | string | 카테고리 이름 |
| `category_color` | string | 카테고리 색상 |
| `tags` | array | 태그 목록 |
| `time_ago` | string | 상대 시간 ("2시간 전" 등) |

### FeedPage Response
| 필드 | 타입 | 설명 |
|------|------|------|
| `total_count` | integer | 전체 항목 수 |
| `page` | integer | 현재 페이지 |
| `items_per_page` | integer | 페이지당 항목 수 |
| `has_next` | boolean | 다음 페이지 존재 여부 |
| `items` | array | 피드 아이템 목록 |

## 비즈니스 규칙

### 피드 필터링
| 규칙 | 설명 |
|------|------|
| **공개 커리큘럼만** | `visibility = 'PUBLIC'`인 커리큘럼만 조회 |
| **최신순 정렬** | `updated_at` 기준 내림차순 |
| **캐시 우선** | Redis 캐시 우선, DB 백업 |
| **페이지네이션** | 최대 50개/페이지 제한 |

### 캐시 정책
| 항목 | 설정값 |
|------|--------|
| **캐시 만료시간** | 5분 (300초) |
| **캐시 키** | `feed:public_curriculums` |
| **개별 아이템 키** | `feed:item:{curriculum_id}` |
| **워밍업** | 최신 100개 커리큘럼 |

### 태그 검색
| 규칙 | 설명 |
|------|------|
| **구분자** | 쉼표(,)로 구분 |
| **AND 조건** | 모든 태그를 포함하는 커리큘럼 |
| **대소문자** | 구분 없음 |
| **공백 제거** | 앞뒤 공백 자동 제거 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 피드 조회 성공 |
| `204` | No Content | 캐시 갱신 성공 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 없음 (관리자 전용) |
| `422` | Unprocessable Entity | 잘못된 쿼리 파라미터 |
