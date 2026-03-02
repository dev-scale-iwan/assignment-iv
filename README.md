## Assignment IV

https://github.com/Devscale-Indonesia/agentic-workflow-batch3

### Setup

```bash
make dev
# Open a new terminal and run
make celery
```

### Usage

```bash
curl -X POST http://localhost:8000/setorsampah \
  -H "Content-Type: application/json" \
  -d '{"input": "Selvi setor sampah tembaga 3 kg"}'
```