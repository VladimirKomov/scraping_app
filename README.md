# Scraping App

This project is designed to **fetch product data from an API** and store it in a **MongoDB database**. It includes:
- **FastAPI backend** for API endpoints and WebSocket-based logging.
- **React frontend** for an intuitive user interface.

---

## 🔥 New Feature: Intelligent Ingredient Matching (`scripts/update_ingredients.py`)

This project now includes a **powerful ingredient-matching script** that leverages **AI-powered semantic search** to map product descriptions to relevant ingredients.

### **🔹 What does it do?**
- Extracts **product descriptions** from MongoDB.
- Uses **SentenceTransformers** (`all-MiniLM-L6-v2`) for text embedding.
- Finds the **most relevant ingredient** using **FAISS (fast similarity search)**.
- Updates MongoDB with the **best-matched ingredient name** and **source ID**.

### **🚀 How to Run the Script?**
```sh
python scripts/update_ingredients.py
```

### **📊 How to Verify the Data Update?**
```sh
mongosh
use kroger_db
db.products_store_03400128.countDocuments({ "ingredient_name": { $exists: true } })
```
✅ If the result matches the total number of products, the update was successful!

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/VladimirKomov/scraping_app.git
cd scraping_app
```

### **2️⃣ Install dependencies with Poetry**
```sh
poetry install
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file in the root directory. See the example in the `.env.example` file.

### **4️⃣ Start MongoDB**
Ensure a running MongoDB instance:
```sh
mongod --dbpath=data/db --port 27017
```

### **5️⃣ Run the Application**
```sh
docker-compose up --build
```

---

## 🚀 API Documentation

Once the app is running, you can access the **API documentation** here:
```
http://localhost:8000/docs
```

---

## 🔧 **WebSocket Logging**
The application supports **real-time logging** via WebSockets.

### **How to View Logs in the Browser**
1. Open the following URL in your browser:
```
http://localhost:3000
```
2. Logs will update **in real-time** as the application runs.

---

## 🔧 **Useful Commands**
📌 **Stop all containers**:
```sh
docker-compose down
```

📌 **View application logs**:
```sh
docker logs -f backend_kroger
```

📌 **Access the application container shell**:
```sh
docker exec -it backend_kroger sh
```

