from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Sample Product Data
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Shoes", "price": 3000, "category": "Fashion", "in_stock": False},
    {"id": 4, "name": "Watch", "price": 5000, "category": "Fashion", "in_stock": True}
]

orders = []

# DAY 1

# Q1 -- Get All Products
@app.get("/products")
def get_products():
    return {"products": products}


# Q2 -- Get Products by Category
@app.get("/products/category")
def get_products_by_category(category: str):

    result = []

    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)

    return {"products": result}





# Q3 -- Get Only Products in Stock
@app.get("/products/in-stock")
def get_in_stock_products():

    result = []

    for product in products:
        if product["in_stock"]:
            result.append(product)

    return {"products": result}



#  Q4 — STORE SUMMARY


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

    return {"products": result}




# Bonus -- Cheapest & Most Expensive Product
@app.get("/products/price-summary")
def price_summary():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "cheapest_product": cheapest,
        "most_expensive_product": expensive
    }



