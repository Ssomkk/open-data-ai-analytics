import requests
import os

# Папка для сирих даних
RAW_DIR = "../data/raw"

# Створюємо директорію, якщо її немає
os.makedirs(RAW_DIR, exist_ok=True)

# Список прямих URL на файли
urls = [
    "https://data.gov.ua/dataset/c445c6ea-f0c3-4167-abb1-5afb4a0e5499/resource/afa0c772-2554-4b9a-98b4-980e54b1e21a/download/pasport-naboru-danikh.xlsx",
    "https://data.gov.ua/dataset/c445c6ea-f0c3-4167-abb1-5afb4a0e5499/resource/d55eebcf-4660-4919-96b3-4894be5a6cda/download/nuclear_safety_q4_2025.xlsx",
]

for url in urls:
    filename = url.split("/")[-1]
    filepath = os.path.join(RAW_DIR, filename)

    print(f"Downloading {filename} ...")
    r = requests.get(url)

    if r.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"Saved to {filepath}")
    else:
        print(f"Failed to download {url} (status {r.status_code})")