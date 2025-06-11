# FastAPI || E-Commerce API

This is a simple E-Commerce backend built with **FastAPI**, supporting:

- JWT-based user authentication
- Cart management (add, update, remove)
- Dummy checkout
- Order history and details
- Structured responses and Error logging

---

## Project Structure

```
app/
├── auth/              # User registration, login
├── cart/              # Cart routes and logic
├── core/              # Database and main settings
├── models/            # SQLAlchemy models
├── orders/            # Order listing and detail routes
├── utils/             # Common utilities (e.g., responses)
└── main.py            # App entrypoint
logs/
└── logs.txt           # Runtime error and request logs
```

---

## Entity Relationship Diagram (ERD)

![ERD](./ERD/ERD.png)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Gajmain2020/NT-Python-Cap.git
cd PythonCap
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


### 4. Create .env file
Create .env file and add the following variables:
```bash
# FOR DATABASE CONFIG
DATABASE_URL

# FOR JWT RELATED CONFIG
JWT_SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS

# FOR PASSWORD RESET CAN USE BREVO STMTP SERVICES
EMAIL_HOST
EMAIL_PORT
EMAIL_USERNAME
EMAIL_PASSWORD
EMAIL_FROM
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

The API Docs will be availabel at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Author

Made by [Gajendra Sahu](https://gajju2309.vercel.app). Contributions welcome!

---