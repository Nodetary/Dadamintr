from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
import time

class UniversalScraper(ABC):
    def __init__(self, ai_assistant, config_path: Optional[str] = None):
        self.session = requests.Session()
        self.ai_assistant = ai_assistant
        self.config = self._load_config(config_path) if config_path else {}
        self.output_dir = "/data/output"
        self.downloads_dir = "/data/downloads"

    def initialize_scraping(self, url: str, target_data: str) -> bool:
        """Initialize scraping process with AI guidance"""
        try:
            # Check if we have existing configuration
            site_config = self._get_site_config(url)
            if not site_config:
                print("Generating new site configuration...")
                site_config = self.ai_assistant.generate_site_config(url, target_data)
                self._save_site_config(url, site_config)

            # Get required elements (cookies, headers, etc.)
            requirements = self.ai_assistant.get_required_elements(url)
            
            # Guide user through setup
            if requirements['authentication_required']:
                self._guide_authentication_setup(url)
            
            if requirements['cookies_needed']:
                self._guide_cookie_setup(url)
                
            return True
            
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def _guide_authentication_setup(self, url: str):
        """Guide user through authentication setup"""
        guidance = self.ai_assistant.guide_user(
            f"Explain how to authenticate for {url}"
        )
        print("\nAuthentication Setup Guide:")
        print(guidance)
        
        # Interactive setup based on AI guidance
        input("\nPress Enter once you've completed authentication...")

    def _guide_cookie_setup(self, url: str):
        """Guide user through cookie setup"""
        guidance = self.ai_assistant.guide_user(
            f"Explain how to obtain cookies for {url}"
        )
        print("\nCookie Setup Guide:")
        print(guidance)
        
        # Interactive cookie collection
        cookies = self._collect_cookies()
        self._save_cookies(cookies)

    def scrape_data(self, url: str, target_data: str) -> List[Dict]:
        """Main scraping method with AI assistance"""
        if not self.initialize_scraping(url, target_data):
            return []

        all_data = []
        page = 1
        
        while True:
            try:
                print(f"Scraping page {page}...")
                html_content = self._fetch_page(url, page)
                
                # Use AI to analyze page structure
                structure = self.ai_assistant.analyze_page_structure(html_content)
                
                # Generate or update selectors if needed
                selectors = self.ai_assistant.generate_selectors(target_data, structure)
                
                # Extract data using selectors
                page_data = self._extract_data(html_content, selectors)
                
                # Validate extracted data
                is_valid, message = self.ai_assistant.validate_data(page_data)
                if not is_valid:
                    print(f"Data validation failed: {message}")
                    break
                
                all_data.extend(page_data)
                
                if not self._has_next_page(html_content):
                    break
                    
                page += 1
                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

        return all_data

    @abstractmethod
    def _extract_data(self, html_content: str, selectors: List[str]) -> List[Dict]:
        """Extract data using provided selectors"""
        pass

    @abstractmethod
    def _has_next_page(self, html_content: str) -> bool:
        """Check if there's a next page"""
        pass

    def _collect_cookies(self) -> Dict:
        """Interactive cookie collection"""
        print("\nPlease enter cookies (press Enter twice to finish):")
        cookies = {}
        while True:
            name = input("Cookie name (or press Enter to finish): ").strip()
            if not name:
                break
            value = input("Cookie value: ").strip()
            cookies[name] = value
        return cookies

    def _load_config(self, config_path: str) -> Dict:
        """Load scraper configuration"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def _save_site_config(self, url: str, config: Dict):
        """Save site-specific configuration"""
        filename = f"site_configs/{url.replace('://', '_').replace('/', '_')}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)

    def _save_cookies(self, cookies: Dict):
        """Save cookies to configuration"""
        with open('config/cookies.json', 'w') as f:
            json.dump(cookies, f, indent=2)

    def export_data(self, data: List[Dict], format: str = 'excel'):
        """Export scraped data in specified format"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if format == 'excel':
            self._export_to_excel(data, f"scraping_results_{timestamp}.xlsx")
        elif format == 'json':
            self._export_to_json(data, f"scraping_results_{timestamp}.json")
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _export_to_excel(self, data: List[Dict], filename: str):
        """Export data to Excel"""
        import pandas as pd
        df = pd.DataFrame(data)
        filepath = os.path.join(self.output_dir, filename)
        df.to_excel(filepath, index=False)
        print(f"Data exported to {filepath}")

    def _export_to_json(self, data: List[Dict], filename: str):
        """Export data to JSON"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data exported to {filepath}")

    def _get_site_config(self, url: str) -> Optional[Dict]:
        """Get site-specific configuration if it exists"""
        filename = f"site_configs/{url.replace('://', '_').replace('/', '_')}.json"
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def _fetch_page(self, url: str, page: int, max_retries: int = 3) -> str:
        """Fetch page content with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params={'page': page})
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to fetch page {page} after {max_retries} attempts: {e}")
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff 