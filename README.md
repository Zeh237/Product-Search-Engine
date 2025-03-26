# Elasticsearch Search Engine Project Setup

This project implements a search engine using Elasticsearch, allowing you to index and search product data. It's built with Python 3.12 and utilizes Flask for the API.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.12:**  Make sure you have Python 3.12 installed on your system.
2.   **Elasticsearch:** You need a running Elasticsearch instance. You can download and install it from the official Elasticsearch website ([https://www.elastic.co/

downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)).
    *   **Note:** Ensure Elasticsearch is running on the default port (9200) or configure the connection details in the project accordingly.
    *   **Docker (Recommended):** 

3.  **Pip:** Python's package installer. It usually comes with Python.

## Project Setup

Follow these steps to set up the project:

1.  **Clone the Repository:**
   git clone github.com/Zeh237/Elasticsearch-Products-Search-Engine.git

2.  **Create a Virtual Environment (Highly Recommended):**
    python3 -m venv venv

3.  **Activate the Virtual Environment:**
    *   **Linux/macOS:**
      source venv/bin/activate
    *   **Windows:**
      env\Scripts\activate

4.  **Install Dependencies:**
    pip install -r requirements.txt

5.  **Environment Variables:**
    *   Create a `.env` file in the root directory of the project.
    *   use the env.example file as a guide for the environment variables needed:

6. **Database Setup**
    *   Make sure you have a database running, and that you have created the database for the project(mysql database).
    *   in the root folder of this project, you will see the products and category tables as csv. import them into your database using workbench or any other tool of your choice

7.  **Run the Application:**
     flask run