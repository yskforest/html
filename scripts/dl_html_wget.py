import time
import os
import subprocess
import re
import argparse

import requests
from bs4 import BeautifulSoup


def sanitize_filename(name: str) -> str:
    """ファイル名・ディレクトリ名に使えない文字を除去"""
    return re.sub(r'[\\/:"*?<>|]+', "_", name)


def get_title(url: str, timeout: int = 10) -> str:
    """URLからタイトルを取得"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "untitled"
        return sanitize_filename(title)
    except Exception as e:
        print(f"[!] タイトル取得失敗: {url} - {e}")
        return "untitled"


def run_wget(wget_path: str, url: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(
        [
            wget_path,
            "--convert-links",
            "--page-requisites",
            "--adjust-extension",
            "--no-host-directories",
            "--cut-dirs=100",
            "--directory-prefix",
            output_dir,
            url,
        ]
    )
    if result.returncode != 0:
        print(f"[!] wget exited with code {result.returncode} for {url}")


def download_multiple_urls(wget_path: str, url_list: list[str], base_dir: str, delay: float = 1.5):
    os.makedirs(base_dir, exist_ok=True)
    for url in url_list:
        url = url.strip()
        if not url:
            continue
        print(f"[+] Processing: {url}")
        title = get_title(url)
        output_dir = os.path.join(base_dir, title)
        run_wget(wget_path, url, output_dir)
        print(f"[+] Done: {title}\n")
        time.sleep(delay)  # ← 適度に待機


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download web pages with wget and organize by title.")
    parser.add_argument("input", help="Path to input text file with URLs")
    parser.add_argument("-o", "--output", default="saved_pages", help="Directory to save downloaded pages")
    parser.add_argument("--wget", default="./wget.exe", help="Path to wget executable")
    parser.add_argument("--delay", type=float, default=1.5, help="Wait time (seconds) between downloads")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"[!] Input file not found: {args.input}")
        exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        urls = f.readlines()

    download_multiple_urls(args.wget, urls, args.output, delay=args.delay)
