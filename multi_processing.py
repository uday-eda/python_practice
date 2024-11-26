from multiprocessing import Process, Queue
import requests
from bs4 import BeautifulSoup
import csv


# Function to fetch links and other info from a single website
def fetch_site_info(url, queue):
    try:
        response = requests.get(url, timeout=5)  # Fetch website content
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML

        # Extract HTTPS links
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://')]

        # Extract title
        title = soup.title.string.strip() if soup.title else "No Title Found"

        # Extract meta description
        meta_description = (
            soup.find("meta", attrs={"name": "description"})
        )
        meta_description = (
            meta_description["content"].strip() if meta_description else "No Meta Description Found"
        )

        # Count number of paragraphs
        num_paragraphs = len(soup.find_all("p"))

        # Send all extracted data to the queue
        queue.put({
            "url": url,
            "title": title,
            "meta_description": meta_description,
            "num_paragraphs": num_paragraphs,
            "num_of_links": len(links),
            "links": links
        })
    except requests.RequestException as e:
        queue.put({"url": url, "error": str(e)})  # Send error info to the queue


if __name__ == "__main__":
    # List of websites to fetch info from
    websites = [
        "https://www.wikipedia.org",
        "https://www.python.org",
        "https://www.example.com",
        "https://www.bbc.com",
        "https://www.github.com"
    ]

    queue = Queue()  # Create a queue for inter-process communication
    processes = []  # List to keep track of processes

    # Create and start a process for each website
    for url in websites:
        process = Process(target=fetch_site_info, args=(url, queue))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Write results to a CSV file
    with open("website_info.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(
            ["Website", "Title", "Meta Description", "Number of Paragraphs", "Number of links", "HTTPS Links", "Error"])

        # Write each website's data
        while not queue.empty():
            site_info = queue.get()
            if "error" in site_info:
                writer.writerow([site_info["url"], "", "", "", "", site_info["error"]])
            else:
                writer.writerow([
                    site_info["url"],
                    site_info["title"],
                    site_info["meta_description"],
                    site_info["num_paragraphs"],
                    site_info["num_of_links"],
                    ", ".join(site_info["links"][:])
                ])

    print("Website information has been saved to 'website_info.csv'.")

