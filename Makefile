dev:
	uv run uvicorn app.main:app --reload

celery:
	uv run celery -A app.celery worker --loglevel=info