# Taxonomy API Documentation

## API 엔드포인트 목록

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/tags` | 태그 생성 | ✅ |
| GET | `/tags` | 태그 목록 조회 | ✅ |
| GET | `/tags/popular` | 인기 태그 조회 | ✅ |
| GET | `/tags/search` | 태그 검색 (자동완성) | ✅ |
| GET | `/tags/statistics` | 태그 통계 | ✅ |
| GET | `/tags/{tag_id}` | 태그 상세 조회 | ✅ |
| PATCH | `/tags/{tag_id}` | 태그 수정 | ✅ |
| DELETE | `/tags/{tag_id}` | 태그 삭제 (관리자만) | ✅ |
| POST | `/categories` | 카테고리 생성 (관리자만) | ✅ |
| GET | `/categories` | 카테고리 목록 조회 | ✅ |
| GET | `/categories/active` | 활성 카테고리 조회 | ✅ |
| GET | `/categories/statistics` | 카테고리 통계 | ✅ |
| GET | `/categories/{category_id}` | 카테고리 상세 조회 | ✅ |
| PATCH | `/categories/{category_id}` | 카테고리 수정 (관리자만) | ✅ |
| DELETE | `/categories/{category_id}` | 카테고리 삭제 (관리자만) | ✅ |
| POST | `/categories/{category_id}/activate` | 카테고리 활성화 | ✅ |
| POST | `/categories/{category_id}/deactivate` | 카테고리 비활성화 | ✅ |
| POST | `/categories/reorder` | 카테고리 순서 변경 | ✅ |
| POST | `/curriculums/{curriculum_id}/tags` | 커리큘럼에 태그 추가 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/tags` | 커리큘럼에서 태그 제거 | ✅ |
| POST | `/curriculums/{curriculum_id}/category` | 커리큘럼에 카테고리 할당 | ✅ |
| DELETE | `/curriculums/{curriculum_id}/category` | 커리큘럼에서 카테고리 제거 | ✅ |
| GET | `/curriculums/{curriculum_id}/tags-and-category` | 커리큘럼 태그/카테고리 조회 | ✅ |
| GET | `/curriculums/search/by-tags` | 태그로 커리큘럼 검색 | ✅ |
| GET | `/curriculums/search/by-category/{category_id}` | 카테고리로 커리큘럼 검색 | ✅ |
| GET | `/curriculums/tags/my-tagged-curriculums` | 내가 태그한 커리큘럼 | ✅ |
| GET | `/curriculums/categories/my-categorized-curriculums` | 내가 분류한 커리큘럼 | ✅ |

## 태그 관리 (Tags)

### 1. 태그 생성
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/tags` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ✅ | 1-20자, 영문/한글/숫자만 허용, 공백 불허 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 생성된 태그 정보 |
| `400` | 유효성 검증 실패 | 태그 이름 규칙 위반 |
| `409` | 중복 태그 | 동일한 이름의 태그 존재 |

### 2. 태그 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/tags` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 20 | 페이지당 항목 수 (최대 50) |
| `search` | string | ❌ | - | 검색어 |
| `min_usage` | integer | ❌ | 1 | 최소 사용 횟수 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 페이지네이션된 태그 목록 |

### 3. 인기 태그 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/tags/popular` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `limit` | integer | ❌ | 20 | 조회할 태그 수 (최대 50) |
| `min_usage` | integer | ❌ | 1 | 최소 사용 횟수 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 사용 횟수 기준 인기 태그 목록 |

### 4. 태그 검색 (자동완성)
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/tags/search` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `q` | string | ✅ | - | 검색 쿼리 (최소 1자) |
| `limit` | integer | ❌ | 10 | 조회할 태그 수 (최대 20) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 자동완성용 태그 목록 |

### 5. 태그 상세 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/tags/{tag_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tag_id` | string | ✅ | 태그 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 태그 상세 정보 |
| `404` | 태그 없음 | - |

### 6. 태그 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PATCH` |
| **URL** | `/tags/{tag_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tag_id` | string | ✅ | 태그 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ❌ | 1-20자, 새 태그 이름 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 수정된 태그 정보 |
| `403` | 권한 없음 | 생성자 또는 관리자만 수정 가능 |
| `409` | 중복 태그 | 동일한 이름의 태그 존재 |

### 7. 태그 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/tags/{tag_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tag_id` | string | ✅ | 태그 ID |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `403` | 권한 없음 (관리자만 삭제 가능) |
| `409` | 태그 사용 중 (삭제 불가) |

### 8. 태그 통계 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/tags/statistics` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 태그 통계 정보 |

## 카테고리 관리 (Categories)

