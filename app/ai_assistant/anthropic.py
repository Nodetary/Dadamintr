from typing import Dict, List
import anthropic
from .base import AIAssistant

class ClaudeAssistant(AIAssistant):
    def __init__(self, config_path: str):
        super().__init__(config_path)
        self.client = anthropic.Anthropic(
            api_key=self.config["anthropic"]["api_key"]
        )
        self.model = self.config["anthropic"]["model"]

    def analyze_page_structure(self, html_content: str) -> Dict:
        prompt = f"""
        Analyze this HTML content and identify key structural elements:
        {html_content[:2000]}...
        
        Return a JSON structure describing:
        1. Main content areas
        2. Navigation elements
        3. Data containers
        4. Pagination elements
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response.content)

    def generate_selectors(self, target_data_description: str, page_structure: Dict) -> List[str]:
        prompt = f"""
        Generate CSS selectors to extract {target_data_description} from a page with this structure:
        {page_structure}
        
        Return a list of precise CSS selectors.
        """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_selectors(response.content) 