import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# List of data sources
sources = ['https://www.dawn.com/','https://www.bbc.com/']

def preprocess_link(base_url, link):
    # Join the base URL and the link to get the absolute URL
    absolute_url = urljoin(base_url, link)
    return absolute_url

def scrape_and_preprocess(source_url):
    try:
        # Send a GET request to the URL
        response = requests.get(source_url)
        
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract links, titles, and descriptions
            links = []
            titles = []
            descriptions = []
            
            # Extract links on the landing page
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    preprocessed_link = preprocess_link(source_url, href)
                    links.append(preprocessed_link)
            
            # Extract titles and descriptions from articles displayed on the homepage
            for article in soup.find_all('article'):
                title = article.find('h2')
                description = article.find('p')
                if title and description:
                    titles.append(title.text.strip())
                    descriptions.append(description.text.strip())
            
            # Save the data to a CSV file
            with open('data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                # Write the data to the CSV file
                for link, title, description in zip(links, titles, descriptions):
                    csv_writer.writerow([source_url, link, title, description])
                    
            print(f"Data saved to data.csv for {source_url}")
        else:
            print(f"Failed to retrieve data from {source_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while scraping {source_url}: {str(e)}")

# Loop through the list of sources and scrape each website
for source in sources:
    print(f"Scraping data from {source}:")
    scrape_and_preprocess(source)
    print()
