# Scraping App

This project is designed to **fetch product data from an API** and store it in a **MongoDB database**.  
It supports two different environments:
- **`main` branch**: Standard Python environment using Poetry (no Docker).
- **`docker` branch**: Fully containerized setup with Docker and WebSocket-based logging.

---

## 🛠 Manual Installation & Setup (Branch `main`)

The **`main` branch** is designed for running the application **without Docker**.

### **1️⃣ Clone the repository and switch to `main`**
```sh
git clone https://github.com/VladimirKomov/scraping_app.git
cd scraping_app
git checkout main
```

### **2️⃣ Install dependencies with Poetry**
```sh
poetry install
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file in the root directory and add the required API credentials:
```ini
BASE_URL=<API_BASE_URL>
API_KEY=<YOUR_API_KEY>
MONGO_URI=mongodb://admin:password@localhost:27017/
```

### **4️⃣ Start MongoDB manually**
If you're not using Docker, you need a running MongoDB instance:
```sh
mongod --dbpath=data/db --port 27017
```

### **5️⃣ Run the application with Poetry**
```sh
poetry run python main.py
```

---

## 🚀 Deployment in Docker (Branch `docker`)

The **`docker` branch** includes **full Docker support** and adds **real-time logging** via WebSockets.

### **1️⃣ Clone the repository and switch to `docker`**
```sh
git clone https://github.com/VladimirKomov/scraping_app.git
cd scraping_app
git checkout docker
```

### **2️⃣ Start the containers (FastAPI + MongoDB)**
```sh
docker-compose up --build -d
```

### **3️⃣ Verify that everything is running**
```sh
docker ps
```

### **4️⃣ Check if the API is running**
```sh
curl http://localhost:8000/
```

### **5️⃣ API documentation**
```
http://localhost:8000/docs
```

---

## ⚙ **Key Differences Between `main` and `docker`**
| Feature             | `main` Branch | `docker` Branch |
|---------------------|--------------|----------------|
| **Runs with Poetry** | ✅ Yes       | ❌ No (Uses Docker) |
| **Requires local MongoDB** | ✅ Yes | ❌ No (Uses Docker MongoDB) |
| **WebSocket Logging** | ❌ No | ✅ Yes |
| **Easier setup** | ❌ No | ✅ Yes (One command) |

---

## 🔧 **WebSocket Logging (`docker` branch only)**
The `docker` branch supports **real-time logging in the browser** using WebSockets.

### **How to View Logs in the Browser**
1. Open:
   ```
   http://localhost:8000/static/logs.html
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
docker logs -f scraping_app
```

📌 **Access the application container shell**:
```sh
docker exec -it scraping_app sh
```

Now the application supports both **Poetry (main branch)** and **Docker (docker branch) with real-time logging!** 🚀

