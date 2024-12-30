from scraper.base import AdobeStockScraper

def main():
    scraper = AdobeStockScraper()
    try:
        assets = scraper.scrape_all_pages()
        if assets:
            scraper.save_to_excel(assets)
    except Exception as e:
        print(f"Scraping failed: {e}")

if __name__ == "__main__":
    main() 