from typing import List, Dict

class ScrapingProgress:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.state_file = f"/data/output/progress_{job_id}.json"
        self.state = self._load_state()
    
    def save_progress(self, page: int, data: List[Dict]):
        self.state["last_page"] = page
        self.state["items_collected"] += len(data)
        self._save_state()
    
    def can_resume(self) -> bool:
        return self.state["last_page"] > 0
    
    def get_resume_point(self) -> int:
        return self.state["last_page"] 