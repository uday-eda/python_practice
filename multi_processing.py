from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup

# Function to fetch links from a single website
def fetch_links(url):
    try:
        response = requests.get(url, timeout=5)  # Fetch website content
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML

        # Extract all anchor tags with href attributes
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://')]
        return {url: links}  # Return links as a dictionary
    except requests.RequestException as e:
        return {url: f"Error: {e}"}  # Handle request exceptions

if __name__ == "__main__":
    # List of websites to fetch links from
    websites = [
        "https://www.wikipedia.org",
        "https://www.python.org",
        "https://www.example.com",
        "https://www.bbc.com",
        "https://www.github.com"
    ]

    # Create a pool of processes
    with Pool(len(websites)) as pool:
        # Fetch links in parallel
        results = pool.map(fetch_links, websites)

    # Aggregate and print the results
    print("Fetched Links:")
    for site_links in results:
        for site, links in site_links.items():
            print(f"Website: {site}")
            if isinstance(links, list):
                print(f"Found {len(links)} links:")
                print(links[:5])  # Display only the first 5 links
            else:
                print(links)  # Print error message
            print()