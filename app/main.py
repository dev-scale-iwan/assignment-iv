from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


from app.modules.research.schema import ResearchInput
from app.modules.research.tasks import setorsampah_task
from app.core.setting import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/setorsampah", openapi_extra={
    "requestBody": {
        "content": {
            "application/json": {
                "examples": {
                    "Selvi": {
                        "summary": "Sample Input",
                        "value": {"input": "Selvi setor sampah plastik 2 kg"}
                    }
                }
            }
        }
    }
})
def do_setorsampah(body: ResearchInput):
    print(f"Hi")
    setorsampah_task.delay(body.input)

    return {"message": "Processing ....!"}

@app.get("/scalar")
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)