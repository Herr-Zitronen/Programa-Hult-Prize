import re
import io
from PyPDF2 import PdfReader
from docx import Document

class AIEngine:
    def __init__(self):
        print("Logic NLP Engine initialized (Deterministic Mode - Aggressive).")

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

    def clean_tokenize(self, text: str):
        # Limpieza agresiva: minúsculas y solo alfanuméricos
        text = text.lower()
        # Reemplazar puntuación por espacios para no pegar palabras
        text = re.sub(r'[^a-z0-9áéíóúñ]', ' ', text) 
        tokens = set(text.split())
        
        # Stopwords mínimas para no filtrar de más por error
        STOPWORDS = {
            "de", "la", "que", "el", "en", "y", "a", "los", "del", "las", "un", "una", "por", "para", "con", "no", "sus", 
            "is", "the", "and", "to", "of", "in"
        }
        
        return {w for w in tokens if w not in STOPWORDS and len(w) > 2}

    def get_embedding(self, text: str):
        # Mock para compatibilidad con llamadas legacy
        return []

    def calculate_similarity_and_skills(self, cv_text: str, role_text: str):
        cv_tokens = self.clean_tokenize(cv_text)
        role_tokens = self.clean_tokenize(role_text)

        intersection = cv_tokens.intersection(role_tokens)
        match_count = len(intersection)
        
        # FÓRMULA AGRESIVA PARA DEMO:
        # Base 15%. Cada palabra coincidente suma 12%.
        # 3 coincidencias = 51%
        # 5 coincidencias = 75%
        # 7 coincidencias = 99%
        score = 15 + (match_count * 12)

        return min(98, int(score)), list(intersection)

    def analyze_cv(self, cv_text, role_text):
        """
        Function that orchestrates the analysis and returns the expected dictionary format.
        """
        score, skills = self.calculate_similarity_and_skills(cv_text, role_text)
        return {
            "score": score,
            "matched_skills": skills[:10],  # Top 10 coincidencias
            "explanation": f"Se encontraron {len(skills)} coincidencias clave."
        }
