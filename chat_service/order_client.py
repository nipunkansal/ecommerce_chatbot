import httpx

ORDER_SERVICE_URL = "http://localhost:8002"

async def fetch_orders(customer_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/data/customer/{customer_id}")
        return response.json()