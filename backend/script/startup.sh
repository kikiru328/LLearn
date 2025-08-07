#!/bin/bash
set -e

echo "🚀 Starting curriculum platform..."

# 현재 디렉토리와 파일 확인
echo "📁 Current directory: $(pwd)"

# 환경변수 확인 (비밀번호는 마스킹)
echo "📊 Configuration:"
echo "  - App: $APP_NAME"
echo "  - DB Host: $DB_HOST"
echo "  - DB User: $DATABASE_NAME"
echo "  - DB Database: $MYSQL_DATABASE"
echo "  - Redis Host: $REDIS_HOST:$REDIS_PORT"
echo "  - Environment: $ENVIRONMENT"

# 데이터베이스 연결 대기
echo "⏳ Waiting for database connection..."
until mysqladmin ping -h"$DB_HOST" -u"$DATABASE_NAME" -p"$DATABASE_PASSWORD" --silent; do
  echo "  ... still waiting for database..."
  sleep 3
done
echo "✅ Database is ready!"

# Redis 연결 대기
echo "🔴 Waiting for Redis..."
until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" ping > /dev/null 2>&1; do
  echo "  ... still waiting for Redis..."
  sleep 2
done
echo "✅ Redis is ready!"

# Alembic 마이그레이션 실행
echo "🔄 Running database migrations..."
if [ -f "alembic.ini" ]; then
    echo "📋 Alembic current revision:"
    alembic current || echo "No current revision"
    
    echo "🔄 Upgrading to head..."
    alembic upgrade head 2>&1 || {
        echo "❌ Migration failed!"
        echo "🔍 Alembic logs:"
        alembic current -v 2>&1 || echo "Failed to get current revision"
        exit 1
    }
    echo "✅ Migrations completed!"
else
    echo "⚠️ No alembic.ini found, skipping migrations"
fi

# Redis 연결 확인
echo "🔴 Verifying Redis connection..."
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" ping
echo "✅ Redis connection verified!"

echo "✅ All services are ready!"
echo ""
echo "📋 Service URLs:"
echo "   🌐 API Server: http://localhost:8000"
echo "   🗄️  Database: $DB_HOST:3306"
echo "   🔴 Redis: $REDIS_HOST:$REDIS_PORT"
echo "   👀 Redis Insight: http://localhost:8001"
echo ""

echo "🌟 Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
