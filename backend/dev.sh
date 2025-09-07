PORT="${PORT:-8080}"

set -a && source ../.env.run && set +a

uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload