set -e

until mysqladmin ping -h"$DB_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  echo "waiting for db..."
  sleep 2
done

alembic upgrade head

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
