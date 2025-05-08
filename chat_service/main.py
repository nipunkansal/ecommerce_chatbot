from fastapi import FastAPI, Request
from router import handle_query

app = FastAPI(title="Chat Service")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query")
    return await handle_query(user_query)