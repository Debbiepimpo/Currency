# 🏦 Currency Exchange API

An API for currency conversion and exchange rate queries, built with **Django 5**, **Django Rest Framework**, and **Python 3.10**.

## 📌 Technologies Used
- **Python 3.10**
- **Django 5**
- **Django REST Framework**
- **Pipenv** (for virtual environment management)
- **SQLite/PostgreSQL** (depending on configuration)
- **CurrencyBeacon API** (to fetch real-time exchange rates)

---

## ⚙️ **Local Setup Instructions**

### 1️⃣ **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/Currency.git # Using HTTPS
   git clone git@github.com:Debbiepimpo/Currency.git # Using SSH
```

### 2️⃣ **Install the Virtual Environment using pipenv**
    ```bash
    pip install pipenv
    pipenv install
```
### 3️⃣ **Install dependencies and setup Database**
    ```bash
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    ```
### 4️⃣ **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```
    - Follow the instructions and provide a username, email, and password.

### 5️⃣ **Run the Project**
    ```bash
    python manage.py runserver
   ```
   The server will be available at http://127.0.0.1:8000/.


# 📌 Required Configuration in Django Admin

To ensure the API functions properly, you must configure **Currencies** and **Providers** in the Django admin panel.

## 🛠 Steps to Configure

1. **Go to the Django Admin Panel**  
   👉 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

2. **Add Currencies** in **Currency**:
   - **Code**: `EUR`, `USD`, `GBP`, etc.
   - **Name**: `Euro`, `Dollar`, `Pound`, etc.

3. **Add Providers** in **Provider**:
   - **Name**: `CurrencyBeacon` or `Mock`
   - **Priority**: `1` for **primary**, `2` for **secondary**
   - **Active**: ✅ **(Checked/Enabled)**

📌 **Note:** Ensure that at least one provider is active for the API to work correctly.

# 🔥 Available Endpoints

## 📍 1️⃣ Latest Exchange Rates
`Get /api/currency-rates/latest/`

### 📌 Example Response:

```json
{
    "base_currency": "EUR",
    "rates": {
        "USD": 1.08,
        "GBP": 0.85
    }
}
```

## 📍 2️⃣ Historical Exchange Rates
`Get /api/currency-rates/historical/`

### 📌 Example Response:

```json
{
    "base_currency": "EUR",
    "date": "2025-02-15",
    "rates": {
        "USD": 1.07,
        "GBP": 0.84
    }
}
```

## 📍 3️⃣ Exchange Rates Over a Time Range
`Get /api/currency-rates/timeseries/`

### 📌 Example Response:

```json
{
    "list": {
        "2025-02-15": {
            "USD": 1.07,
            "GBP": 0.84
        },
        "2025-02-16": {
            "USD": 1.08,
            "GBP": 0.85
        }
    }
}
```

## 📍 4️⃣ Currency Conversion
`Get /api/currency-rates/convert/`

### 📌 Example Response:

```json
{
    "from": "USD",
    "to": "EUR",
    "amount": 100,
    "converted_amount": 92.50
}
```
