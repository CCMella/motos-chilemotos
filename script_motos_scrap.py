import csv
import random
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.chilemotos.com/moto"
CSV_FILE = r"C:\Users\camil\OneDrive\Escritorio\automatizado\motos_chilemotos\motos_chilemotos.csv"
HEADERS = ["titulo", "precio", "ano", "kilometraje", "cilindrada", "url"]

def extract_motos(page):
    items = page.query_selector_all('.geodir-post')
    results = []
    for item in items:
        title_el = item.query_selector('.geodir-entry-title a')
        title = title_el.inner_text().strip() if title_el else ''
        url = title_el.get_attribute('href') if title_el else ''

        price_el = item.query_selector('.geodir-field-price')
        price = price_el.inner_text().strip() if price_el else ''

        year_el = item.query_selector('.geodir-field-ano_de_fabricacion')
        year = year_el.inner_text().strip() if year_el else ''

        km_el = item.query_selector('.geodir-field-kilometraje')
        km = km_el.inner_text().strip() if km_el else ''

        cil_el = item.query_selector('.geodir-field-cilindrada')
        cil = cil_el.inner_text().strip() if cil_el else ''

        results.append({"titulo": title, "precio": price, "ano": year, "kilometraje": km, "cilindrada": cil, "url": url})
    return results

def get_last_page(page):
    links = page.query_selector_all('.navigation a')
    last = 1
    for a in links:
        text = a.inner_text().strip()
        if text.isdigit():
            num = int(text)
            if num > last:
                last = num
    return last

def load_existing_urls():
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            if "url" not in reader.fieldnames:
                return set()
            return {row["url"] for row in reader if row["url"]}
    except (FileNotFoundError, KeyError):
        return set()

def main():
    existing_urls = load_existing_urls()
    print(f"Registros existentes en el CSV: {len(existing_urls)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-CL",
            timezone_id="America/Santiago"
        )
        page = context.new_page()

        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            if not existing_urls:
                writer.writerow(HEADERS)

            page.goto(BASE_URL, wait_until="domcontentloaded")
            time.sleep(random.uniform(3, 5))

            last_page = get_last_page(page)
            print(f"Total de paginas encontradas: {last_page}")

            nuevas = 0
            for current_page_num in range(1, last_page + 1):
                if current_page_num > 1:
                    url = f"{BASE_URL}/page/{current_page_num}/"
                    page.goto(url, wait_until="domcontentloaded")
                    time.sleep(random.uniform(3, 5))

                print(f"Scrapeando pagina {current_page_num}/{last_page}...")
                motos = extract_motos(page)
                print(f"  -> {len(motos)} motos encontradas")

                for moto in motos:
                    if moto["url"] not in existing_urls:
                        writer.writerow([moto["titulo"], moto["precio"], moto["ano"], moto["kilometraje"], moto["cilindrada"], moto["url"]])
                        existing_urls.add(moto["url"])
                        nuevas += 1

                time.sleep(random.uniform(2, 4))

        browser.close()
        print(f"\nListo! {nuevas} motos nuevas agregadas a {CSV_FILE}")

if __name__ == "__main__":
    main()



