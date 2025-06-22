class RepositoryError(Exception):
    """Repository 기본 예외"""
    pass

class EntityNotFoundError(RepositoryError):
    """엔티티를 찾을 수 없음 (모든 엔티티 공통)"""
    def __init__(self, entity_type: str, identifier: str):
        self.entity_type = entity_type
        self.identifier = identifier
        super().__init__(f"{entity_type} not found: {identifier}")

class DuplicateEntityError(RepositoryError):
    """중복된 엔티티 (모든 엔티티 공통)"""
    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"Duplicate {entity_type}: {field}={value}")

class DatabaseError(RepositoryError):
    """데이터베이스 관련 오류 (연결, 트랜잭션 등)"""
    pass