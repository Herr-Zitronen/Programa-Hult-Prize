import io
import re
import os
import requests
import json
from PyPDF2 import PdfReader
from docx import Document

class AIEngine:
    def __init__(self):
        # Migrated to standard Inference API URL for better stability
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.api_token = os.environ.get("HF_TOKEN")
        print("AI Engine initialized via Hugging Face API (Inference Endpoint).")

    def extract_text_from_pdf(self, file_bytes):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""

    def extract_text_from_docx(self, file_bytes):
        try:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_embedding(self, text: str):
        # Call Hugging Face API
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
        payload = {"inputs": text}
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Handle different return formats from HF API
                # Case 1: List of floats [0.1, 0.2, ...] (Standard for Feature Extraction)
                # Case 2: List of list [[0.1, ...]] (Batch mode sometimes)
                if isinstance(data, list):
                    if len(data) > 0 and isinstance(data[0], list):
                        return data[0]
                    return data
                # Case 3: Error dictionary wrapped in 200 (rare but possible)
                if isinstance(data, dict) and "error" in data:
                    print(f"HF API returned error in JSON: {data}")

            else:
                # Debug logging requested by user
                print(f"HF API Failed. Status: {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"HF API Exception: {e}")
        
        # Fallback: Zero vector (384 dimensions for MiniLM)
        print("Using Fallback Zero Vector due to API failure.")
        return [0.0] * 384

    def calculate_similarity(self, embedding1, embedding2):
        # Manual Cosine Similarity (No numpy/scikit-learn)
        
        if not embedding1 or not embedding2:
            return 0

        # Dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        
        # Magnitudes
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Clamp between 0 and 1
        similarity = max(0.0, min(1.0, similarity))
        
        return int(similarity * 100)

    def extract_keywords(self, text: str, role_text: str = ""):
        # Simple Explainability Logic (Regex based)
        
        def tokenize(s):
            # Lowercase and split by non-alphanumeric
            words = re.findall(r'\b[a-z]{3,}\b', s.lower())
            return set(words)

        cv_tokens = tokenize(text)
        role_tokens = tokenize(role_text)
        
        # Intersection
        common = cv_tokens.intersection(role_tokens)
        
        return list(common)
