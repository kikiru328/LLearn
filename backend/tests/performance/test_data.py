#!/usr/bin/env python3
"""
LLearn 프로젝트 LLM 성능 측정 스크립트
커리큘럼 생성 API의 성능을 측정합니다.
"""

import requests
import time
import json
import statistics
from datetime import datetime
from typing import List, Dict, Any


class LLMPerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.user_tokens = {}  # 사용자별 토큰 저장
        self.results = []
        self.users = [
            ("testtestuser@test.com", "!!Test123"),
            ("testtestuser02@test.com", "!!Test123"),
            ("testtestuser03@test.com", "!!Test123"),
            ("testtestuser04@test.com", "!!Test123"),
            ("testtestuser05@test.com", "!!Test123"),
            ("testtestuser06@test.com", "!!Test123"),
            ("testtestuser07@test.com", "!!Test123"),
            ("testtestuser08@test.com", "!!Test123"),
            ("testtestuser09@test.com", "!!Test123"),
            ("testtestuser10@test.com", "!!Test123"),
        ]

    def create_test_users(self) -> bool:
        """새로운 테스트 사용자들을 자동 생성"""
        print("👤 새로운 테스트 사용자 생성 중...")

        signup_url = f"{self.base_url}/api/v1/auth/signup"
        created_count = 0

        for i, (email, password) in enumerate(self.users, 1):
            signup_data = {
                "name": f"testtestuser{i:02d}",
                "email": email,
                "password": password,
            }

            try:
                response = requests.post(signup_url, json=signup_data)
                if response.status_code == 200 or response.status_code == 201:
                    # 200 또는 201 = 회원가입 성공
                    print(f"✅ 사용자 생성 성공: {email}")
                    created_count += 1
                elif response.status_code == 409:
                    # 409 = 이미 존재하는 사용자 (사용 가능)
                    print(f"ℹ️  사용자 이미 존재: {email}")
                    created_count += 1
                elif response.status_code == 400:
                    # 400 에러도 이메일 중복일 가능성
                    error_text = response.text.lower()
                    if "email" in error_text:
                        print(f"ℹ️  사용자 이미 존재: {email}")
                        created_count += 1
                    else:
                        print(
                            f"❌ 사용자 생성 실패: {email} - {response.status_code} - {response.text}"
                        )
                else:
                    print(
                        f"❌ 사용자 생성 실패: {email} - {response.status_code} - {response.text}"
                    )
            except Exception as e:
                print(f"❌ 사용자 생성 중 오류: {email} - {e}")

            time.sleep(0.2)  # API 부하 방지

        print(f"✅ {created_count}/{len(self.users)}명 사용자 준비 완료")
        return created_count > 0

    def login_user(self, email: str, password: str) -> bool:
        """개별 사용자 로그인 및 토큰 획득"""
        login_url = f"{self.base_url}/api/v1/auth/login"

        data = {"username": email, "password": password}

        try:
            response = requests.post(login_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.user_tokens[email] = token_data["access_token"]
                print(f"✅ 로그인 성공: {email}")
                return True
            else:
                print(f"❌ 로그인 실패: {email} - {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 로그인 중 오류: {email} - {e}")
            return False

    def login_all_users(self) -> bool:
        """모든 사용자 로그인"""
        print(f"🔐 {len(self.users)}명 사용자 로그인 중...")

        success_count = 0
        for email, password in self.users:
            if self.login_user(email, password):
                success_count += 1
            time.sleep(0.5)  # 로그인 간격

        print(f"✅ {success_count}/{len(self.users)}명 로그인 성공")
        return success_count > 0

    def generate_test_cases(self, count: int = 100) -> List[Dict[str, Any]]:
        """테스트용 커리큘럼 생성 케이스들을 준비"""
        test_cases = []

        # 다양한 주제들
        topics = [
            "Python 기초",
            "JavaScript 심화",
            "React 개발",
            "Vue.js 기본",
            "Node.js 백엔드",
            "Django 웹개발",
            "FastAPI 구축",
            "Flask 미니앱",
            "데이터베이스 설계",
            "SQL 마스터",
            "MongoDB 활용",
            "Redis 캐싱",
            "머신러닝 입문",
            "딥러닝 기초",
            "데이터 분석",
            "AI 모델링",
            "Docker 컨테이너",
            "Kubernetes 오케스트레이션",
            "AWS 클라우드",
            "GCP 서비스",
            "Git 버전관리",
            "CI/CD 파이프라인",
            "테스트 자동화",
            "성능 최적화",
            "네트워크 보안",
            "웹 보안",
            "API 설계",
            "마이크로서비스",
            "함수형 프로그래밍",
            "객체지향 설계",
            "디자인 패턴",
            "클린 코드",
            "알고리즘 분석",
            "자료구조",
            "시스템 설계",
            "분산 시스템",
            "블록체인 개발",
            "게임 개발",
            "모바일 앱",
            "크로스플랫폼",
            "UI/UX 디자인",
            "프론트엔드 최적화",
            "백엔드 아키텍처",
            "데브옵스",
            "TDD 개발",
            "BDD 테스팅",
            "리팩토링",
            "코드 리뷰",
        ]

        difficulties = ["beginner", "intermediate", "expert"]
        periods = [2, 4, 6, 8, 12, 16]

        for i in range(count):
            topic = topics[i % len(topics)]
            difficulty = difficulties[i % len(difficulties)]
            period = periods[i % len(periods)]

            test_case = {
                "goal": f"{topic} 학습",
                "period": period,
                "difficulty": difficulty,
                "details": f"{topic}에 대한 체계적 학습 과정",
            }
            test_cases.append(test_case)

        return test_cases

    def test_single_curriculum_generation(
        self, test_case: Dict[str, Any], test_num: int, user_email: str
    ) -> Dict[str, Any]:
        """단일 커리큘럼 생성 테스트 (특정 사용자로)"""
        if user_email not in self.user_tokens:
            return {"success": False, "error": f"No token for user {user_email}"}

        headers = {
            "Authorization": f"Bearer {self.user_tokens[user_email]}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/api/v1/curriculums/generate"

        start_time = time.time()

        try:
            response = requests.post(url, headers=headers, json=test_case, timeout=120)
            end_time = time.time()

            response_time = end_time - start_time

            result = {
                "test_number": test_num,
                "user_email": user_email,
                "success": response.status_code == 201,
                "status_code": response.status_code,
                "response_time": response_time,
                "goal": test_case["goal"],
                "period": test_case["period"],
                "difficulty": test_case["difficulty"],
                "timestamp": datetime.now().isoformat(),
            }

            if response.status_code == 201:
                curriculum_data = response.json()
                result.update(
                    {
                        "curriculum_id": curriculum_data.get("id"),
                        "weeks_count": len(curriculum_data.get("week_schedules", [])),
                        "total_lessons": sum(
                            len(week.get("lessons", []))
                            for week in curriculum_data.get("week_schedules", [])
                        ),
                    }
                )
                print(
                    f"✅ 테스트 {test_num:3d} ({user_email[:10]}): {test_case['goal']:20s} | {response_time:6.2f}초 | {result['weeks_count']}주차"
                )
            else:
                result["error"] = response.text
                print(
                    f"❌ 테스트 {test_num:3d} ({user_email[:10]}): {test_case['goal']:20s} | 실패 ({response.status_code})"
                )

        except requests.exceptions.Timeout:
            result = {
                "test_number": test_num,
                "user_email": user_email,
                "success": False,
                "error": "Timeout (120s)",
                "response_time": 120.0,
                "goal": test_case["goal"],
                "timestamp": datetime.now().isoformat(),
            }
            print(
                f"⏰ 테스트 {test_num:3d} ({user_email[:10]}): {test_case['goal']:20s} | 타임아웃"
            )

        except Exception as e:
            result = {
                "test_number": test_num,
                "user_email": user_email,
                "success": False,
                "error": str(e),
                "response_time": None,
                "goal": test_case["goal"],
                "timestamp": datetime.now().isoformat(),
            }
            print(
                f"💥 테스트 {test_num:3d} ({user_email[:10]}): {test_case['goal']:20s} | 오류: {e}"
            )

        return result

    def run_performance_test(self, test_count: int = 100, delay: float = 1.0):
        """전체 성능 테스트 실행 (멀티 사용자)"""
        print(f"🚀 LLearn 멀티 사용자 LLM 성능 테스트 시작")
        print(f"👥 사용자: {len(self.users)}명")
        print(f"📊 테스트 설정: {test_count}개 커리큘럼, {delay}초 간격")
        print("=" * 80)

        # 0. 새로운 테스트 사용자 생성
        if not self.create_test_users():
            print("❌ 사용자 생성 실패로 테스트를 중단합니다.")
            return

        # 1. 모든 사용자 로그인
        if not self.login_all_users():
            print("❌ 로그인 실패로 테스트를 중단합니다.")
            return

        # 2. 테스트 케이스 생성
        test_cases = self.generate_test_cases(test_count)
        print(f"📝 {len(test_cases)}개 테스트 케이스 준비 완료")
        print()

        # 3. 성능 테스트 실행 (사용자 라운드로빈)
        start_total = time.time()
        logged_in_users = [
            email for email, _ in self.users if email in self.user_tokens
        ]

        if not logged_in_users:
            print("❌ 로그인된 사용자가 없습니다.")
            return

        print(f"🔄 {len(logged_in_users)}명 사용자 라운드로빈으로 테스트 진행")
        print()

        for i, test_case in enumerate(test_cases, 1):
            # 라운드로빈으로 사용자 선택
            user_email = logged_in_users[(i - 1) % len(logged_in_users)]

            result = self.test_single_curriculum_generation(test_case, i, user_email)
            self.results.append(result)

            # 중간 대기 (마지막 테스트가 아닐 때만)
            if i < len(test_cases):
                time.sleep(delay)

        end_total = time.time()
        total_time = end_total - start_total

        print()
        print("=" * 80)
        print(f"🏁 테스트 완료! 총 소요시간: {total_time:.2f}초")

        # 4. 결과 분석
        self.analyze_results()

        # 5. 결과 저장
        self.save_results()

    def analyze_results(self):
        """테스트 결과 분석 및 출력"""
        if not self.results:
            print("❌ 분석할 결과가 없습니다.")
            return

        successful_results = [r for r in self.results if r["success"]]
        failed_results = [r for r in self.results if not r["success"]]

        print(f"\n📊 **멀티 사용자 LLM 성능 측정 결과**")
        print("=" * 60)

        # 기본 통계
        total_tests = len(self.results)
        success_count = len(successful_results)
        success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0

        print(f"🎯 **전체 통계**")
        print(f"├── 총 테스트: {total_tests}개")
        print(f"├── 성공: {success_count}개")
        print(f"├── 실패: {len(failed_results)}개")
        print(f"└── 성공률: {success_rate:.1f}%")
        print()

        # 응답 시간 분석 (성공한 경우만)
        if successful_results:
            response_times = [r["response_time"] for r in successful_results]

            print(f"⏱️ **응답 시간 분석**")
            print(f"├── 평균: {statistics.mean(response_times):.2f}초")
            print(f"├── 중간값: {statistics.median(response_times):.2f}초")
            print(f"├── 최소: {min(response_times):.2f}초")
            print(f"├── 최대: {max(response_times):.2f}초")

            # 표준편차는 데이터가 2개 이상일 때만 계산
            if len(response_times) >= 2:
                print(f"├── 표준편차: {statistics.stdev(response_times):.2f}초")
            else:
                print(f"├── 표준편차: N/A (데이터 부족)")

            # P95, P99 계산 (데이터가 충분할 때만)
            if len(response_times) >= 5:
                sorted_times = sorted(response_times)
                p95_index = max(0, int(len(sorted_times) * 0.95))
                p99_index = max(0, int(len(sorted_times) * 0.99))
                print(f"├── P95: {sorted_times[p95_index]:.2f}초")
                print(f"└── P99: {sorted_times[p99_index]:.2f}초")
            else:
                print(f"├── P95: N/A (데이터 부족)")
                print(f"└── P99: N/A (데이터 부족)")
            print()

        # 커리큘럼 생성 품질 분석
        if successful_results:
            weeks_counts = [
                r.get("weeks_count", 0)
                for r in successful_results
                if "weeks_count" in r
            ]
            lessons_counts = [
                r.get("total_lessons", 0)
                for r in successful_results
                if "total_lessons" in r
            ]

            if weeks_counts:
                print(f"📚 **생성 품질 분석**")
                print(f"├── 평균 주차 수: {statistics.mean(weeks_counts):.1f}주")
                print(f"├── 평균 레슨 수: {statistics.mean(lessons_counts):.1f}개")
                print(
                    f"├── 주차별 평균 레슨: {statistics.mean(lessons_counts) / statistics.mean(weeks_counts):.1f}개"
                )

                # 표준편차는 데이터가 2개 이상일 때만 계산
                if len(weeks_counts) >= 2:
                    consistency = (
                        "높음" if statistics.stdev(weeks_counts) < 2 else "보통"
                    )
                else:
                    consistency = "데이터 부족"
                print(f"└── 생성 일관성: {consistency}")
                print()

        # 난이도별 성능 분석
        difficulty_stats = {}
        for result in successful_results:
            diff = result.get("difficulty", "unknown")
            if diff not in difficulty_stats:
                difficulty_stats[diff] = []
            difficulty_stats[diff].append(result["response_time"])

        if difficulty_stats:
            print(f"🎚️ **난이도별 성능**")
            for diff, times in difficulty_stats.items():
                avg_time = statistics.mean(times)
                print(f"├── {diff}: {avg_time:.2f}초 평균 ({len(times)}개)")
            print()

        # 사용자별 성능 분석
        user_stats = {}
        for result in successful_results:
            user = result.get("user_email", "unknown")
            if user not in user_stats:
                user_stats[user] = []
            user_stats[user].append(result["response_time"])

        if user_stats:
            print(f"👥 **사용자별 성능**")
            for user_email, times in user_stats.items():
                avg_time = statistics.mean(times)
                test_count = len(times)
                user_short = user_email.split("@")[0]
                print(
                    f"├── {user_short:8s}: {avg_time:6.2f}초 평균 ({test_count:2d}개)"
                )
            print()

        # 동시성 분석
        print(f"🔄 **동시성 테스트 결과**")
        print(f"├── 참여 사용자: {len(user_stats)}명")
        print(
            f"├── 사용자당 평균: {len(successful_results) / len(user_stats):.1f}개 커리큘럼"
        )
        print(
            f"├── 부하 분산: {'균등' if max(len(times) for times in user_stats.values()) - min(len(times) for times in user_stats.values()) <= 2 else '불균등'}"
        )
        print(f"└── 동시성 효과: {'확인됨' if len(user_stats) > 1 else '단일 사용자'}")
        print()

        # 실패 원인 분석
        if failed_results:
            error_types = {}
            for result in failed_results:
                error = result.get("error", "Unknown")
                error_type = error.split(":")[0] if ":" in error else error
                error_types[error_type] = error_types.get(error_type, 0) + 1

            print(f"❌ **실패 원인 분석**")
            for error_type, count in error_types.items():
                print(f"├── {error_type}: {count}회")
            print()

        # 성능 등급 평가
        if successful_results:
            avg_time = statistics.mean([r["response_time"] for r in successful_results])

            if avg_time < 10:
                grade = "A+ (매우 우수)"
            elif avg_time < 15:
                grade = "A (우수)"
            elif avg_time < 25:
                grade = "B (양호)"
            elif avg_time < 40:
                grade = "C (보통)"
            else:
                grade = "D (개선 필요)"

            print(f"🏆 **종합 성능 등급: {grade}**")
            print(f"📈 **권장사항**: ", end="")
            if avg_time < 15:
                print("현재 성능이 매우 우수합니다!")
            elif avg_time < 30:
                print("프로덕션 환경에 적합한 성능입니다.")
            else:
                print("캐싱이나 비동기 처리 도입을 검토해보세요.")

    def save_results(self):
        """결과를 JSON 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"multiuser_llm_test_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "test_info": {
                        "total_tests": len(self.results),
                        "total_users": len(self.users),
                        "successful_users": len(self.user_tokens),
                        "timestamp": datetime.now().isoformat(),
                        "success_rate": len([r for r in self.results if r["success"]])
                        / len(self.results)
                        * 100,
                        "user_distribution": {
                            email: len(
                                [
                                    r
                                    for r in self.results
                                    if r.get("user_email") == email
                                ]
                            )
                            for email in self.user_tokens.keys()
                        },
                    },
                    "results": self.results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"💾 결과가 {filename}에 저장되었습니다.")


def main():
    """메인 실행 함수"""
    tester = LLMPerformanceTester()

    # 멀티 사용자 테스트 실행
    tester.run_performance_test(
        test_count=100, delay=1.0  # 100개 커리큘럼 생성  # 1초 간격
    )


if __name__ == "__main__":
    main()
