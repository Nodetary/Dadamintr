from typing import Dict, List
import openai
from .base import AIAssistant

class OpenAIAssistant(AIAssistant):
    def __init__(self, config_path: str):
        super().__init__(config_path)
        openai.api_key = self.config["openai"]["api_key"]
        self.model = self.config["openai"]["model"]

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
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return self._parse_response(response.choices[0].message.content)

    def generate_selectors(self, target_data_description: str, page_structure: Dict) -> List[str]:
        prompt = f"""
        Generate CSS selectors to extract {target_data_description} from a page with this structure:
        {page_structure}
        
        Return a list of precise CSS selectors.
        """
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        
        return self._parse_selectors(response.choices[0].message.content) 