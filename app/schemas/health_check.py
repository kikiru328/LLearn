from datetime import datetime
from pydantic import BaseModel, Field


class ServiceInfo(BaseModel):
    name: str = Field(..., description="App Name")
    version: str = Field(..., description="App Version")
    environment: str = Field(
        ..., description="실행 환경 (development/production/staging)"
    )


class SystemInfo(BaseModel):
    platform: str = Field(..., description="OS 환경 (windows/iOS/Linux)")
    python_version: str = Field(..., description="Python Version")
    architecture: str = Field(..., description="시스템 아키텍처 (x86_64/arm64/etc)")


class DependencyStatus(BaseModel):
    database: str = Field(
        ..., description="database connection status (connected/disconnected)"
    )
    llm_service: str = Field(..., description="llm_service(openai) available")


class BasicHealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str


class DetailedHealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime
    service: ServiceInfo
    system: SystemInfo
    dependencies: DependencyStatus
