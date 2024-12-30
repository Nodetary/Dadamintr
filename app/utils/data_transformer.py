from typing import Dict, List, Callable
import pandas as pd

class DataTransformer:
    def __init__(self):
        self.transformations: List[Callable] = []
    
    def add_transformation(self, func: Callable):
        self.transformations.append(func)
    
    def transform(self, data: List[Dict]) -> List[Dict]:
        for transform_func in self.transformations:
            data = transform_func(data)
        return data
    
    @staticmethod
    def clean_text(text: str) -> str:
        return " ".join(text.split())
    
    @staticmethod
    def standardize_dates(data: List[Dict], date_field: str) -> List[Dict]:
        for item in data:
            if date_field in item:
                try:
                    item[date_field] = pd.to_datetime(item[date_field]).strftime('%Y-%m-%d')
                except:
                    pass
        return data 