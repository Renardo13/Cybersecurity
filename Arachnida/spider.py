#!/usr/bin/python3

# Take the content of the url of the website
# Create the folder dest
# Take with beautiful soup all the balise html <img>
# Curl the img to download 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
# For creating directories
import os
import argparse
from urllib.parse import urlparse

extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

def parsing():
    parser = argparse.ArgumentParser(description="Spider: download images from a website.")

    parser.add_argument("url", help="URL to extract images from")
    parser.add_argument("-r", "--recursive", action="store_true", help="Download recursively")
    # nammed arguments (...=...)
    parser.add_argument("-l", "--level", type=int, default=5, help="Maximum recursion depth (default: 5)") 
    parser.add_argument("-p", "--path", default="./data/", help="Path to save downloaded files")

    args = parser.parse_args()
    return(args)

# debug
def print_arg(args):
    print("URL:", args.url)
    print("Recursive:", args.recursive)
    print("Level:", args.level)
    print("Path:", args.path)

def create_dir(args):
    try:
        os.makedirs(args.path, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {args.path}: {e}")
        exit(1)

def right_extension(url):
    for ext in extensions:
        if ext in url:
            return True
    return False


# transorm url in absolute path in the website
# take the name of the pic with urlparse
def download_img(args, src):

    try:
        # Take the obsolute url
        img_url = urljoin(args.url, src)

        # Parse the name of the pic
        filename = os.path.basename(urlparse(img_url).path)
        if not filename:
            filename = "image.jpg"

        # entiere path of destination folder because open takes the path of the future downloaded file.
        # ex : foldername/filename.jpg
        filepath = os.path.join(args.path, filename)

        response = requests.get(img_url)

        with open(filepath, "wb") as folder:
            folder.write(response.content)

        print(f"Downloaded {filepath}")

    except Exception as e:
            print(f"Failed to download {src}: {e}")


def get_image(html, args):
    soup = BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src or not right_extension(src):
            continue
        download_img(args, src)


def url_check(args):
    try:
        response = requests.get(args.url)
    except Exception as e:
        print("Failed to download {args.url}: {e}")
    return(response.text)


def main():
    args = parsing()
    create_dir(args)
    html = url_check(args)
    get_image(html, args)

if __name__ == "__main__":
    main()
