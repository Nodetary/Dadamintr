from typing import Optional, Dict
import requests
from rotating_proxies import RotatingProxy

class ProxyManager:
    def __init__(self, proxy_config: Dict):
        self.proxy_list = proxy_config.get("proxies", [])
        self.current_index = 0
        self.rotating_proxy = RotatingProxy(self.proxy_list)
    
    def get_proxy(self) -> Optional[Dict]:
        if not self.proxy_list:
            return None
        return self.rotating_proxy.get_proxy()
    
    def mark_bad_proxy(self, proxy: Dict):
        self.rotating_proxy.mark_bad_proxy(proxy) 