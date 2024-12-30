from typing import Dict, List
import google.generativeai as genai
from .base import AIAssistant

class GeminiAssistant(AIAssistant):
    def __init__(self, config_path: str):
        super().__init__(config_path)
        genai.configure(api_key=self.config["gemini"]["api_key"])
        self.model = genai.GenerativeModel(self.config["gemini"]["model"])

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
        
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)

    def generate_selectors(self, target_data_description: str, page_structure: Dict) -> List[str]:
        prompt = f"""
        Generate CSS selectors to extract {target_data_description} from a page with this structure:
        {page_structure}
        
        Return a list of precise CSS selectors.
        """
        
        response = self.model.generate_content(prompt)
        return self._parse_selectors(response.text) 