### 9. 카테고리 생성 (관리자만)
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/categories` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ✅ | 2-30자, 영문/한글/숫자/공백/하이픈 허용 |
| `description` | string | ❌ | 최대 500자, 카테고리 설명 |
| `color` | string | ✅ | 헥스 색상 코드 (#FFFFFF) |
| `icon` | string | ❌ | 최대 50자, 아이콘 이름 |
| `sort_order` | integer | ❌ | 정렬 순서 (기본값: 자동 할당) |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 생성된 카테고리 정보 |
| `400` | 유효성 검증 실패 | 색상 형식/이름 규칙 위반 |
| `403` | 권한 없음 | 관리자만 생성 가능 |
| `409` | 중복 카테고리 | 동일한 이름의 카테고리 존재 |

### 10. 활성 카테고리 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/categories/active` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 활성화된 카테고리 목록 (정렬순) |

### 11. 카테고리 목록 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/categories` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 20 | 페이지당 항목 수 (최대 50) |
| `include_inactive` | boolean | ❌ | false | 비활성화된 카테고리 포함 여부 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 페이지네이션된 카테고리 목록 |

### 12. 카테고리 수정 (관리자만)
| 항목 | 내용 |
|------|------|
| **Method** | `PATCH` |
| **URL** | `/categories/{category_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `category_id` | string | ✅ | 카테고리 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ❌ | 2-30자, 새 카테고리 이름 |
| `description` | string | ❌ | 최대 500자, 설명 |
| `color` | string | ❌ | 헥스 색상 코드 |
| `icon` | string | ❌ | 최대 50자, 아이콘 이름 |
| `sort_order` | integer | ❌ | 정렬 순서 |
| `is_active` | boolean | ❌ | 활성화 여부 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 수정된 카테고리 정보 |
| `403` | 권한 없음 | 관리자만 수정 가능 |
| `404` | 카테고리 없음 | - |

### 13. 카테고리 순서 변경 (관리자만)
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/categories/reorder` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `categories` | array | ✅ | 순서 변경할 카테고리 목록 |
| `categories[].id` | string | ✅ | 카테고리 ID |
| `categories[].sort_order` | integer | ✅ | 새 정렬 순서 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `403` | 권한 없음 | 관리자만 변경 가능 |

## 커리큘럼 태그/카테고리 관리

### 14. 커리큘럼에 태그 추가
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/tags` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `tag_names` | array | ✅ | 1-10개, 추가할 태그 이름들 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 추가된 태그 목록 |
| `400` | 태그 개수 제한 초과 | 최대 10개 제한 |
| `403` | 권한 없음 | 본인 커리큘럼만 태그 추가 가능 |

### 15. 커리큘럼에서 태그 제거
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/curriculums/{curriculum_id}/tags` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tag_name` | string | ✅ | 제거할 태그 이름 |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `403` | 권한 없음 | 본인 커리큘럼만 수정 가능 |
| `404` | 태그 없음 | - |

### 16. 커리큘럼에 카테고리 할당
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/curriculums/{curriculum_id}/category` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Request Body:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `category_id` | string | ✅ | 할당할 카테고리 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | 할당된 카테고리 정보 |
| `400` | 비활성 카테고리 | 활성화된 카테고리만 할당 가능 |
| `403` | 권한 없음 | 본인 커리큘럼만 수정 가능 |

### 17. 커리큘럼 태그/카테고리 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/{curriculum_id}/tags-and-category` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `curriculum_id` | string | ✅ | 커리큘럼 ID |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 커리큘럼의 태그와 카테고리 정보 |
| `404` | 커리큘럼 없음 | - |

## 검색 및 발견

