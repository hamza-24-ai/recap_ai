from docx import Document
from io import BytesIO

def extractor_text_from_file(file_bytes : bytes, file_name : str) -> str:

    ext = "."+ file_name.split(".")[-1].lower()

    if ext == ".txt":
        return file_bytes.decode("utf-8")
    
    elif ext == ".docx":
        text_data = Document(BytesIO(file_bytes))

        text = "/n".join([para.text for para in text_data.paragraphs])
        return text
    
    else:
        return ValueError(f"Unsported File Error : {ext}")