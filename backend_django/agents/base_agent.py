from typing import Dict, Any
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class BaseAgent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

        # initial tokenizer and fine tuned model
        model_path = "/Users/parsaalizade/Desktop/ai-recruiter-agency/fine-tuning-results"
        
        # Check if model path exists, else fallback or warn
        if os.path.exists(model_path):
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
        else:
            print(f"Warning: Model path {model_path} not found. AI agents may not function correctly.")
            self.tokenizer = None
            self.model = None

    async def run(self, message: list) -> Dict[str, Any]:
        """default run method to be override by child classes"""
        raise NotImplementedError("Subclasses must implement run()")

    def _query_model(self, prompt: str) -> str:
        """Query the fine-tuned model with the given prompt"""
        if not self.model or not self.tokenizer:
            return "Error: Model not loaded."

        try:
            # Encode the prompt text
            # Use a larger context window. Most modern models support at least 2048.
            inputs = self.tokenizer.encode(
                self.instructions + prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=2048 
            )

            # Generate response
            # Use max_new_tokens to specify how much TO generate, regardless of prompt length
            outputs = self.model.generate(
                inputs, 
                max_new_tokens=1000,
                num_return_sequences=1, 
                temperature=0.7,
                do_sample=True # Enable sampling for more creative/varied outputs
            )

            # Decode the generated output
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

        except Exception as e:
            print(f"Error querying the model: {str(e)}")
            raise

    def _query_ollama(self, prompt: str) -> str:
        """Query the running Ollama instance via HTTP API"""
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.1",
            "prompt": self.instructions + "\n" + prompt,
            "stream": False,
            "format": "json" 
        }
        
        try:
            import requests
            print(f"DEBUG: Sending query to Ollama: {url}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("DEBUG: Ollama response received")
            return response.json().get("response", "")
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            # Fallback to local model if available, or raise
            return self._query_model(prompt)

    def _parse_json_safely(self, text: str) -> Dict[str, Any]:
        """Safely parse JSON from text, handling potential errors"""
        try:
            # Try to find JSON-like content between curly braces
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                json_str = text[start : end + 1]
                return json.loads(json_str)
            return {"error": "No JSON content found"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON content"}
