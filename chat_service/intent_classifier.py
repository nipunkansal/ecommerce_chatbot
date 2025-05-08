def classify_intent(query: str) -> str:
    product_keywords = ["buy", "price", "feature", "details", "specs", "recommend"]
    order_keywords = ["order", "status", "shipping", "delivered", "customer id"]

    if any(word in query.lower() for word in product_keywords):
        return "product"
    elif any(word in query.lower() for word in order_keywords):
        return "order"
    else:
        return "unknown"