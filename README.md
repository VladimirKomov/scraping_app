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


