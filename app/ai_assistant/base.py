from abc import ABC, abstractmethod
import json
from typing import Dict, List, Optional

class AIAssistant(ABC):
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.conversation_history = []

    @abstractmethod
    def analyze_page_structure(self, html_content: str) -> Dict:
        """Analyze webpage structure and identify key elements"""
        pass

    @abstractmethod
    def generate_selectors(self, target_data_description: str, page_structure: Dict) -> List[str]:
        """Generate CSS/XPath selectors based on target data description"""
        pass

    @abstractmethod
    def guide_user(self, context: str) -> str:
        """Generate guidance for the user based on context"""
        pass

    @abstractmethod
    def validate_data(self, scraped_data: List[Dict]) -> tuple[bool, str]:
        """Validate scraped data quality and structure"""
        pass

    def _load_config(self, config_path: str) -> Dict:
        """Load AI service configuration"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def save_conversation(self, output_path: str):
        """Save conversation history for future reference"""
        with open(output_path, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)

    def get_required_elements(self, website_url: str) -> Dict:
        """Determine required elements for scraping (cookies, headers, etc.)"""
        requirements = {
            'cookies_needed': False,
            'authentication_required': False,
            'required_headers': [],
            'guidance': ''
        }
        
        # Ask AI to analyze website requirements
        prompt = f"Analyze the requirements for scraping {website_url}"
        response = self.guide_user(prompt)
        
        # Process AI response and update requirements
        # Implementation specific to each AI service
        
        return requirements

    def generate_site_config(self, url: str, target_data: str) -> Dict:
        """Generate scraping configuration for a new website"""
        config = {
            'url': url,
            'selectors': {},
            'required_cookies': [],
            'pagination': None,
            'data_validation': {}
        }
        
        # Use AI to analyze and generate configuration
        prompt = f"Generate scraping configuration for {url} to extract {target_data}"
        response = self.guide_user(prompt)
        
        # Process AI response and update config
        # Implementation specific to each AI service
        
        return config 