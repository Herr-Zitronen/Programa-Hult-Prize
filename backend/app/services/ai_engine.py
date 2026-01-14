import io
import re
import numpy as np
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
from docx import Document
from sklearn.metrics.pairwise import cosine_similarity

class AIEngine:
    def __init__(self):
        # Load the specified lightweight model
        print("Loading AI Model: all-MiniLM-L6-v2...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("AI Model loaded successfully.")

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
        # Basic cleanup: remove extra whitespace, distinct characters could be removed if needed
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_embedding(self, text: str):
        # Generate embedding for a single text
        return self.model.encode(text, convert_to_tensor=False)

    def calculate_similarity(self, embedding1, embedding2):
        # Calculate cosine similarity between two embeddings
        emb1 = embedding1.reshape(1, -1)
        emb2 = embedding2.reshape(1, -1)
        score = cosine_similarity(emb1, emb2)[0][0]
        # Return integer 0-100
        return int(score * 100)

    def extract_keywords(self, text: str, role_text: str = ""):
        # Simple Explainability Logic:
        # 1. Tokenize both texts (simple split by non-word chars)
        # 2. Filter out short words (stopwords check would be better but simple length works for MVP)
        # 3. Find intersection
        
        def tokenize(s):
             # Lowercase and split by non-alphanumeric
            words = re.findall(r'\b[a-z]{3,}\b', s.lower())
            return set(words)

        cv_tokens = tokenize(text)
        role_tokens = tokenize(role_text)
        
        # Common tokens, excluding very common generic words if we had a list, 
        # but intersection with Role usually limits it to relevant terms implicitly.
        common = cv_tokens.intersection(role_tokens)
        
        return list(common)
