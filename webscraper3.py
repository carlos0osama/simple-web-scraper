import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.ram-e-shop.com/shop/page/"
products = []

for page in range(1, 80):
    url = f"{base_url}{page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for product in soup.find_all('div', class_='o_wsale_product_grid_wrapper'):
            name_tag = product.find('a', class_='text-primary text-decoration-none')
            name = name_tag.text.strip() if name_tag else 'N/A'
            
            link = name_tag['href'] if name_tag else 'N/A'
            
            price_tag = product.find('span', class_='oe_currency_value')
            price = price_tag.text.strip() if price_tag else 'N/A'
            
            products.append([name, link, price])
    else:
        print(f"Failed to fetch page {page}")

df = pd.DataFrame(products, columns=['Product Name', 'Link', 'Price'])
df.to_excel('products.xlsx', index=False)

print("Data saved to products.xlsx")