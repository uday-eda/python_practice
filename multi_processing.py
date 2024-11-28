import csv
import logging
import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue

def create_timestamped_logfile():
    """
    Creates a new log file with the current timestamp as the filename.

    Args:
        None

    Returns:
        None

    Raises:
        OSError: If there is an issue creating or accessing the log file.
        ValueError: If the timestamp format is invalid.
    """
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"web_scraper_{timestamp}.log"
        logging.basicConfig(
            filename=filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info(f"Log file created successfully.")
    except Exception as e:
        logging.error(f"Failed to create log file.")

create_timestamped_logfile()

def fetch_https_links(soup):
    """
    Extract all HTTPS links from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
        list: A list of HTTPS links found in the webpage.

    Raises:
        Exception: If any error occurs during link extraction.
    """
    try:
        return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://')]
    except Exception as e:
        logging.error(f"Error extracting HTTPS links: {e}")
        return []


def fetch_title(soup):
    """
    Extract the title from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
        str: The title of the webpage or a default string if no title is found.

    Raises:
        Exception: If any error occurs during title extraction.
    """
    try:
        return soup.title.string.strip() if soup.title else "No Title Found"
    except Exception as e:
        logging.error(f"Error extracting title: {e}")
        return "Error extracting title"


def fetch_meta_description(soup):
    """
    Extract the meta description from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
        str: The meta description content or a default string if not found.

    Raises:
        Exception: If any error occurs during meta description extraction.
    """
    try:
        meta_tag = soup.find("meta", attrs={"name": "description"})
        return meta_tag["content"].strip() if meta_tag else "No Meta Description Found"
    except Exception as e:
        logging.error(f"Error extracting meta description: {e}")
        return "Error extracting meta description"


def count_paragraphs(soup):
    """
    Count the number of paragraph tags in the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
        int: The number of paragraph tags in the webpage.

    Raises:
        Exception: If any error occurs during paragraph counting.
    """
    try:
        return len(soup.find_all("p"))
    except Exception as e:
        logging.error(f"Error counting paragraphs: {e}")
        return 0


def fetch_site_info(url, queue):
    """
    Fetch website information including title, meta description, number of paragraphs,
    and HTTPS links. Send the data to the queue.

    Args:
        url (str): The URL of the website to fetch data from.
        queue (Queue): The multiprocessing queue to store the fetched data.

    Returns:
        None

    Raises:
        None: All exceptions are handled internally.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = fetch_https_links(soup)
        site_info = {
            "url": url,
            "title": fetch_title(soup),
            "meta_description": fetch_meta_description(soup),
            "num_paragraphs": count_paragraphs(soup),
            "num_links": len(links),
            "links": links
        }
        queue.put(site_info,block=True, timeout=10)
        logging.info(f"Successfully fetched data for {url}")  # Wait for 10 seconds if queue is full
    except requests.RequestException as e:
        queue.put({"url": url, "error": str(e)})
        logging.error(f"Request error for {url}: {e}")
    except Exception as e:
        queue.put({"url": url, "error": f"Unexpected error: {e}"})
        logging.error(f"Unexpected error for {url}: {e}")


def save_to_csv(queue, file_name="website_info.csv"):
    """
    Save the extracted website information from the queue to a CSV file.

    Args:
        queue (Queue): The multiprocessing queue containing the website data.
        file_name (str): The name of the CSV file to save the data.

    Returns:
        None

    Raises:
        Exception: If an error occurs while writing to the CSV file.
    """
    try:
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Website", "Title", "Meta Description", "Number of Paragraphs", "Number of Links",
                             "HTTPS Links", "Error"])

            while not queue.empty():
                site_info = queue.get()
                if "error" in site_info:
                    writer.writerow([site_info["url"], "", "", "", "", "", site_info["error"]])
                else:
                    writer.writerow([
                        site_info["url"],
                        site_info["title"],
                        site_info["meta_description"],
                        site_info["num_paragraphs"],
                        site_info["num_links"],
                        ", ".join(site_info["links"][:])  # Save only the first 5 links as a sample
                    ])
        logging.info(f"Data saved successfully to {file_name}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")


def main():
    """
    Main function to fetch website information concurrently and save it to a CSV file.

    Args:
        None

    Returns:
        None

    Raises:
        None: All exceptions are handled internally.
    """
    try:
        websites = [
            "https://www.wikipedia.org",
            "https://www.python.org",
            "https://www.example.com",
            "https://www.bbc.com",
            "https://www.github.com"
        ]

        queue = Queue()
        processes = []

        for url in websites:
            process = Process(target=fetch_site_info, args=(url, queue))
            processes.append(process)
            process.start()
            logging.info(f"Process started for {url}")

        for process in processes:
            process.join()

        save_to_csv(queue)
        print("Website information has been saved to 'website_info.csv'.")
        logging.info("Program completed successfully")
    except Exception as e:
        logging.error(f"Error in main function: {e}")


if __name__ == "__main__":
    main()

