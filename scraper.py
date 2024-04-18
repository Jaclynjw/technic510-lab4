import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import psycopg2
from contextlib import closing
import pandas as pd
import streamlit as st
import re

load_dotenv()
# Database connection parameters
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Function to connect to the database
def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS, sslmode='prefer')
    
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    rating INTEGER,
                    price DECIMAL(10, 2)
                );
            """)
            cur.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_title_description
                ON books ((md5(title || description)));
            """)
            conn.commit()
    return conn

def fetch_books(query, params=None):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(results, columns=columns)
    return df

def extract_decimal(value):
    match = re.search(r'\d+\.?\d*', value)
    if match:
        return float(match.group())
    else:
        return None

def scrape_books():
    books = []
    word_to_number = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}
    
    for i in range(1,51):#51
        print(i)
        url = f'http://books.toscrape.com/catalogue/page-{i}.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        for book_info in soup.select('article.product_pod'):
            book = {}
            book['title'] = book_info.h3.a['title']
            book['price'] = extract_decimal(book_info.select('p.price_color')[0].get_text())
            book['rating'] = word_to_number[book_info.select('p.star-rating')[0].get_attribute_list('class')[1]]
            book['url'] = book_info.h3.a['href']
            book_url = 'https://books.toscrape.com/catalogue/' + book['url']
            book_res = requests.get(book_url)
            book_soup = BeautifulSoup(book_res.text, 'html.parser')
            #Fetching book description
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.text, 'html.parser')
            description_tag = book_soup.find('meta', attrs={'name': 'description'})   
            book['description'] = description_tag['content'].strip() if description_tag else 'No description available'
            books.append(book) 

    #save to database 
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            for book in books:
                cur.execute(
                    "INSERT INTO books (title, description, rating, price) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (book['title'], book['description'], book['rating'], book['price'])
                )
            conn.commit()

def main():
    # Initialize the database
    #scrape_books()

    # Set the page title
    st.title("Book Search and Filter")

    # Display all books by default
    default_query = "SELECT DISTINCT title, description, rating, price FROM books ORDER BY title"
    df_default = fetch_books(default_query)
    
    # Create an expander to hide the search options by default to make the UI cleaner
    with st.expander("Search and Filter Options", expanded=False):
        # User input for search
        search_query = st.text_input("Search by book title")

        # Select box for filtering by rating
        rating_filter = st.selectbox("Filter by rating", ("All", "One", "Two", "Three", "Four", "Five"), index=0)

        # Options for ordering
        sort_order = st.selectbox("Order by", ("Rating", "Price"))
        order_direction = st.radio("Order direction", ("Ascending", "Descending"))

        # Build the query based on input
        query = """
        SELECT DISTINCT title, description, rating, price FROM books
        WHERE title ILIKE %s
        """
        params = [f'%{search_query}%']

        word_to_number = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }

        # Add rating filter to the query if needed
        if rating_filter != "All":
            query += " AND rating = %s"
            params.append(word_to_number[rating_filter])

        # Add order by clause
        if sort_order == "Rating":
            query += f" ORDER BY rating { 'ASC' if order_direction == 'Ascending' else 'DESC' }"
        else:
            query += f" ORDER BY price { 'ASC' if order_direction == 'Ascending' else 'DESC' }"

        # Fetch and display the data based on user input
        if st.button("Search"):
            df = fetch_books(query, params)
            if not df.empty:
                st.dataframe(df)
            else:
                st.write("No books found matching the criteria.")

    # Display all books by default outside the expander
    st.write("### All Books", unsafe_allow_html=True)
    st.dataframe(df_default, 800, 300)


if __name__ == '__main__':
    main()