### 18. 태그로 커리큘럼 검색
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/search/by-tags` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `tag_names` | array | ✅ | 검색할 태그 이름들 (교집합) |
| `page` | integer | ❌ | 페이지 번호 |
| `items_per_page` | integer | ❌ | 페이지당 항목 수 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 매칭되는 커리큘럼 ID 목록 |

### 19. 카테고리로 커리큘럼 검색
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/curriculums/search/by-category/{category_id}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `category_id` | string | ✅ | 카테고리 ID |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 10 | 페이지당 항목 수 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | 해당 카테고리의 커리큘럼 ID 목록 |

## 데이터 모델

### Tag 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 태그 ID |
| `name` | string | 태그 이름 (1-20자, 영문/한글/숫자) |
| `usage_count` | integer | 사용 횟수 |
| `is_popular` | boolean | 인기 태그 여부 (사용횟수 ≥ 10) |
| `created_by` | string | 생성자 사용자 ID |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### Category 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 카테고리 ID |
| `name` | string | 카테고리 이름 (2-30자) |
| `description` | string | 카테고리 설명 (최대 500자) |
| `color` | string | 헥스 색상 코드 (#FFFFFF) |
| `icon` | string | 아이콘 이름 (최대 50자) |
| `sort_order` | integer | 정렬 순서 |
| `is_active` | boolean | 활성화 여부 |
| `usage_count` | integer | 사용 횟수 |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

### CurriculumTags 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `curriculum_id` | string | 커리큘럼 ID |
| `tags` | array | 연결된 태그 목록 |
| `category` | object | 할당된 카테고리 (1:1 관계) |

### Statistics 객체
| 필드 | 타입 | 설명 |
|------|------|------|
| `total_tags` | integer | 전체 태그 수 |
| `popular_tags_count` | integer | 인기 태그 수 |
| `unused_tags_count` | integer | 미사용 태그 수 |
| `most_popular_tags` | array | 최고 인기 태그 이름들 |
| `total_categories` | integer | 전체 카테고리 수 |
| `active_categories` | integer | 활성 카테고리 수 |
| `inactive_categories` | integer | 비활성 카테고리 수 |

## 비즈니스 규칙

### 태그 (Tag) 제약사항
| 규칙 | 설명 |
|------|------|
| **이름 길이** | 1-20자 |
| **허용 문자** | 영문, 한글, 숫자만 허용 (공백 불허) |
| **정규화** | 소문자로 자동 변환 |
| **중복** | 동일 이름 태그 생성 불가 |
| **자동 생성** | 커리큘럼 태깅 시 없는 태그 자동 생성 |

### 카테고리 (Category) 제약사항
| 규칙 | 설명 |
|------|------|
| **이름 길이** | 2-30자 |
| **허용 문자** | 영문, 한글, 숫자, 공백, 하이픈 허용 |
| **색상 형식** | 헥스 색상 코드 필수 (#FFFFFF) |
| **정렬 순서** | 자동 할당 또는 수동 설정 |
| **활성화 상태** | 비활성 카테고리는 할당 불가 |

### 커리큘럼 연결 제약사항
| 규칙 | 설명 |
|------|------|
| **태그 개수** | 커리큘럼당 최대 10개 태그 |
| **카테고리 개수** | 커리큘럼당 1개 카테고리 (1:1 관계) |
| **권한** | 커리큘럼 소유자만 태그/카테고리 관리 가능 |
| **사용 횟수** | 태그 연결/해제 시 자동 증감 |

### 태그 인기도 기준
| 사용 횟수 | 분류 |
|-----------|------|
| 10회 이상 | 인기 태그 |
| 1-9회 | 일반 태그 |
| 0회 | 미사용 태그 |

### 삭제 정책
| 리소스 | 삭제 조건 |
|--------|----------|
| **태그** | 사용 횟수가 0인 태그만 삭제 가능 (관리자만) |
| **카테고리** | 사용 중이지 않은 카테고리만 삭제 가능 (관리자만) |
| **커리큘럼 연결** | 소유자가 언제든 해제 가능 |

## 권한 관리

### 태그 권한
| 작업 | 일반 사용자 | 생성자 | 관리자 |
|------|-------------|--------|--------|
| **생성** | ✅ | ✅ | ✅ |
| **조회** | ✅ | ✅ | ✅ |
| **수정** | ❌ | ✅ | ✅ |
| **삭제** | ❌ | ❌ | ✅ |

### 카테고리 권한
| 작업 | 일반 사용자 | 관리자 |
|------|-------------|--------|
| **생성** | ❌ | ✅ |
| **조회** | ✅ | ✅ |
| **수정** | ❌ | ✅ |
| **삭제** | ❌ | ✅ |
| **활성화/비활성화** | ❌ | ✅ |
| **순서 변경** | ❌ | ✅ |

### 커리큘럼 연결 권한
| 작업 | 소유자 | 일반 사용자 | 관리자 |
|------|--------|-------------|--------|
| **태그 추가/제거** | ✅ | ❌ | ✅ |
| **카테고리 할당/해제** | ✅ | ❌ | ✅ |
| **조회** | ✅ | 공개 커리큘럼만 | ✅ |

## 검색 및 필터링

### 태그 검색 기능
| 기능 | 설명 |
|------|------|
| **이름 검색** | 부분 문자열 매칭 (LIKE 검색) |
| **인기도 필터** | 최소 사용 횟수 기준 필터링 |
| **자동완성** | 검색어 기반 태그 제안 |
| **정렬** | 사용 횟수 내림차순 → 이름 오름차순 |

### 카테고리 검색 기능
| 기능 | 설명 |
|------|------|
| **활성 상태 필터** | 활성/비활성 카테고리 분류 |
| **정렬** | sort_order 오름차순 → 이름 오름차순 |
| **사용 통계** | 각 카테고리별 사용 횟수 포함 |

### 커리큘럼 검색 기능
| 기능 | 설명 |
|------|------|
| **태그 기반 검색** | 여러 태그의 교집합 검색 |
| **카테고리 기반 검색** | 특정 카테고리의 모든 커리큘럼 |
| **사용자 활동 추적** | 내가 태깅/분류한 커리큘럼 목록 |

## 사용 사례

### 일반적인 태깅 플로우
1. **커리큘럼 생성** → 새 커리큘럼 작성
2. **태그 추가** → `POST /curriculums/{id}/tags` (기존 태그 또는 자동 생성)
3. **카테고리 할당** → `POST /curriculums/{id}/category`
4. **검색 활용** → `GET /curriculums/search/by-tags` 또는 `/by-category/{id}`

### 관리자 카테고리 관리 플로우
1. **카테고리 생성** → `POST /categories`
2. **순서 조정** → `POST /categories/reorder`
3. **활성화 관리** → `POST /categories/{id}/activate` 또는 `/deactivate`
4. **사용 통계 확인** → `GET /categories/statistics`

### 사용자 태그 발견 플로우
1. **인기 태그 조회** → `GET /tags/popular`
2. **태그 검색** → `GET /tags/search?q=검색어`
3. **태그 상세 확인** → `GET /tags/{id}`
4. **커리큘럼에 적용** → `POST /curriculums/{id}/tags`

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회/수정 성공 |
| `201` | Created | 생성 성공 |
| `204` | No Content | 삭제/해제 성공 |
| `400` | Bad Request | 유효성 검증 실패, 태그 개수 제한 초과 |
| `401` | Unauthorized | 인증 실패 |
| `403` | Forbidden | 권한 없음 (관리자 전용 기능, 소유자 전용 기능) |
| `404` | Not Found | 리소스 없음 |
| `409` | Conflict | 중복 이름, 태그/카테고리 사용 중 (삭제 불가) |

## 모니터링 및 분석

### 추적 가능한 메트릭
| 메트릭 | 설명 |
|--------|------|
| `curriculum_tag_assignment` | 커리큘럼 태그 할당 횟수 |
| `curriculum_category_assignment` | 커리큘럼 카테고리 할당 횟수 |
| `tag_creation` | 새 태그 생성 횟수 |
| `tag_usage_count` | 태그별 사용 횟수 |
| `category_usage_count` | 카테고리별 사용 횟수 |

### 통계 정보
| 통계 | 제공 정보 |
|------|----------|
| **태그 통계** | 전체/인기/미사용 태그 수, 최고 인기 태그 |
| **카테고리 통계** | 전체/활성/비활성 카테고리 수 |
| **사용자 활동** | 개인별 태깅/분류 활동 내역 |

## 성능 최적화

### 데이터베이스 인덱스
| 테이블 | 인덱스 | 목적 |
|--------|--------|------|
| `tags` | `name`, `usage_count`, `created_by` | 검색 및 정렬 최적화 |
| `categories` | `active_sort`, `name` | 활성 카테고리 조회 최적화 |
| `curriculum_tags` | `curriculum_id`, `tag_id`, `added_by` | 연결 관계 조회 최적화 |
| `curriculum_categories` | `curriculum_id`, `category_id` | 1:1 관계 조회 최적화 |

### 캐싱 전략
| 데이터 | 캐싱 방식 | TTL |
|--------|----------|-----|
| **인기 태그** | 메모리 캐시 | 1시간 |
| **활성 카테고리** | 메모리 캐시 | 30분 |
| **태그 통계** | 메모리 캐시 | 6시간 |
| **카테고리 통계** | 메모리 캐시 | 6시간 |

## 확장성 고려사항

### 향후 확장 가능 기능
| 기능 | 설명 |
|------|------|
| **태그 계층구조** | 부모-자식 태그 관계 |
| **태그 동의어** | 유사한 의미의 태그 그룹화 |
| **자동 태그 추천** | AI 기반 태그 자동 제안 |
| **태그 분석** | 태그 트렌드 및 관련성 분석 |
| **카테고리 트리** | 다단계 카테고리 구조 |

### 스케일링 고려사항
| 항목 | 고려사항 |
|------|----------|
| **태그 수 증가** | 검색 성능 최적화, 샤딩 고려 |
| **태깅 요청 증가** | 비동기 처리, 배치 업데이트 |
| **검색 요청 증가** | 검색 엔진 도입 (Elasticsearch) |
| **통계 계산** | 실시간 → 배치 처리로 전환 |
