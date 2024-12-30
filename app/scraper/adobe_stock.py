from .base import UniversalScraper
from bs4 import BeautifulSoup
from typing import Dict, List

class AdobeStockScraper(UniversalScraper):
    def _extract_data(self, html_content: str, selectors: List[str]) -> List[Dict]:
        soup = BeautifulSoup(html_content, 'lxml')
        assets = []

        for row in soup.select(selectors[0]):  # Assuming first selector is for rows
            try:
                columns = row.select(selectors[1])  # Assuming second selector is for columns
                if len(columns) >= 6:
                    asset = {
                        'date': columns[0].text.strip(),
                        'author': columns[1].text.strip(),
                        'asset_id': columns[2].text.strip(),
                        'license': columns[3].text.strip(),
                        'media_type': columns[4].text.strip(),
                        'price': columns[5].text.strip()
                    }
                    
                    img = row.select_one(selectors[2])  # Assuming third selector is for thumbnails
                    if img and img.get('src'):
                        asset['thumbnail_url'] = img['src']
                    
                    assets.append(asset)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue

        return assets

    def _has_next_page(self, html_content: str) -> bool:
        soup = BeautifulSoup(html_content, 'lxml')
        # Implement pagination detection logic
        next_button = soup.select_one('a.next-page')  # Adjust selector as needed
        return bool(next_button) 