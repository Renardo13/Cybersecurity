#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import os
import argparse

extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
visited = set()  # url already visited


def parsing():
    parser = argparse.ArgumentParser(description="Spider: download images from a website.")
    parser.add_argument("url")
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("-l", "--level", type=int, default=5)
    parser.add_argument("-p", "--path", default="./data/")
    return parser.parse_args()


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def right_extension(url):
    return any(url.lower().endswith(ext) for ext in extensions)


def download_img(img_url, dest_path):
    filename = os.path.basename(urlparse(img_url).path)
    if not filename:
        filename = "image.jpg"

    filepath = os.path.join(dest_path, filename)

    r = requests.get(img_url)
    with open(filepath, "wb") as f:
        f.write(r.content)

    print(f"Downloaded → {filepath}")


def get_images(url, html, args):
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        img_url = urljoin(url, src)
        if right_extension(img_url):
            download_img(img_url, args.path)


def fetch(url):
    try:
        r = requests.get(url)
        return r.text
    except:
        return ""


def url_levels(url, max_level):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    parts = parsed.path.strip('/').split('/')

    urls = [url]
    if max_level == 0:
        return urls

    current_level = 1
    while len(parts) > 1 and current_level <= max_level:
        parts.pop()
        urls.append(base + "/" + "/".join(parts) + "/")
    urls.append(base + "/")
    return urls


def crawl(url, args, level):

    # clean up to prevent double
    url, _ = urldefrag(url)

    if url in visited or level < 0:
        return
    visited.add(url)

    print(f"Crawling: {url}")
    html = fetch(url)
    if not html:
        return

    get_images(url, html, args)

    if args.recursive and level > 0:
        soup = BeautifulSoup(html, "html.parser")
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        for link in soup.find_all("a", href=True):
            href = link['href']
            # ignore extern links
            if href.startswith("http") and not href.startswith(base):
                continue
            next_url = urljoin(base, href)
            crawl(next_url, args, level - 1)


def main():
    args = parsing()
    create_dir(args.path)

    levels = url_levels(args.url, args.level)
    for lvl_url in levels:
        print(f"\nExploring level URL: {lvl_url}")
        html = fetch(lvl_url)
        get_images(lvl_url, html, args)
        if args.recursive:
            crawl(lvl_url, args, args.level)


if __name__ == "__main__":
    main()
