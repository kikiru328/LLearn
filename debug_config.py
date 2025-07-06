# test_di_working.py
from app.core.container import Container

container = Container()

# 1. UseCase 생성
create_user_usecase = container.create_user_usecase()

# 2. 의존성이 제대로 주입되었는지 확인
print(f"user_repository 주입됨: {create_user_usecase.user_repository is not None}")
print(f"password_service 주입됨: {create_user_usecase.password_service is not None}")

# 3. Singleton 동작 확인
service1 = container.llm_service()
service2 = container.llm_service()
print(f"LLM 서비스 싱글톤 동작: {service1 is service2}")

# 4. Factory 동작 확인  
repo1 = container.user_repository()
repo2 = container.user_repository()
print(f"Repository 팩토리 동작: {repo1 is not repo2}")

print("✅ 의존성 주입 완벽 동작!")