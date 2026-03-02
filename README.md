## Assignment IV

https://github.com/Devscale-Indonesia/agentic-workflow-batch3

### Setup

```bash
make dev
```

### Usage

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence"}'
```