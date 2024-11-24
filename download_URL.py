import requests
from http.cookiejar import MozillaCookieJar
import os

file_path = 'links_ortsat2023_jesus.txt'
output_dir = './ortosat_tifs'

# Load cookies from browser export
cookie_jar = MozillaCookieJar("cookies.txt")
cookie_jar.load()

os.makedirs(output_dir, exist_ok=True)

def download_files_with_cookies(url_file, cookies):
    with open(url_file, 'r') as file:
        urls = file.readlines()

    for idx, url in enumerate(urls):
        url = url.strip()
        if not url:
            continue

        file_name = url.split('/')[-1] or f'file_{idx}.dat'
        output_path = os.path.join(output_dir, file_name)

        try:
            print(f'Downloading {url}...')
            response = requests.get(url, cookies=cookies, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f'Successfully downloaded to {output_path}')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download {url}: {e}')

download_files_with_cookies(file_path, cookie_jar)
