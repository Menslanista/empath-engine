from fastapi import FastAPI
from pydantic import BaseModel

class MemoryQuery(BaseModel):
    session_id: str
    key: str | None = None

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/memory/get")
async def memory_get(q: MemoryQuery):
    return {"session_id": q.session_id, "key": q.key, "value": "stub"}