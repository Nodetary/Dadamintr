class AIModelManager:
    def __init__(self, config_path: str):
        self.models = self._initialize_models(config_path)
        self.primary_model = "anthropic"  # Claude as default
        
    def get_response(self, prompt: str) -> str:
        try:
            return self.models[self.primary_model].generate_response(prompt)
        except Exception as e:
            print(f"Primary model failed: {e}, trying fallback...")
            for model_name, model in self.models.items():
                if model_name != self.primary_model:
                    try:
                        return model.generate_response(prompt)
                    except:
                        continue
            raise Exception("All AI models failed") 