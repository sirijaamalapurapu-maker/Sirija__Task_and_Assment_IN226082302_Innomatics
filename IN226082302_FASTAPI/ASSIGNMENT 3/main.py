from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# Sample Product Data
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Shoes", "price": 3000, "category": "Fashion", "in_stock": False},
    {"id": 4, "name": "Watch", "price": 5000, "category": "Fashion", "in_stock": True},

    # Added Products (Q1 requirement)
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

orders = []

# =========================================
# DAY 1
# =========================================

# Q1 -- Get All Products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# Q2 -- Get Products by Category
@app.get("/products/category")
def get_products_by_category(category: str):

    result = []

    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)

    if len(result) == 0:
        return {"error": "No products found in this category"}

    return {
        "category": category,
        "products": result,
        "total": len(result)
    }


# Q3 -- Get Only Products in Stock
@app.get("/products/in-stock")
def get_in_stock_products():

    result = []

    for product in products:
        if product["in_stock"]:
            result.append(product)

    return {
        "in_stock_products": result,
        "count": len(result)
    }


# Q4 — STORE SUMMARY
@app.get("/store/summary")
def store_summary():

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }


# Q5 -- Search Product by Name
@app.get("/products/search")
def search_products(name: str):

    result = []

    for product in products:
        if name.lower() in product["name"].lower():
            result.append(product)

    if len(result) == 0:
        return {"message": "No products matched your search"}

    return {
        "keyword": name,
        "results": result,
        "total_matches": len(result)
    }


# Bonus -- Cheapest & Most Expensive Product
@app.get("/products/price-summary")
def price_summary():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }






# DAY 2

# Q1 -- Filter Products 

@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None)
):

    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    return {"filtered_products": result}


# Q2 -- Get Only Price of Product
@app.get("/product/{product_id}/price")
def get_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {"price": product["price"]}

    return {"error": "Product not found"}


# Q3 -- Customer Feedback
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


# Q4 -- Product Dashboard
@app.get("/products/dashboard")
def product_dashboard():

    total_products = len(products)

    in_stock = len([p for p in products if p["in_stock"]])
    out_stock = len([p for p in products if not p["in_stock"]])

    avg_price = sum(p["price"] for p in products) / total_products

    return {
        "total_products": total_products,
        "in_stock_products": in_stock,
        "out_of_stock_products": out_stock,
        "average_price": avg_price
    }


# Q5 -- Bulk Order
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
                    invalid_products.append({"id": pid, "reason": "Out of stock"})

        if not found:
            invalid_products.append({"id": pid, "reason": "Product not found"})

    orders.append(valid_products)

    return {
        "ordered_products": valid_products,
        "invalid_products": invalid_products
    }


# Order Status Tracker
@app.get("/orders/status")
def order_status():

    total_orders = len(orders)

    total_items = sum(len(order) for order in orders)

    return {
        "total_orders": total_orders,
        "total_products_ordered": total_items
    }



orders = []

# POST /orders  (create order with pending status)

class OrderRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


@app.post("/orders")
def place_order(order: OrderRequest):

    product = next((p for p in products if p["id"] == order.product_id), None)

    if not product:
        return {"error": "Product not found"}

    if not product["in_stock"]:
        return {"error": "Product out of stock"}

    order_data = {
        "order_id": len(orders) + 1,
        "product": product["name"],
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(order_data)

    return {
        "message": "Order placed successfully",
        "order": order_data
    }


# GET /orders/{order_id}

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}

    return {"error": "Order not found"}


# PATCH /orders/{order_id}/confirm

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"

            return {
                "message": "Order confirmed",
                "order": order
            }
        


        # DAY 3

# Add Product
class NewProduct(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True


@app.post("/products/add")
def add_product(product: NewProduct):

    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {"message": "Product added", "product": new_product}


# Update Product
@app.put("/products/update/{product_id}")
def update_product(product_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):

    for product in products:

        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {"message": "Product updated", "product": product}

    return {"error": "Product not found"}


# Delete Product
@app.delete("/products/delete/{product_id}")
def delete_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return {"message": "Product deleted", "product": product}

    return {"error": "Product not found"}


# Product Audit
@app.get("/products/audit")
def product_audit():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    total_value = sum(p["price"] for p in in_stock)

    most_expensive = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_products": [p["name"] for p in out_stock],
        "total_stock_value": total_value,
        "most_expensive_product": most_expensive
    }


# Apply Discount
@app.put("/products/discount")
def apply_discount(category: str = Query(...), discount_percent: int = Query(..., ge=1, le=90)):

    updated = []

    for product in products:

        if product["category"].lower() == category.lower():

            discount = product["price"] * discount_percent / 100
            product["price"] = int(product["price"] - discount)

            updated.append(product)

    if not updated:
        return {"message": "No products found in this category"}

    return {
        "category": category,
        "discount_percent": discount_percent,
        "updated_products": updated
    }


# IMPORTANT: Dynamic route must be LAST
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Product not found"}