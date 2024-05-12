import requests
from bs4 import BeautifulSoup
import csv

sources = ['https://www.dawn.com/', 'https://www.bbc.com/']

def scrape_website(url):
    try:

        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = soup.find_all('a')
            
            # Save the links to a CSV file
            with open('links.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                # Write the links to the CSV file
                for link in links:
                    csv_writer.writerow([url, link.get('href')])
                    
            print(f"Data saved to links.csv for {url}")
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")

# Loop through the list of sources and scrape each website
for source in sources:
    print(f"Scraping data from {source}:")
    scrape_website(source)
    print()
