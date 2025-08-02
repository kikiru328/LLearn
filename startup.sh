#!/bin/bash
set -e

echo "🚀 Starting curriculum platform..."

# 현재 디렉토리와 파일 확인
echo "📁 Current directory: $(pwd)"

# Alembic 설정 확인
if [ -f "alembic.ini" ]; then
    echo "✅ alembic.ini found"
else
    echo "❌ alembic.ini not found"
fi

# 환경변수 확인
echo "📊 Database config:"
echo "  - Host: $DB_HOST"
echo "  - User: $MYSQL_USER"
echo "  - Database: $MYSQL_DATABASE"
echo "  - DATABASE_URL: $DATABASE_URL"

# 데이터베이스 연결 대기
echo "⏳ Waiting for database connection..."
until mysqladmin ping -h"$DB_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  echo "  ... still waiting for database..."
  sleep 3
done

echo "✅ Database is ready!"

# Alembic 마이그레이션 실행
echo "🔄 Running database migrations..."
if [ -f "alembic.ini" ]; then
    echo "📋 Alembic current revision:"
    alembic current || echo "No current revision"
    
    echo "📋 Available revisions:"
    alembic history || echo "No migration history"
    
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

echo "🌟 Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
