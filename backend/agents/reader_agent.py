import os
import uuid
import requests
import fitz  # PyMuPDF
import shutil

class ReaderAgent:

    def __init__(self):
        self.download_folder = "data/papers"
        os.makedirs(self.download_folder, exist_ok=True)

    def download_pdf(self, pdf_url: str):

        filename = f"{uuid.uuid4()}.pdf"
        path = os.path.join(self.download_folder, filename)
        response = requests.get(pdf_url, timeout=60)
        response.raise_for_status()
        with open(path, "wb") as file:
            file.write(response.content)
        return path

    def extract_text(self, pdf_path: str):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text
    
    def save_uploaded_pdf(self, uploaded_file):
        filename = f"{uuid.uuid4()}.pdf"
        path = os.path.join(
            self.download_folder,
            filename
        )
        shutil.copyfile(uploaded_file, path)
        return path
    
    def save_uploaded_file(self, uploaded_file):
        filename = f"{uuid.uuid4()}.pdf"
        path = os.path.join(
            self.download_folder,
            filename
        )
        with open(path, "wb") as f:
            f.write(uploaded_file.file.read())
        return path