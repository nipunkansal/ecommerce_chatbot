from fastapi import FastAPI, Query
from retriever import search_products

app = FastAPI(title="Product Search Service", description="Provides product search using RAG.")

@app.get("/search")
def search(q: str = Query(..., description="User product-related query")):
    try:
        answer = search_products(q)
        return {"response": answer}
    except Exception as e:
        return {"error": str(e)}
