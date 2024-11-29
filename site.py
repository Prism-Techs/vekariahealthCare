import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import mimetypes
import re

class WebsiteCloner:
    def __init__(self, base_url, output_dir):
        self.base_url = base_url
        self.output_dir = output_dir
        self.downloaded_files = set()
        self.session = requests.Session()
        # Set a User-Agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def download_resource(self, url, resource_type):
        """Download a resource (CSS, JS, image, etc.) and save it locally"""
        if url in self.downloaded_files or not url.startswith(('http://', 'https://')):
            return url

        try:
            # Create the local path
            parsed = urlparse(url)
            local_path = os.path.join(self.output_dir, resource_type, parsed.path.lstrip('/'))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download the resource
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                self.downloaded_files.add(url)
                return os.path.relpath(local_path, self.output_dir)
            return url
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return url

    def process_html(self, html_content):
        """Process HTML content and download all associated resources"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Process CSS files
        for css_tag in soup.find_all('link', rel='stylesheet'):
            if css_tag.get('href'):
                absolute_url = urljoin(self.base_url, css_tag['href'])
                local_path = self.download_resource(absolute_url, 'css')
                css_tag['href'] = local_path

        # Process JavaScript files
        for js_tag in soup.find_all('script', src=True):
            absolute_url = urljoin(self.base_url, js_tag['src'])
            local_path = self.download_resource(absolute_url, 'js')
            js_tag['src'] = local_path

        # Process images
        for img_tag in soup.find_all('img', src=True):
            absolute_url = urljoin(self.base_url, img_tag['src'])
            local_path = self.download_resource(absolute_url, 'images')
            img_tag['src'] = local_path

        return str(soup)

    def clone(self):
        """Main method to clone the website"""
        try:
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)

            # Download the main page
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                # Process the HTML and save all resources
                processed_html = self.process_html(response.text)
                
                # Save the main HTML file
                index_path = os.path.join(self.output_dir, 'index.html')
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(processed_html)
                
                print(f"Website cloned successfully to {self.output_dir}")
                return True
            else:
                print(f"Failed to download the webpage. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error cloning website: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    url = "https://fairfoul-dark.dora.run/"  # Replace with the website you want to clone
    output_directory = "cloned_website"
    
    cloner = WebsiteCloner(url, output_directory)
    cloner.clone()