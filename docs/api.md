# Curriculum Learning Platform API Documentation

## Overview

커리큘럼 학습 플랫폼의 REST API 문서입니다.

- **Base URL**: `http://localhost:8000/api/v1`
- **Authentication**: Bearer Token
- **Content Type**: `application/json`

## Authentication

모든 보호된 엔드포인트는 Authorization 헤더에 Bearer Token을 포함해야 합니다.

```http
Authorization: Bearer {access_token}
```

---

## 🔐 Authentication

### Sign Up
회원가입을 진행합니다.

```http
POST /auth/signup
```

**Request Body:**
```json
{
  "name": "홍길동",
  "email": "user@example.com", 
  "password": "Password123!"
}
```

**Response:**
```json
{
  "name": "홍길동",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Login
로그인 후 액세스 토큰을 발급받습니다.

```http
POST /auth/login
```

**Request Body (Form Data):**
```
username=user@example.com
password=Password123!
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "USER"
}
```

---

## 👤 Users

### Get My Profile
현재 로그인한 사용자의 프로필을 조회합니다.

```http
GET /users/me
```

**Response:**
```json
{
  "name": "홍길동",
  "email": "user@example.com"
}
```

### Update My Profile
프로필 정보를 수정합니다.

```http
PUT /users/me
```

**Request Body:**
```json
{
  "name": "새이름",
  "password": "NewPassword123!"
}
```

**Response:**
```json
{
  "name": "새이름",
  "email": "user@example.com",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Delete My Account
계정을 삭제합니다.

```http
DELETE /users/me
```

### Get Users List
사용자 목록을 조회합니다.

```http
GET /users?page=1&items_per_page=10
```

**Response:**
```json
{
  "total_count": 50,
  "page": 1,
  "items_per_page": 10,
  "users": [
    {
      "name": "홍길동",
      "email": "user@example.com"
    }
  ]
}
```

### Get User by Name
특정 사용자를 이름으로 조회합니다.

```http
GET /users/{username}
```

---

## 📚 Curriculums

### Generate AI Curriculum
AI를 사용하여 커리큘럼을 자동 생성합니다.

```http
POST /curriculums/generate
```

**Request Body:**
```json
{
  "goal": "React 웹 개발 마스터하기",
  "period": 12,
  "difficulty": "intermediate",
  "details": "실무에 바로 적용할 수 있는 React 프로젝트 위주로 학습하고 싶습니다."
}
```

**Response:**
```json
{
  "id": "01H8...",
  "title": "240802 React 웹 개발 마스터하기",
  "visibility": "PRIVATE",
  "week_schedules": [
    {
      "week_number": 1,
      "lessons": ["React 기초 개념", "JSX 문법", "컴포넌트 생성"]
    }
  ]
}
```

### Create Manual Curriculum
수동으로 커리큘럼을 생성합니다.

```http
POST /curriculums
```

**Request Body:**
```json
{
  "title": "나만의 Python 커리큘럼",
  "visibility": "PUBLIC",
  "week_schedules": [
    {
      "week_number": 1,
      "lessons": ["Python 설치", "기본 문법", "변수와 데이터 타입"]
    },
    {
      "week_number": 2,
      "lessons": ["조건문", "반복문", "함수"]
    }
  ]
}
```

### Get My Curriculums
내가 생성한 커리큘럼 목록을 조회합니다.

```http
GET /curriculums?page=1&items_per_page=10
```

**Response:**
```json
{
  "total_count": 5,
  "curriculums": [
    {
      "id": "01H8...",
      "title": "React 웹 개발",
      "owner_name": "홍길동",
      "visibility": "PUBLIC"
    }
  ]
}
```

### Get Curriculum Details
커리큘럼 상세 정보를 조회합니다.

```http
GET /curriculums/{curriculum_id}
```

**Response:**
```json
{
  "id": "01H8...",
  "owner_name": "홍길동",
  "title": "React 웹 개발",
  "visibility": "PUBLIC",
  "week_schedules": [
    {
      "week_number": 1,
      "lessons": ["React 기초", "JSX", "컴포넌트"]
    }
  ]
}
```

### Update Curriculum
커리큘럼 정보를 수정합니다.

```http
PATCH /curriculums/{curriculum_id}
```

**Request Body:**
```json
{
  "title": "수정된 제목",
  "visibility": "PUBLIC"
}
```

### Delete Curriculum
커리큘럼을 삭제합니다.

```http
DELETE /curriculums/{curriculum_id}
```

---

## 📅 Week Schedules

### Add Week
새로운 주차를 추가합니다.

```http
POST /curriculums/{curriculum_id}/weeks
```

**Request Body:**
```json
{
  "week_number": 3,
  "lessons": ["새로운 주제1", "새로운 주제2"]
}
```

### Delete Week
주차를 삭제합니다.

```http
DELETE /curriculums/{curriculum_id}/weeks/{week_number}
```

### Add Lesson
주차에 새로운 레슨을 추가합니다.

```http
POST /curriculums/{curriculum_id}/weeks/{week_number}/lessons
```

**Request Body:**
```json
{
  "lesson": "새로운 레슨",
  "index": 1
}
```

### Update Lesson
레슨 내용을 수정합니다.

```http
PATCH /curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}
```

**Request Body:**
```json
{
  "lesson": "수정된 레슨"
}
```

### Delete Lesson
레슨을 삭제합니다.

```http
DELETE /curriculums/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}
```

---

## 📝 Summaries

### Create Summary
주차별 학습 요약을 작성합니다.

```http
POST /curriculums/{curriculum_id}/weeks/{week_number}/summaries
```

**Request Body:**
```json
{
  "content": "이번 주에 React의 기본 개념을 학습했습니다. JSX 문법을 익히고 간단한 컴포넌트를 만들어보았습니다. 컴포넌트의 props와 state 개념을 이해했고, 이벤트 핸들링 방법도 배웠습니다. 실습을 통해 todo 리스트 앱을 만들어보며 실제 개발 경험을 쌓았습니다."
}
```

**Response:**
```json
{
  "id": "01H8...",
  "content": "이번 주에 React의 기본 개념을...",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "feedback": null
}
```

### Get Week Summaries
특정 주차의 요약 목록을 조회합니다.

```http
GET /curriculums/{curriculum_id}/weeks/{week_number}/summaries?page=1&items_per_page=10
```

### Get Summary Details
요약 상세 정보를 조회합니다.

```http
GET /curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}
```

### Get My Summaries
내가 작성한 모든 요약을 조회합니다.

```http
GET /summaries/me?page=1&items_per_page=10
```

**Response:**
```json
{
  "total_count": 15,
  "summaries": [
    {
      "id": "01H8...",
      "curriculum_id": "01H7...",
      "snippet": "이번 주에 React의 기본 개념을...",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Delete Summary
요약을 삭제합니다.

```http
DELETE /curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}
```

---

## 🤖 Feedback

### Generate AI Feedback
AI를 사용하여 요약에 대한 피드백을 생성합니다.

```http
POST /curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}/feedback
```

**Response:**
```json
{
  "id": "01H8...",
  "comment": "React 기본 개념을 잘 이해하신 것 같습니다. 특히 컴포넌트와 JSX에 대한 이해가 돋보입니다. 다음 주에는 Hook 개념을 추가로 학습하시면 더 깊이 있는 이해가 가능할 것입니다.",
  "score": 8.5,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Get Feedback
피드백을 조회합니다.

```http
GET /curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}/feedback
```

### Delete Feedback
피드백을 삭제합니다.

```http
DELETE /curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}/feedback/{feedback_id}
```

---

## 💝 Social Features

### Toggle Like
커리큘럼 좋아요를 토글합니다.

```http
POST /curriculums/{curriculum_id}/like
```

**Response:**
```json
{
  "is_liked": true,
  "like_count": 15
}
```

### Toggle Bookmark
커리큘럼 북마크를 토글합니다.

```http
POST /curriculums/{curriculum_id}/bookmark
```

**Response:**
```json
{
  "is_bookmarked": true
}
```

### Get Curriculum Likes
커리큘럼의 좋아요 목록을 조회합니다.

```http
GET /curriculums/{curriculum_id}/likes?page=1&items_per_page=10
```

### Get Social Info
커리큘럼의 소셜 정보를 조회합니다.

```http
GET /curriculums/{curriculum_id}/social-info
```

**Response:**
```json
{
  "curriculum_id": "01H8...",
  "like_count": 15,
  "is_liked": true,
  "is_bookmarked": false
}
```

### Get My Likes
내가 좋아요한 커리큘럼 목록을 조회합니다.

```http
GET /users/me/likes?page=1&items_per_page=10
```

### Get My Bookmarks
내가 북마크한 커리큘럼 목록을 조회합니다.

```http
GET /users/me/bookmarks?page=1&items_per_page=10
```

---

## 💬 Comments

### Create Comment
커리큘럼에 댓글을 작성합니다.

```http
POST /curriculums/{curriculum_id}/comments
```

**Request Body:**
```json
{
  "content": "정말 유익한 커리큘럼이네요! 감사합니다.",
  "parent_comment_id": null
}
```

**Response:**
```json
{
  "id": "01H8...",
  "user_id": "01H7...",
  "curriculum_id": "01H6...",
  "content": "정말 유익한 커리큘럼이네요! 감사합니다.",
  "parent_comment_id": null,
  "is_deleted": false,
  "reply_count": 0,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Get Curriculum Comments
커리큘럼의 댓글 목록을 조회합니다.

```http
GET /curriculums/{curriculum_id}/comments?page=1&items_per_page=10
```

### Get Comment Replies
댓글의 대댓글 목록을 조회합니다.

```http
GET /curriculums/comments/{parent_comment_id}/replies?page=1&items_per_page=10
```

### Update Comment
댓글을 수정합니다.

```http
PUT /curriculums/comments/{comment_id}
```

**Request Body:**
```json
{
  "content": "수정된 댓글 내용입니다."
}
```

### Delete Comment
댓글을 삭제합니다 (소프트 삭제).

```http
DELETE /curriculums/comments/{comment_id}
```

### Get My Comments
내가 작성한 댓글 목록을 조회합니다.

```http
GET /users/me/comments?page=1&items_per_page=10
```

### Get Comment Stats
커리큘럼의 댓글 통계를 조회합니다.

```http
GET /curriculums/{curriculum_id}/comments/stats
```

**Response:**
```json
{
  "curriculum_id": "01H8...",
  "total_comment_count": 25
}
```

---

## 🏷️ Tags

### Create Tag
새로운 태그를 생성합니다.

```http
POST /tags
```

**Request Body:**
```json
{
  "name": "javascript"
}
```

### Get Popular Tags
인기 태그 목록을 조회합니다.

```http
GET /tags/popular?limit=20&min_usage=1
```

**Response:**
```json
[
  {
    "id": "01H8...",
    "name": "javascript",
    "usage_count": 45,
    "is_popular": true,
    "created_by": "01H7...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Search Tags
태그를 검색합니다 (자동완성용).

```http
GET /tags/search?q=java&limit=10
```

### Get All Tags
모든 태그 목록을 조회합니다.

```http
GET /tags?page=1&items_per_page=20
```

### Add Tags to Curriculum
커리큘럼에 태그를 추가합니다.

```http
POST /curriculums/{curriculum_id}/tags
```

**Request Body:**
```json
{
  "tag_names": ["javascript", "react", "frontend"]
}
```

### Get Curriculum Tags
커리큘럼의 태그와 카테고리를 조회합니다.

```http
GET /curriculums/{curriculum_id}/tags
```

**Response:**
```json
{
  "curriculum_id": "01H8...",
  "tags": [
    {
      "id": "01H7...",
      "name": "javascript",
      "usage_count": 45,
      "is_popular": true,
      "created_by": "01H6...",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "category": {
    "id": "01H5...",
    "name": "프로그래밍",
    "description": "프로그래밍 관련 커리큘럼",
    "color": "#007bff",
    "icon": "code",
    "sort_order": 1,
    "is_active": true,
    "curriculum_count": 0,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### Remove Tag from Curriculum
커리큘럼에서 태그를 제거합니다.

```http
DELETE /curriculums/{curriculum_id}/tags
```

**Request Body:**
```json
{
  "tag_name": "javascript"
}
```

---

## 📂 Categories

### Create Category (Admin Only)
새로운 카테고리를 생성합니다.

```http
POST /categories
```

**Request Body:**
```json
{
  "name": "프로그래밍",
  "description": "프로그래밍 관련 커리큘럼",
  "color": "#007bff",
  "icon": "code",
  "sort_order": 1
}
```

### Get Categories
카테고리 목록을 조회합니다.

```http
GET /categories?page=1&items_per_page=20&include_inactive=false
```

### Get Active Categories
활성화된 카테고리 목록을 조회합니다.

```http
GET /categories/active
```

### Update Category (Admin Only)
카테고리를 수정합니다.

```http
PATCH /categories/{category_id}
```

### Assign Category to Curriculum
커리큘럼에 카테고리를 할당합니다.

```http
POST /curriculums/{curriculum_id}/category
```

**Request Body:**
```json
{
  "category_id": "01H8..."
}
```

### Remove Category from Curriculum
커리큘럼에서 카테고리를 제거합니다.

```http
DELETE /curriculums/{curriculum_id}/category
```

---

## 👮 Admin APIs

### Get Admin Stats
관리자 통계를 조회합니다.

```http
GET /admins/stats
```

**Response:**
```json
{
  "total_users": 150,
  "total_curriculums": 75,
  "total_summaries": 300,
  "total_feedbacks": 250
}
```

### Get Admin Dashboard
관리자 대시보드 데이터를 조회합니다.

```http
GET /admins/dashboard
```

### Admin User Management
```http
GET /admins/users                    # 사용자 목록
GET /admins/users/{user_id}          # 사용자 상세
PATCH /admins/users/{user_id}        # 사용자 수정
DELETE /admins/users/{user_id}       # 사용자 삭제
```

### Admin Curriculum Management
```http
GET /admins/curriculums              # 모든 커리큘럼 조회
GET /admins/curriculums/{id}         # 커리큘럼 상세
PATCH /admins/curriculums/{id}       # 커리큘럼 수정
DELETE /admins/curriculums/{id}      # 커리큘럼 삭제
```

### Bulk Operations
```http
DELETE /admins/bulk/curriculums      # 커리큘럼 일괄 삭제
PATCH /admins/bulk/curriculums       # 커리큘럼 일괄 수정
DELETE /admins/bulk/users            # 사용자 일괄 삭제
```

---

## 📊 Monitoring

### Health Check
애플리케이션 상태를 확인합니다.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "curriculum-api",
  "version": "1.0.0"
}
```

### Metrics
Prometheus 메트릭을 조회합니다.

```http
GET /metrics
```

---

## Error Responses

API에서 발생할 수 있는 공통 에러 응답입니다.

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "관리자만 접근이 가능합니다."
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "이미 사용 중인 이메일입니다."
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

API는 사용자당 다음과 같은 속도 제한이 적용됩니다:

- **일반 API**: 분당 100회 요청
- **LLM API** (커리큘럼 생성, 피드백): 분당 10회 요청
- **업로드**: 분당 20회 요청

제한을 초과하면 `429 Too Many Requests` 응답을 받게 됩니다.

---

## Pagination

목록 조회 API는 다음과 같은 페이지네이션 파라미터를 지원합니다:

- `page`: 페이지 번호 (기본값: 1)
- `items_per_page`: 페이지당 항목 수 (기본값: 10, 최대: 100)

응답에는 다음 정보가 포함됩니다:

```json
{
  "total_count": 100,
  "page": 1,
  "items_per_page": 10,
  "data": [...]
}
```
