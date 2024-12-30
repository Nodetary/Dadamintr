import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class AdobeStockScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://stock.adobe.com"
        self.license_history_url = f"{self.base_url}/Dashboard/LicenseHistory"
        self.output_dir = "/data/output"
        self.thumbnails_dir = "/data/thumbnails"
        self.config_dir = "/app/config"
        
        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        
        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
        # Load cookies from config
        self.load_cookies()

    def load_cookies(self):
        """Load cookies from config/cookies.json"""
        cookie_file = os.path.join(self.config_dir, 'cookies.json')
        try:
            with open(cookie_file, 'r') as f:
                self.cookies = json.load(f)
                print("Successfully loaded cookies from config file")
        except FileNotFoundError:
            print(f"Cookie file not found at {cookie_file}")
            self.cookies = {}
        except json.JSONDecodeError:
            print(f"Error parsing cookie file at {cookie_file}")
            self.cookies = {}

    def get_page(self, page_number=1):
        """Fetch a single page of license history"""
        params = {'page': page_number}
        
        response = self.session.get(
            self.license_history_url,
            cookies=self.cookies,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page {page_number}: {response.status_code}")
        return response.text

    def parse_page(self, html_content):
        """Parse the license history page content"""
        soup = BeautifulSoup(html_content, 'lxml')
        assets = []

        # Find all asset rows in the table
        for row in soup.select('tr:has(td)'):  # Select rows that contain td elements
            try:
                columns = row.select('td')
                if len(columns) >= 6:
                    asset = {
                        'date': columns[0].text.strip(),
                        'author': columns[1].text.strip(),
                        'asset_id': columns[2].text.strip(),
                        'license': columns[3].text.strip(),
                        'media_type': columns[4].text.strip(),
                        'price': columns[5].text.strip()
                    }
                    
                    # Try to get thumbnail URL if available
                    img = row.select_one('img')
                    if img and img.get('src'):
                        asset['thumbnail_url'] = img['src']
                    
                    assets.append(asset)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue

        return assets

    def download_thumbnail(self, url, asset_id):
        """Download thumbnail image for an asset"""
        if not url:
            return None
            
        filename = os.path.join(self.thumbnails_dir, f"{asset_id}.jpg")
        
        if not os.path.exists(filename):
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    return filename
            except Exception as e:
                print(f"Error downloading thumbnail for asset {asset_id}: {e}")
        return None

    def scrape_all_pages(self, max_pages=None):
        """Scrape all pages of license history"""
        all_assets = []
        page = 1
        
        while True:
            try:
                print(f"Scraping page {page}...")
                html_content = self.get_page(page)
                assets = self.parse_page(html_content)
                
                if not assets:
                    break
                
                # Download thumbnails
                for asset in assets:
                    if 'thumbnail_url' in asset:
                        thumbnail_path = self.download_thumbnail(
                            asset['thumbnail_url'],
                            asset['asset_id']
                        )
                        asset['local_thumbnail_path'] = thumbnail_path
                
                all_assets.extend(assets)
                
                if max_pages and page >= max_pages:
                    break
                    
                page += 1
                time.sleep(2)  # Respectful delay between requests
                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break
        
        return all_assets

    def save_to_excel(self, assets):
        """Save the asset data to an Excel file"""
        if not assets:
            print("No assets to save")
            return None
            
        filename = os.path.join(
            self.output_dir,
            f"adobe_stock_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
            
        df = pd.DataFrame(assets)
        
        # Reorder columns for better readability
        columns = ['date', 'asset_id', 'media_type', 'author', 'license', 'price', 
                  'thumbnail_url', 'local_thumbnail_path']
        df = df.reindex(columns=[col for col in columns if col in df.columns])
        
        # Create Excel writer with xlsxwriter engine
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Asset Inventory')
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Asset Inventory']
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)
        
        print(f"Saved {len(assets)} records to {filename}")
        return filename

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
