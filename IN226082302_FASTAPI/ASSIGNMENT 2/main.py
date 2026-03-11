from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Sample Product Data
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Shoes", "price": 3000, "category": "Fashion", "in_stock": False},
    {"id": 4, "name": "Watch", "price": 5000, "category": "Fashion", "in_stock": True}
]

orders = []

# DAY----1

# 1️-- Get All Products

# -----------------------------
@app.get("/products")
def get_products():
    return {"products": products}


# -----------------------------
# 2️- Get Products by Category
# -----------------------------
@app.get("/products/category")
def get_products_by_category(category: str):
    result = []
    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)

    return {"products": result}


# -----------------------------
# 3️- Search Product by Name
# -----------------------------
@app.get("/products/search")
def search_products(name: str):
    result = []
    for product in products:
        if name.lower() in product["name"].lower():
            result.append(product)

    return {"products": result}


# -----------------------------
# 4️- Get Only Products in Stock
# -----------------------------
@app.get("/products/in-stock")
def get_in_stock_products():
    result = []

    for product in products:
        if product["in_stock"] == True:
            result.append(product)

    return {"products": result}


# -----------------------------
# 5️- Get Product by ID
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Product not found"}


#Cheapest & Most Expensive Product


@app.get("/products/price-summary")
def price_summary():

    cheapest_product = min(products, key=lambda p: p["price"])
    expensive_product = max(products, key=lambda p: p["price"])

    return {
        "cheapest_product": cheapest_product,
        "most_expensive_product": expensive_product
    }

# -----------------------------
# DAY 2 TASKS
# -----------------------------

# 1-Filter Products by Minimum Price
@app.get("/products/minprice")
def filter_min_price(min_price: int = Query(None)):

    if min_price is not None:
        result = [p for p in products if p["price"] >= min_price]
    else:
        result = products

    return {"filtered_products": result, "count": len(result)}


# -----------------------------
# 2- Get Only the Price of a Product
# -----------------------------
@app.get("/product/{product_id}/price")
def get_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {"price": product["price"]}

    return {"error": "Product not found"}


# -----------------------------
# 3- Accept Customer Feedback
# -----------------------------
class Feedback(BaseModel):
    customer_name: str
    product_name: str
    message: str


@app.post("/feedback")
def accept_feedback(feedback: Feedback):

    return {
        "message": "Feedback received successfully",
        "data": feedback
    }


# -----------------------------
# 4- Product Summary Dashboard
# -----------------------------
@app.get("/products/dashboard")
def product_dashboard():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"]])

    out_of_stock = len([p for p in products if not p["in_stock"]])

    avg_price = sum(p["price"] for p in products) / total_products

    return {
        "total_products": total_products,
        "in_stock_products": in_stock,
        "out_of_stock_products": out_of_stock,
        "average_price": avg_price
    }


# -----------------------------
# 5- Validate & Place Bulk Order
# -----------------------------
class Order(BaseModel):
    product_ids: List[int]


@app.post("/order/bulk")
def place_bulk_order(order: Order):

    valid_products = []
    invalid_products = []

    for pid in order.product_ids:

        found = False

        for p in products:
            if p["id"] == pid:
                found = True

                if p["in_stock"]:
                    valid_products.append(p)
                else:
                    invalid_products.append({
                        "id": pid,
                        "reason": "Out of stock"
                    })

        if not found:
            invalid_products.append({
                "id": pid,
                "reason": "Product not found"
            })

    orders.append(valid_products)

    return {
        "ordered_products": valid_products,
        "invalid_products": invalid_products
    }


# -----------------------------
#  Order Status Tracker
# -----------------------------
@app.get("/orders/status")
def order_status():

    total_orders = len(orders)

    total_items = sum(len(order) for order in orders)

    return {
        "total_orders": total_orders,
        "total_products_ordered": total_items
    }