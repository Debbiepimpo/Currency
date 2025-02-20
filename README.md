# Cardia API

## Description

Cardia is a RESTful API for managing products and orders, built using Django and Django REST Framework. It supports CRUD operations for products and allows creating and managing orders associated with those products.

---

## Requirements

- **Python 3.10+**
- **pip** (Python's package manager)
- SQLite database (preconfigured in the project)

---

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/cardia.git
   cd cardia
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
3. **Run migrations**:
    ```bash
    python manage.py migrate
4. **Start the development server**:
    ```bash
    python manage.py runserver
   ```
   The server will be available at http://127.0.0.1:8000.

--- 
ENDPOINTS

## Product Endpoints

- **List all products**: `GET /api/products/`
- **Create a new product**: `POST /api/products/add-product/`
- **Retrieve a specific product**: `GET /api/products/{id}/`
- **Update a product**: `PUT /api/products/update-product/{id}/`
- **Delete a product**: `DELETE /api/products/delete-product/{id}/`
      

## Order Endpoints

- **List all orders**: `GET /api/orders/`
- **Create a new order**: `POST /api/orders/add-order/`
- **Retrieve a specific order**: `GET /api/orders/{id}/`
- **Update an order**: `PUT /api/orders/update-order/{id}/`
- **Delete an order**: `DELETE /api/orders/delete-order/{id}/`
