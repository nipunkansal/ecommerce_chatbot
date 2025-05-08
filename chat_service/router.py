from intent_classifier import classify_intent
from llm_response import generate_response
from order_client import fetch_orders
import httpx

PRODUCT_SERVICE_URL = "http://localhost:8001"  # Assuming running locally

async def handle_query(user_query: str):
    intent = classify_intent(user_query)

    if intent == "product":
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{PRODUCT_SERVICE_URL}/search", params={"q": user_query})
            search_results = response.json().get("results", [])
        context = "\n".join([r["Product_Title"] + ": " + r["Description"] for r in search_results[:3]])
        return {"response": generate_response(context, user_query)}

    elif intent == "order":
        customer_id = extract_customer_id(user_query)
        orders = await fetch_orders(customer_id)
        context = str(orders)
        return {"response": generate_response(context, user_query)}

    else:
        return {"response": "I'm sorry, I couldn't determine your intent. Please ask about a product or order."}


def extract_customer_id(query: str) -> int:
    import re
    match = re.search(r"\d+", query)
    return int(match.group()) if match else -1
    
if __name__== "__main__":
    query = "What are the top 5 highly-rated guitar products?"
    handle_query(query)