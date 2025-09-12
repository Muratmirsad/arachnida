import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def download_image(img_url, save_path):
    """Downloads an image from a given URL to the specified path."""
    try:
        # wikipedia gibi bazı sitelerde bot korumasından dolayı
        # 403 yanıtını alıyorum
        response = requests.get(img_url, stream=True, timeout=10)
        response.raise_for_status()  #! check for error codes <--- test this before evo

        filename = os.path.basename(urlparse(img_url).path)
        full_path = os.path.join(save_path, filename)

        with open(full_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        print(f"Downloaded: {img_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error (Download): {img_url} - {e}")
    except Exception as e:
        print(f"Error (File Write): {full_path} - {e}")


def crawl_website(url, max_depth, save_path, recursive):
    """
    Crawls a website to find and download images.
    Handles recursion and depth control.
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    queue = [(url, 0)]
    
    base_netloc = urlparse(url).netloc

    while queue:
        current_url, depth = queue.pop(0)

        if depth > max_depth or current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        print(f"\n🔎 Crawling (Depth: {depth}): {current_url}")

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for img_tag in soup.find_all('img'):
                img_url = img_tag.get('src')
                if not img_url:
                    continue
                
                img_url = urljoin(current_url, img_url)

                if any(img_url.lower().endswith(ext) for ext in image_extensions):
                    download_image(img_url, save_path)
            
            if recursive:
                for a_tag in soup.find_all('a', href=True):
                    link_url = urljoin(current_url, a_tag['href'])
                    if urlparse(link_url).netloc == base_netloc and link_url not in visited_urls:
                        queue.append((link_url, depth + 1))

        except requests.exceptions.RequestException as e:
            print(f"Error (Crawl): {current_url} - {e}")
        except Exception as e:
            print(f"Error (Parse): {current_url} - {e}")


def main():
    """parses arguments and starts the search"""
    parser = argparse.ArgumentParser(description="Recursively downloads images from a website.")
    parser.add_argument("url", help="The URL of the website to start from.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively downloads images.")
    parser.add_argument("-l", "--level", type=int, default=5, help="Maximum depth level for recursive download (default: 5).")
    parser.add_argument("-p", "--path", default="./data/", help="Path to save the downloaded files (default: ./data/).")
    args = parser.parse_args()

    #? directory
    os.makedirs(args.path, exist_ok=True)
    
    # if -r flag is not set, set depth to 0
    max_depth = args.level if args.recursive else 0

    crawl_website(args.url, max_depth, args.path, args.recursive)
    print("\n✨ Crawl finished.")


if __name__ == "__main__":
    main()