# User API Documentation

## API 엔드포인트 목록

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/auth/signup` | 회원가입 | ❌ |
| POST | `/auth/login` | 로그인 | ❌ |
| GET | `/users/me` | 내 정보 조회 | ✅ |
| PUT | `/users/me` | 내 정보 수정 | ✅ |
| DELETE | `/users/me` | 계정 삭제 | ✅ |
| GET | `/users` | 사용자 목록 조회 | ✅ |
| GET | `/users/{user_name}` | 사용자명으로 조회 | ✅ |

## 인증 (Authentication)

### 1. 회원가입
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/auth/signup` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ✅ | 2-32자, 한글/영문/숫자만 허용 |
| `email` | string | ✅ | 이메일 형식, 최대 64자, 중복 불가 |
| `password` | string | ✅ | 8-64자, 대소문자+숫자+특수문자 포함 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `201` | 성공 | `{"name": "홍길동", "email": "hong@example.com", "created_at": "2025-01-15T10:30:00Z"}` |
| `400` | 유효성 검증 실패 | 이메일 중복, 이름 중복, 비밀번호 규칙 위반 |

### 2. 로그인
| 항목 | 내용 |
|------|------|
| **Method** | `POST` |
| **URL** | `/auth/login` |
| **Content-Type** | `application/x-www-form-urlencoded` |

**Request Body (Form Data):**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `username` | string | ✅ | 이메일 주소 |
| `password` | string | ✅ | 비밀번호 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"access_token": "jwt_token", "token_type": "bearer", "role": "USER"}` |
| `401` | 인증 실패 | 이메일 없음 또는 비밀번호 불일치 |

## 사용자 관리 (Users)

### 3. 내 정보 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/me` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"name": "홍길동", "email": "hong@example.com"}` |
| `401` | 인증 실패 | 토큰 없음 또는 유효하지 않음 |

### 4. 내 정보 수정
| 항목 | 내용 |
|------|------|
| **Method** | `PUT` |
| **URL** | `/users/me` |
| **Headers** | `Authorization: Bearer {access_token}` |
| **Content-Type** | `application/json` |

**Request Body:**
| 필드 | 타입 | 필수 | 제약사항 |
|------|------|------|---------|
| `name` | string | ❌ | 2-32자, 한글/영문/숫자만 허용, 중복 불가 |
| `password` | string | ❌ | 8-64자, 대소문자+숫자+특수문자 포함 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"name": "홍길동", "email": "hong@example.com", "updated_at": "2025-01-15T10:30:00Z"}` |
| `400` | 유효성 검증 실패 | 이름 중복, 비밀번호 규칙 위반 |
| `404` | 사용자 없음 | - |

### 5. 계정 삭제
| 항목 | 내용 |
|------|------|
| **Method** | `DELETE` |
| **URL** | `/users/me` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Response:**
| 상태코드 | 설명 |
|----------|------|
| `204` | 성공 (응답 본문 없음) |
| `404` | 사용자 없음 |

### 6. 사용자 목록 조회 (소셜 기능용)
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Query Parameters:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|-------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 |
| `items_per_page` | integer | ❌ | 18 | 페이지당 항목 수 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"total_count": 100, "page": 1, "items_per_page": 18, "users": [...]}` |

### 7. 사용자명으로 조회
| 항목 | 내용 |
|------|------|
| **Method** | `GET` |
| **URL** | `/users/{user_name}` |
| **Headers** | `Authorization: Bearer {access_token}` |

**Path Parameters:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `user_name` | string | ✅ | 조회할 사용자명 |

**Response:**
| 상태코드 | 설명 | Response Body |
|----------|------|---------------|
| `200` | 성공 | `{"name": "홍길동", "email": "hong@example.com"}` |
| `404` | 사용자 없음 | - |

## 데이터 모델

### User DTO
| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | ULID 형식의 사용자 ID |
| `email` | string | 이메일 주소 |
| `name` | string | 사용자명 |
| `role` | string | 역할 (USER, ADMIN) |
| `created_at` | datetime | 생성일시 |
| `updated_at` | datetime | 수정일시 |

## 비즈니스 규칙

### 이메일 검증
| 규칙 | 설명 |
|------|------|
| **형식** | 유효한 이메일 형식 |
| **길이** | 최대 64자 |
| **유일성** | 중복 불가 |
| **정규화** | 소문자 변환, 공백 제거 |

### 이름 검증
| 규칙 | 설명 |
|------|------|
| **길이** | 2-32자 |
| **문자** | 한글, 영문, 숫자, 공백만 허용 |
| **유일성** | 중복 불가 |
| **정규화** | 앞뒤 공백 제거 |

### 비밀번호 검증
| 규칙 | 설명 |
|------|------|
| **길이** | 8-64자 |
| **구성** | 대문자, 소문자, 숫자, 특수문자 각 1개 이상 |
| **제한** | 공백 포함 불가 |
| **저장** | 해시화하여 저장 |

### 역할 (Role)
| 역할 | 설명 |
|------|------|
| `USER` | 일반 사용자 |
| `ADMIN` | 관리자 |

## HTTP 상태 코드

| 코드 | 설명 | 발생 시점 |
|------|------|-----------|
| `200` | OK | 조회/수정 성공 |
| `201` | Created | 생성 성공 |
| `204` | No Content | 삭제 성공 |
| `400` | Bad Request | 유효성 검증 실패 |
| `401` | Unauthorized | 인증 실패 |
| `404` | Not Found | 리소스 없음 |
| `422` | Unprocessable Entity | 처리할 수 없는 엔티티 |
