import os
import re
from urllib.parse import urljoin, urlparse, quote
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import chardet


def filename_from_url(url):
    parsed = urlparse(url)
    path = os.path.basename(parsed.path) or "resource"
    if parsed.query:
        path += "_" + quote(parsed.query, safe="")
    return path


def detect_encoding(content_bytes):
    detected = chardet.detect(content_bytes)
    return detected["encoding"] or "utf-8"


def download_file(session, url, folder):
    try:
        filename = filename_from_url(url)
        local_path = os.path.join(folder, filename)
        r = session.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return filename
    except Exception as e:
        print(f"[!] Failed to download {url}: {e}")
        return None


def extract_css_urls(css_text):
    return re.findall(r'url\((["\']?)(.*?)\1\)', css_text)


def download_complete_webpage(url, output_dir="downloaded_page"):
    os.makedirs(output_dir, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    encoding = detect_encoding(resp.content)
    html_text = resp.content.decode(encoding, errors="replace")
    soup = BeautifulSoup(html_text, "html.parser")

    tags_attrs = {
        "link": "href",
        "script": "src",
        "img": "src",
        "iframe": "src",
    }

    downloaded = {}

    for tag, attr in tags_attrs.items():
        for element in tqdm(soup.find_all(tag)):
            res_url = element.get(attr)
            if not res_url or res_url.startswith("data:") or res_url.startswith("about:"):
                continue  # ← ここで about: を無視

            full_url = urljoin(url, res_url)
            if full_url in downloaded:
                filename = downloaded[full_url]
            else:
                filename = download_file(session, full_url, output_dir)
                if filename:
                    downloaded[full_url] = filename

            if filename:
                element[attr] = filename

    # CSS内の画像等も再帰的に取得
    for full_url, filename in tqdm(downloaded.items()):
        if filename.endswith(".css"):
            local_path = os.path.join(output_dir, filename)
            try:
                css_text = open(local_path, "r", encoding="utf-8", errors="ignore").read()
                urls_in_css = extract_css_urls(css_text)
                for _, inner_url in urls_in_css:
                    if inner_url.startswith("data:") or inner_url.startswith("about:"):
                        continue
                    full_css_url = urljoin(full_url, inner_url)
                    css_res_name = download_file(session, full_css_url, output_dir)
                    if css_res_name:
                        css_text = css_text.replace(inner_url, css_res_name)
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(css_text)
            except Exception as e:
                print(f"[!] Failed to process CSS {filename}: {e}")

    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"\n✅ 完了！HTMLとリソースは以下に保存されました:\n{html_path}")


# 使用方法
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python download_webpage.py https://example.com")
        sys.exit(1)
    target_url = sys.argv[1]
    download_complete_webpage(target_url)
