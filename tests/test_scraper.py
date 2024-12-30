import pytest
from app.scraper.base import UniversalScraper
from app.ai_assistant.base import AIAssistant

def test_scraper_initialization():
    ai_assistant = MockAIAssistant()
    scraper = UniversalScraper(ai_assistant)
    assert scraper.output_dir == "/data/output"
    assert scraper.downloads_dir == "/data/downloads"

def test_cookie_collection():
    ai_assistant = MockAIAssistant()
    scraper = UniversalScraper(ai_assistant)
    cookies = {"session": "test123"}
    assert scraper._save_cookies(cookies) is None

class MockAIAssistant(AIAssistant):
    def analyze_page_structure(self, html_content: str):
        return {"type": "test"}
        
    def generate_selectors(self, target_data_description: str, page_structure: dict):
        return [".test-selector"] 