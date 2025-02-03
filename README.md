# API Data Scraper

This project is designed to fetch product data from the API and store it in a MongoDB database. It utilizes authentication via the API and dynamically creates collections for each store's products.

## Features
- Fetches product data from API using search terms.
- Stores product data in MongoDB with collections dynamically created per store.
- Uses pagination to retrieve all available products efficiently.
- Runs with MongoDB inside a Docker container for easy setup.

## Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8+

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add the required environment variables:
   ```ini
   BASE_URL=< API base URL>
   ```

4. **Run MongoDB using Docker:**
   ```bash
   docker-compose up -d
   ```
   This will start MongoDB in a Docker container with credentials `admin/password` and persist data using a volume.

5. **Run the script to fetch product data:**
   ```bash
   python main.py
   ```

## API Authentication
The script uses client credentials to authenticate with the API. Tokens are cached to avoid unnecessary requests. If a token expires, the script automatically retrieves a new one.

## MongoDB Data Storage
- MongoDB runs inside Docker with the container name `mongodb_your_name`.
- Product data is stored in collections named `products_store_<store_id>`.
- Data includes `productId`, `name`, `price`, and other relevant attributes.

## Stopping & Cleaning Up
To stop the MongoDB container:
```bash
docker-compose down
```
To remove all data (use with caution):
```bash
docker-compose down -v
```

## Contributing
Feel free to submit pull requests or suggest improvements.


### Added the function random of falling asleep (random.uniform(1, 5))


## 🛠 Deployment in Docker (Branch `docker`)

The `dev` branch now includes Docker support, allowing the application to run inside a container.

### 📌 **How to Run the Application in Docker**
1. **Clone the repository and switch to the `docker` branch**:
   ```sh
   git clone https://github.com/VladimirKomov/scraping_app.git
   cd scraping_app
   git checkout dev
   ```

2. **Start the containers (application + MongoDB)**:
   ```sh
   docker-compose up --build -d
   ```

3. **Verify that the containers are running**:
   ```sh
   docker ps
   ```

4. **Check if the API is running**:
   ```sh
   curl http://localhost:8000/
   ```

5. **API documentation is available at**:
   ```
   http://localhost:8000/docs
   ```

### ⚙ **Docker Structure**
- **MongoDB** (`mongodb_kroger`) — Database container.
- **FastAPI application** (`scraping_app`) — API server running inside the container.

### 🔧 **Useful Commands**
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

Now the application is fully containerized and runs inside **Docker**. 🚀


