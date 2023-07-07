import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a product listing page
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    product_data = []
    for product in products:
        product_url = product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()

        rating = product.find('span', {'class': 'a-icon-alt'})
        if rating:
            rating = rating.text.strip()
        else:
            rating = ''

        review_count = product.find('span', {'class': 'a-size-base'})
        if review_count:
            review_count = review_count.text.strip()
        else:
            review_count = ''

        product_data.append({
            'URL': product_url,
            'Name': product_name,
            'Price': product_price,
            'Rating': rating,
            'Review Count': review_count
        })

    return product_data

# Function to scrape product details from multiple product listing pages
def scrape_amazon_products(url, num_pages):
    all_products = []

    for page in range(1, num_pages + 1):
        page_url = url + str(page)
        print(f"Scraping page {page}: {page_url}")
        product_data = scrape_product_details(page_url)
        all_products.extend(product_data)

    return all_products

# URL of the product listing page
url = 'https://www.amazon.in/s?k=bags&crid=2M096C6104MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg='

# Number of pages to scrape
num_pages = 20

# Scrape the data
product_data = scrape_amazon_products(url, num_pages)

# Save the scraped data to a CSV file
csv_file = 'amazon_products.csv'
fieldnames = ['URL', 'Name', 'Price', 'Rating', 'Review Count']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Scraping completed successfully!")






