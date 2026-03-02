from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


from app.modules.research.schema import ResearchInput
from app.modules.research.tasks import research_task

app = FastAPI(title="Research API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/research")
def do_research(body: ResearchInput):
    print(f"Hi")
    research_task.delay(body.topic)

    return {"message": "Processing ....!"}

@app.get("/scalar")
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)