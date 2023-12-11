import os
import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin, urlparse, quote

def get_domain(url):
    ext = tldextract.extract(url)
    return ext.domain

def parse_links(soup, url):
    domain = get_domain(url)
    with open(f'{domain}_Links.txt', 'w') as file:
        links = [a['href'] for a in soup.find_all('a', href=True)]
        for link in links:
            file.write(link + '\n')
    print(f'Links saved to {domain}_Links.txt')

def download_images(soup, url):
    domain = get_domain(url)
    image_folder = f'./{domain}_images/'
    os.makedirs(image_folder, exist_ok=True)

    images = [img['src'] for img in soup.find_all('img', src=True)]
    for img_url in images:
        try:
            if not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(url, img_url)

            img_data = requests.get(img_url).content

            # Generate a valid filename with a .jpg extension by default
            img_name = os.path.join(image_folder, f'image_{hash(img_url)}.jpg')
            
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            print(f'Downloaded: {img_name}')
        except Exception as e:
            print(f'Error downloading image: {e}')

def main():
    url = input("Enter the URL of the site: ")

    if not urlparse(url).scheme:
        protocol = input("Choose a protocol (http or https): ")
        url = f'{protocol}://{url}'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        option = input("What do you want to parse for?\n1. Links\n2. Images\n")

        if option == '1':
            parse_links(soup, url)
        elif option == '2':
            download_images(soup, url)
        else:
            print("Invalid option. Please choose 1 or 2.")
    else:
        print(f"Failed to retrieve the content. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
