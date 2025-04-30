# models/document_validator.py

import easyocr
from difflib import SequenceMatcher
from PIL import Image, ImageEnhance
import io
import openai
import os

class DocumentValidator:
    def __init__(self):
        self.reader = easyocr.Reader(['pt'], gpu=False)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def similaridade(self, a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def validate(self, uploaded_file, nome, cpf):
        try:
            # 🧠 Pré-processamento da imagem
            image = Image.open(uploaded_file).convert("L")  # escala de cinza
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.5)  # aumenta contraste

            buf = io.BytesIO()
            image.save(buf, format="PNG")
            image_bytes = buf.getvalue()

            # 🔍 OCR com EasyOCR
            results = self.reader.readtext(image_bytes, detail=0, paragraph=False)
            texto_extraido = " ".join(results).lower()

            nome_limpo = nome.strip().lower()
            cpf_limpo = cpf.replace(".", "").replace("-", "").strip()

            print(f"[DEBUG] Nome informado: {nome_limpo}")
            print(f"[DEBUG] CPF informado: {cpf_limpo}")
            print(f"[DEBUG] Texto extraído: {texto_extraido}")

            # Similaridade rápida com nome (fallback)
            match = self.similaridade(nome_limpo, texto_extraido)
            print(f"[DEBUG] Similaridade (nome): {match}")

            if match > 0.7 and cpf_limpo in texto_extraido.replace(".", "").replace("-", "").replace(" ", ""):
                return True

            # Validação via GPT
            gpt_nome = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um assistente técnico de verificação de documentos via OCR."},
                    {"role": "user", "content": f"""
O nome informado pelo usuário é: "{nome_limpo}".

Texto extraído da imagem:
"{texto_extraido}"

O nome informado está visivelmente presente no texto (mesmo que com erros de OCR)? Responda apenas com SIM ou NÃO.
"""}
                ],
                temperature=0.1
            )

            gpt_cpf = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um assistente técnico de verificação de documentos via OCR."},
                    {"role": "user", "content": f"""
O CPF informado pelo usuário é: "{cpf_limpo}".

Texto extraído da imagem:
"{texto_extraido}"

O CPF informado está presente no texto (mesmo que com erros de OCR)? Responda apenas com SIM ou NÃO.
"""}
                ],
                temperature=0.1
            )

            resposta_nome = gpt_nome.choices[0].message.content.strip().lower()
            resposta_cpf = gpt_cpf.choices[0].message.content.strip().lower()

            print(f'Texto Extraido: {texto_extraido}')
            print(f"[DEBUG] GPT nome retornou: {resposta_nome}")
            print(f"[DEBUG] GPT cpf retornou: {resposta_cpf}")

            return "sim" in resposta_nome and "sim" in resposta_cpf

        except Exception as e:
            print(f"[ERRO] Validação com EasyOCR/GPT-4o: {e}")
            return False
