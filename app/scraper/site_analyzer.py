from typing import Dict, List
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

class SiteAnalyzer:
    def __init__(self, ai_assistant):
        self.ai_assistant = ai_assistant
        self.analyzed_urls = set()
        self.site_map = {}

    def analyze_site(self, base_url: str, max_pages: int = 5) -> Dict:
        """Analyze site structure and patterns"""
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        
        for _ in range(max_pages):
            if len(self.analyzed_urls) >= max_pages:
                break
                
            url = self._get_next_url()
            if not url:
                break
                
            self._analyze_page(url)
        
        return self._generate_site_report()

    def _analyze_page(self, url: str) -> None:
        """Analyze individual page structure"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Analyze page structure using AI
            structure = self.ai_assistant.analyze_page_structure(response.text)
            
            self.site_map[url] = {
                'structure': structure,
                'forms': self._analyze_forms(soup),
                'navigation': self._analyze_navigation(soup),
                'data_tables': self._analyze_tables(soup)
            }
            
            self.analyzed_urls.add(url)
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")

    def _analyze_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Analyze forms and their fields"""
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'fields': []
            }
            
            for field in form.find_all(['input', 'select', 'textarea']):
                form_data['fields'].append({
                    'type': field.name,
                    'name': field.get('name', ''),
                    'id': field.get('id', ''),
                    'required': field.get('required', False)
                })
            
            forms.append(form_data)
        return forms

    def _analyze_navigation(self, soup: BeautifulSoup) -> Dict:
        """Analyze navigation structure"""
        nav_elements = soup.find_all(['nav', 'header', 'footer'])
        navigation = {
            'main_nav': [],
            'pagination': None,
            'breadcrumbs': []
        }
        
        for nav in nav_elements:
            links = nav.find_all('a')
            nav_type = self._determine_nav_type(nav)
            if nav_type == 'pagination':
                navigation['pagination'] = self._extract_pagination(nav)
            elif nav_type == 'breadcrumbs':
                navigation['breadcrumbs'] = [a.text.strip() for a in links]
            else:
                navigation['main_nav'].extend([{
                    'text': a.text.strip(),
                    'href': a.get('href', '')
                } for a in links])
        
        return navigation

    def _analyze_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Analyze data tables"""
        tables = []
        for table in soup.find_all('table'):
            table_data = {
                'headers': [],
                'rows': 0,
                'columns': 0,
                'has_pagination': False
            }
            
            headers = table.find_all('th')
            if headers:
                table_data['headers'] = [h.text.strip() for h in headers]
            
            rows = table.find_all('tr')
            table_data['rows'] = len(rows)
            if rows:
                table_data['columns'] = len(rows[0].find_all(['td', 'th']))
            
            tables.append(table_data)
        
        return tables

    def _generate_site_report(self) -> Dict:
        """Generate comprehensive site analysis report"""
        return {
            'base_url': self.base_url,
            'pages_analyzed': len(self.analyzed_urls),
            'common_patterns': self._identify_patterns(),
            'authentication': self._detect_authentication(),
            'site_map': self.site_map
        }

    def _identify_patterns(self) -> Dict:
        """Identify common patterns across pages"""
        patterns = {
            'selectors': {},
            'structures': {},
            'navigation': {}
        }
        
        # Analyze patterns using AI
        for url, data in self.site_map.items():
            structure = data['structure']
            self.ai_assistant.analyze_patterns(structure, patterns)
        
        return patterns

    def _detect_authentication(self) -> Dict:
        """Detect authentication requirements"""
        auth_forms = []
        login_urls = []
        
        for url, data in self.site_map.items():
            for form in data['forms']:
                if self._is_auth_form(form):
                    auth_forms.append({
                        'url': url,
                        'form': form
                    })
                    login_urls.append(url)
        
        return {
            'requires_auth': bool(auth_forms),
            'login_urls': login_urls,
            'auth_forms': auth_forms
        } 