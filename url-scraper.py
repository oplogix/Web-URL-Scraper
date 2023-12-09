import argparse
import csv
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Scraper:
    def __init__(self, site):
        self.site = self.format_url(site)

    def format_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def scrape(self):
        try:
            r = urllib.request.urlopen(self.site)
            html = r.read()
            parser = "html.parser"
            sp = BeautifulSoup(html, parser)

            url_dict = {"LINKS": []}

            for tag in sp.find_all("a", href=True):
                url = tag["href"]
                url_dict["LINKS"].append(url)

            base_name = urlparse(self.site).hostname.replace('www.', '').split('.')[0]

            
            text_output_file = f"{base_name}-scrape.txt"
            csv_output_file = f"{base_name}-scrape.csv"

            with open(text_output_file, "w", encoding="utf-8") as text_file:
                for section, urls in url_dict.items():
                    text_file.write(f"--- {section} ---\n")
                    for url in urls:
                        text_file.write(url + "\n")

            print(f"URLs saved to {text_output_file} successfully.")

            with open(csv_output_file, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Section", "URL"])
                for section, urls in url_dict.items():
                    for url in urls:
                        csv_writer.writerow([section, url])

            print(f"URLs saved to {csv_output_file} successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Web Scraper Tool")
    parser.add_argument("site", nargs="?", help="Website URL to scrape")
    args = parser.parse_args()

    if not args.site:
        parser.print_help()
        print("\nExample:")
        print("python web_scraper.py www.example.com")
        return

    scraper = Scraper(args.site)
    scraper.scrape()

if __name__ == "__main__":
    main()
