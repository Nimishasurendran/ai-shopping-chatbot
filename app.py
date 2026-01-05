from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import google.generativeai as genai
import os

app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


genai.configure(api_key="AIzaSyDEHwokOlC0J1zdg_PmI7BG_bCKaNJfWAQ")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

with open(os.path.join(BASE_DIR, "products.json"), "r") as f:
    products = json.load(f)

cart = []
orders = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(user_message: dict):
    msg = user_message["message"].lower()

    if "show" in msg or "products" in msg:
        return {
            "reply": "\n".join(
                [f"{p['id']}. {p['name']} - ₹{p['price']} (Stock: {p['stock']})"
                 for p in products]
            )
        }

    if "add" in msg:
        for p in products:
            if p["name"].lower() in msg:
                if p["stock"] > 0:
                    cart.append({
                        "id": p["id"],
                        "name": p["name"],
                        "price": p["price"],
                        "quantity": 1
                    })
                    p["stock"] -= 1
                    return {"reply": f"{p['name']} added to cart . Anything else?"}
                else:
                    return {"reply": "Sorry, product out of stock"}

    if "checkout" in msg or "confirm" in msg:
        if not cart:
            return {"reply": "Your cart is empty"}

        total_price = sum(item["price"] * item["quantity"] for item in cart)

        order = {
            "products": cart,
            "total_price": total_price,
            "status": "confirmed"
        }

        orders.append(order)
        cart.clear()

        return {
            "reply": f"Order confirmed with Total price: ₹{total_price}"
        }
    response = model.generate_content(msg)
    return {"reply": response.text}