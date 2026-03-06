from fastapi import FastAPI

app = FastAPI()

# Sample Product Data
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Shoes", "price": 3000, "category": "Fashion", "in_stock": False},
    {"id": 4, "name": "Watch", "price": 5000, "category": "Fashion", "in_stock": True}
]

# 1️⃣ Get All Products
@app.get("/products")
def get_products():
    return {"products": products}


# 2️⃣ Get Products by Category
@app.get("/products/category")
def get_products_by_category(category: str):
    result = []
    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)
    return {"products": result}


# 3️⃣ Search Product by Name
@app.get("/products/search")
def search_products(name: str):
    result = []
    for product in products:
        if name.lower() in product["name"].lower():
            result.append(product)
    return {"products": result}


# 4️⃣ Get Only Products in Stock
@app.get("/products/in-stock")
def get_in_stock_products():
    result = []
    for product in products:
        if product["in_stock"] == True:
            result.append(product)
    return {"products": result}


# 5️⃣ Get Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"message": "Product not found"}