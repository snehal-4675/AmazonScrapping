import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a product page
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract ASIN
    asin = soup.find('th', string='ASIN').find_next('td').text.strip()

    # Extract product description
    product_description = soup.find('div', {'id': 'productDescription'}).text.strip()

    # Extract manufacturer
    manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()

    return asin, product_description, manufacturer

# Function to scrape product details from multiple product URLs
def scrape_product_urls(product_urls):
    product_data = []

    for url in product_urls:
        print(f"Scraping URL: {url}")
        asin, product_description, manufacturer = scrape_product_details(url)

        product_data.append({
            'URL': url,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        })

    return product_data

# URL of the product listing page
url = 'https://www.amazon.in/s?k=bags&crid=2M096C6104MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg='

# Number of pages to scrape for product URLs
num_pages = 20

# Scrape the product URLs
product_urls = scrape_amazon_products(url, num_pages)

# Limit the number of URLs to 200
product_urls = product_urls[:200]

# Scrape additional information from the product URLs
product_data = scrape_product_urls(product_urls)

# Save the scraped data to a CSV file
csv_file = 'amazon_products_additional_info.csv'
fieldnames = ['URL', 'ASIN', 'Product Description', 'Manufacturer']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Scraping completed successfully!")
