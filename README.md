# 🧾 Invoice Management API

A simple Invoice Management System built using **Django (Backend API)** for handling users, items, and invoices.  
This project is designed for a Flutter frontend integration.

---

# 🚀 Features

## 👤 User Module
- User Registration
- User Login
- Admin approval required for login

## 📦 Item Module
- Add Items (Goods / Service)
- HSN/SAC validation (6-digit)
- Taxable / Non-taxable selection
- View all items
- Delete item

## 🧾 Invoice Module
- Create invoice with multiple items
- Customer details (name, email, phone, address)
- Date selection
- View invoices
- Delete invoice (user only)

## 👨‍💼 Admin Features
- View users
- Approve users
- View all items
- View all invoices

---

# 🛠 Tech Stack

- Python 3.x
- Django
- Django REST (custom JSON APIs)
- SQLite (default database)

---

# 📡 API Endpoints

## 🔐 Authentication
- POST `/api/register/` → Register user  
- POST `/api/login/` → Login user  

---

## 📦 Items
- POST `/api/add-item/` → Add item  
- GET `/api/items/` → Get all items  
- DELETE `/api/delete-item/<id>/` → Delete item  

---

## 🧾 Invoices
- POST `/api/create-invoice/` → Create invoice  
- GET `/api/invoices/` → Get invoices  
- DELETE `/api/delete-invoice/<id>/` → Delete invoice  

---

# ⚙️ Setup Instructions

## 1️⃣ Clone project
```bash
git clone https://github.com/yourusername/invoice-backend.git
cd invoice-backend
